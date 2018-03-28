from automl import app, req
from automl.mltask.taskcontroller import TaskController
from automl.response import Response


@app.route('/task/task', methods=['POST'])
def on_task_run():
    data = req.get_json()
    TaskController.run_task.delay(graph_id=data['id'])
    return Response().ok(msg='success')


@app.route('/task/taskfromnode', methods=['POST'])
def on_task_from_node_run():
    data = req.get_json()
    TaskController.run_task_from_node.delay(graph_id=data['graphId'], node_id=data['nodeId'])
    return Response().ok(msg='success')
