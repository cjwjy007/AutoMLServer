from automl import app, req
from automl.mldata.datacontroller import DataController
from automl.response import Response


@app.route('/data/data', methods=['GET', 'DELETE'])
def get_dataset_list():
    if req.method == 'GET':
        data = DataController.get_dataset_by_page(page=req.args.get('page'))
        return Response().ok(msg='success', data=data)
    elif req.method == 'DELETE':
        data = req.get_json()
        id = data['id']
        ret = DataController.delete_dataset(id=id)
        if ret:
            return Response().ok(msg='success', data='')
        else:
            return Response().err(msg='failure', data='')


@app.route('/data/alldata', methods=['GET'])
def get_all_dataset():
    if req.method == 'GET':
        data = DataController.get_all_datasets()
        return Response().ok(msg='success', data=data)


@app.route('/data/uploaddata', methods=['POST'])
def upload_data():
    if req.method == 'POST':
        file = req.files['file']
        form = req.form
        ret = DataController.data_upload(file=file, form=form)
        if ret:
            return Response().ok(msg='success')
        else:
            return Response().err(msg='error')


@app.route('/data/datasetcount', methods=['GET'])
def dataset_counter():
    data = DataController.get_dataset_count()
    return Response().ok(msg='success', data=data)
