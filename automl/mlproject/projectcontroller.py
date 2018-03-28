import os
import random
import string
import datetime

from automl import db
from automl.errhandler.errhandler import ErrHandler
from automl.mlproject.projectmodel import Project
from filepath import resource_dir


class ProjectController:
    """
    ProjectController
    """

    def __init__(self):
        pass

    @staticmethod
    def create_project(project_name):
        """
        create a new project, insert database, create json file
        :param project_name: str
        project name
        :return: bool
        return if success
        """
        graph_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        status = 0
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_time = create_time
        proj = Project(project_name, graph_id, status, create_time, update_time)

        # create file
        try:
            open(os.path.join(resource_dir, '{0}.json'.format(graph_id)), 'w')
            open(os.path.join(resource_dir, '{0}_config.json'.format(graph_id)), 'w')
        except FileNotFoundError as e:
            ErrHandler().handle_err(e)

        # write to db and create file
        try:
            db.session.add(proj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            ProjectController.clear_file(graph_id)
            ErrHandler().handle_err(e)
        return True

    @staticmethod
    def get_project_count():
        """
        get the count of projects in database
        :return: int
        return the count
        """
        return Project.query.count()

    @staticmethod
    def get_project_by_page(page):
        """
        get project array by page, a page contains 10 columns
        :param page:
        :return: array
        return project array
        """
        start_index = (int(page) - 1) * 10
        result = Project.query.limit(10).offset(start_index).all()
        ret = []
        for r in result:
            r_dict = r.__dict__
            del r_dict['_sa_instance_state']
            ret.append(r_dict)
        return ret

    @staticmethod
    def delete_project(id):
        """
        delete project by project id
        :param id: int
        ID of project(primary key in database)
        :return: bool
        return if success
        """
        p = Project.query.filter_by(id=id).first()
        graph_id = p.graph_id
        try:
            # delete db record
            db.session.delete(p)
            db.session.commit()

            # delete file
            ProjectController.clear_file(graph_id)
            return True
        except Exception as e:
            db.session.rollback()
            ErrHandler().handle_err(e)

    @staticmethod
    def clear_file(graph_id):
        """
        delete json file of project
        :param graph_id: str
        ID of graph
        :return:
        """
        if os.path.exists(os.path.join(resource_dir, '{0}.json'.format(graph_id))):
            os.remove(os.path.join(resource_dir, '{0}.json'.format(graph_id)))
        if os.path.exists(os.path.join(resource_dir, '{0}_config.json'.format(graph_id))):
            os.remove(os.path.join(resource_dir, '{0}_config.json'.format(graph_id)))

    @staticmethod
    def modify_project_status(graph_id, status):
        """
        modify project status, 0: ready 1: running 2:success 3:fail
        :param graph_id: str
        ID of graph
        :param status: int
        status to be written
        :return: bool
        return if success
        """
        try:
            pj = Project.query.filter_by(graph_id=graph_id).first()
            if pj:
                pj.status = status
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            ErrHandler().handle_err(e)
        return True

    @staticmethod
    def get_project_status(graph_id):
        """
        get project status, 0: ready 1: running 2:success 3:fail
        :param graph_id: str
        ID of graph
        :return: int
        return project status
        """
        try:
            pj = Project.query.filter_by(graph_id=graph_id).first()
            if pj:
                return pj.status
        except Exception as e:
            ErrHandler().handle_err(e)

    @staticmethod
    def modify_db_update_time(graph_id):
        """
        when a graph updates, this function is called to modify update_time in database
        :param graph_id: str
        ID of graph
        :return: bool
        return if success
        """
        try:
            p = Project.query.filter_by(graph_id=graph_id).first()
            p.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            ErrHandler().handle_err(e)
        return True
