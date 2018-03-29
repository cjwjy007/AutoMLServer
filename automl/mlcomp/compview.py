from automl import app, req
from automl.mlcomp.compcontroller import CompController
from automl.response import Response

"""
/*
* url: '/config/columns'
* method: 'get'
* Request:
* Object
* data:{
*   graphId: graphId
* }
*
* Response:
* Object
* {
*   data:[columnName1,columnName2,columnName3...],
*   msg:responseMsg,
*   stateCode:responseCode
* }
*
* */
"""


@app.route('/config/columns', methods=['GET'])
def components_handler():
    graph_id = req.args.get('graphId')
    node_id = req.args.get('nodeId')
    columns = CompController.get_data_columns(graph_id=graph_id, node_id=node_id)
    return Response().ok(msg='success', data=columns)


@app.route('/config/datanames', methods=['GET'])
def get_father_data_node_names():
    graph_id = req.args.get('graphId')
    node_id = req.args.get('nodeId')
    names = CompController.get_data_names(graph_id=graph_id, node_id=node_id)
    return Response().ok(msg='success', data=names)


"""
/*
* url: '/config/columnsdetail'
* method: 'get'
* Request:
* Object
* data:{
*   graphId: graphId,
*   column: columnName
* }
*
* Response:
* Object
* {
*   data:{
*     feature1: value,
*     feature2: value
*     ...
*   },
*   msg:responseMsg,
*   stateCode:responseCode
* }
* */
"""


@app.route('/config/columnsdetail', methods=['GET'])
def components_detail():
    graph_id = req.args.get('graphId')
    node_id = req.args.get('nodeId')
    col_name = req.args.get('column')
    info = CompController.get_data_columns_detail(graph_id=graph_id, node_id=node_id, col_name=col_name)
    return Response().ok(msg='success', data=info)


"""
/*
* url: '/config/config'
* method: 'post'
* Request:
* Object
* data:{
*   graphId: graphId,
*   nodeId: nodeId,
*   config: configDetail
* }
*
* Response:
* Object
* {
*   data:null,
*   msg:responseMsg,
*   stateCode:responseCode
* }
* */

/*
* url: '/config/config'
* method: 'get'
* Request:
* Object
* data:{
*   graphId: graphId,
*   nodeId: nodeId
* }
*
* Response:
* Object
* {
*   data:{
*     config: configDetail,
*   },
*   msg:responseMsg,
*   stateCode:responseCode
* }
* */

"""


@app.route('/config/config', methods=['GET', 'POST'])
def config_handler():
    if req.method == 'GET':
        graph_id = req.args.get('graphId')
        node_id = req.args.get('nodeId')
        data = CompController.get_config(graph_id=graph_id, node_id=node_id)
        return Response().ok(msg='success', data=data)
    elif req.method == 'POST':
        data = req.get_json()
        state = CompController.set_config(graph_id=data['graphId'], node_id=data['nodeId'], config=data['config'])
        if state:
            return Response().ok(msg='success', data='')
        else:
            return Response().err(msg='failure', data='')
