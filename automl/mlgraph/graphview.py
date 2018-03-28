from automl import app, req
from automl.mlgraph.graphcontroller import GraphController
from automl.response import Response

"""
/*
* url: '/graph/graph'
* method: 'get'
* Request:
* Object
* data:{
*   id: graphId,
* }
*
* Response:
* Object
* {
*   data:graphData,
*   msg:responseMsg,
*   stateCode:responseCode
* }
*
* */

/*
* url: '/graph/graph'
* method: 'post'
* Request:
* Object
* data:{
*   id: graphId,
*   gData: graphData
* }
*
* Response:
* Object
* {
*   data:null,
*   msg:responseMsg,
*   stateCode:responseCode
* }
*
* */
"""


@app.route('/graph/graph', methods=['GET', 'POST'])
def graph():
    if req.method == 'GET':
        data = GraphController.get_graph(req.args.get('id'))
        return Response().ok(msg='success', data=data)
    elif req.method == 'POST':
        data = req.get_json()
        state = GraphController.save_graph(data['id'], data['gData'])
        if state:
            return Response().ok(msg='success', data='')
        else:
            return Response().err(msg='failure', data='')


"""
/*
* url: '/graph/nodestatus'
* method: 'get'
* Request:
* Object
* data:{
*   id: graphId,
* }
*
* Response:
* Object
* {
*   data:[{'node_id': node_id,'node_status': node_status}..],
*   msg:responseMsg,
*   stateCode:responseCode
* }
*
* */
"""


@app.route('/graph/nodestatus', methods=['GET'])
def get_node_status():
    data = GraphController.get_nodes_status(graph_id=req.args.get('id'))
    return Response().ok(msg='success', data=data)


@app.route('/graph/node', methods=['DELETE'])
def node_manager():
    data = req.get_json()
    ret = GraphController.delete_db_node_info(graph_id=data['graph_id'], node_id=data['node_id'])
    if ret:
        return Response().ok(msg='success', data=ret)
    else:
        return Response().err(msg='error', data=ret)


@app.route('/graph/nodeout', methods=['GET'])
def get_node_out():
    ret = GraphController.get_data_output_preview_by_node(graph_id=req.args.get('graphId'),
                                                          node_id=req.args.get('nodeId'))
    if ret:
        return Response().ok(msg='success', data=ret)
    else:
        return Response().err(msg='结果无法显示', data=ret)


@app.route('/graph/nodeoutdownload', methods=['GET'])
def download_node_out():
    ret = GraphController.download_data_output_by_node(graph_id=req.args.get('graphId'),
                                                       node_id=req.args.get('nodeId'))
    if ret:
        return ret
    else:
        return Response().err(msg='无法下载', data=ret)
