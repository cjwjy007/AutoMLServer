from automl import app, req
from automl.mlproject.projectcontroller import ProjectController
from automl.response import Response


@app.route('/project/project', methods=['GET', 'POST', 'DELETE'])
def project_handler():
    if req.method == 'GET':
        data = ProjectController.get_project_by_page(page=req.args.get('page'))
        return Response().ok(msg='success', data=data)
    elif req.method == 'POST':
        data = req.get_json()
        ret = ProjectController.create_project(project_name=data['projectName'])
        if ret:
            return Response().ok(msg='success', data='')
        else:
            return Response().err(msg='failure', data='')
    elif req.method == 'DELETE':
        data = req.get_json()
        id = data['id']
        ret = ProjectController.delete_project(id=id)
        if ret:
            return Response().ok(msg='success', data='')
        else:
            return Response().err(msg='failure', data='')


@app.route('/project/projectcount', methods=['GET'])
def project_counter():
    data = ProjectController.get_project_count()
    return Response().ok(msg='success', data=data)


@app.route('/project/projectstatus', methods=['GET'])
def get_project_status():
    data = ProjectController.get_project_status(graph_id=req.args.get('id'))
    return Response().ok(msg='success', data=data)
