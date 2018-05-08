import datetime
import os
import random
import string

from werkzeug.utils import secure_filename

from automl import db
from automl.errhandler.errhandler import ErrHandler
from automl.mldata.datamodel import DataSet
from filepath import data_dir


class DataController:
    """
    DataController handle things about uploaded dataset
    """

    def __init__(self):
        pass

    @staticmethod
    def _allowed_file(filename):
        """
        return if file is the format of txt or csv
        :param filename: string
        filename
        :return: bool
        return if the file is allowed
        """
        allowed = {'txt', 'csv', 'npz'}
        return '.' in filename and filename.split('.')[-1] in allowed

    @staticmethod
    def data_upload(file, form=None):
        """
        receive file from client
        :param file: obj
        upload file
        :param form: json
        upload extra data
        :return: bool
        return if the file is successfully uploaded
        """
        if form is None:
            form = {}
        if file and DataController._allowed_file(file.filename) and form.get('name'):
            try:
                # secure_filename causes an error when filename contains chinese characters
                # filename = secure_filename(file.filename)
                filename = file.filename
                save_path = os.path.join(data_dir, filename)
                # add a token if the file is exist
                if os.path.exists(save_path):
                    rand_token = "".join(random.sample(string.ascii_letters + string.digits, 8))
                    save_path = "{0}_{1}".format(save_path, rand_token)
                    file.save(save_path)
                else:
                    file.save(save_path)
                create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data_set = DataSet(name=form.get('name'), path=save_path, desc=form.get('desc'),
                                   create_time=create_time)
                db.session.add(data_set)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                ErrHandler.handle_err(e)

    @staticmethod
    def get_dataset_count():
        """
        count dataset in database
        :return: int
        return number of dataset in dataset
        """
        return DataSet.query.count()

    @staticmethod
    def get_dataset_by_page(page):
        """
        get dataset by page ID
        :param page: int
        page ID
        :return: array
        return datasets array in page
        """
        start_index = (int(page) - 1) * 10
        result = DataSet.query.limit(10).offset(start_index).all()
        ret = []
        for r in result:
            r_dict = r.__dict__
            if '_sa_instance_state' in r_dict:
                del r_dict['_sa_instance_state']
            ret.append(r_dict)
        return ret

    @staticmethod
    def get_all_datasets():
        """
        get all datasets
        :return: array
        return datasets array
        """
        result = DataSet.query.all()
        ret = []
        for r in result:
            r_dict = r.__dict__
            if '_sa_instance_state' in r_dict:
                del r_dict['_sa_instance_state']
            ret.append(r_dict)
        return ret

    @staticmethod
    def delete_dataset(id):
        """
        delete dataset by page ID
        :param id: int
        dataset id in database
        :return: bool
        return if the dataset is deleted
        """
        ds = DataSet.query.filter_by(id=id).first()
        path = ds.path
        try:
            # delete db record
            db.session.delete(ds)
            db.session.commit()

            # delete file
            return DataController._clear_file(path)
        except Exception as e:
            db.session.rollback()
            ErrHandler().handle_err(e)

    @staticmethod
    def _clear_file(path):
        """
        clear file
        :param path: str
        file path
        :return: bool
        return if the file is deleted
        """
        if os.path.exists(path):
            os.remove(path)
        return True

    @staticmethod
    def get_data_by_id(id):
        """
        get dataset by id
        :param id: int
        dataset id in database
        :return: int
        return number of dataset in dataset
        """
        ds = DataSet.query.filter_by(id=id).first()
        return ds

    @staticmethod
    def get_datapath_by_id(id):
        """
        get dataset by page ID
        :param id: int
        page ID
        :return: int
        return number of dataset in dataset
        """
        return DataController.get_data_by_id(id).path
