import json
import queue
import threading

import time

import os

from automl.errhandler.errhandler import ErrHandler
from automl.mlgraph.graphcontroller import GraphController
from automl.mlproject.projectcontroller import ProjectController
from automl.mltask.taskedge import TaskEdge
from automl.mltask.tasknode.nodefactory import NodeFactory
from filepath import resource_dir


class Task:
    """
    this is main class of running a task
    :param MAX_RUNING_TIME: int (second)
    when a task running over this time, the task will be closed automatically
    :param start_node_id: str
    it's start node id when you start task from a node, if it's None,the task runs from the beginning
    :param running_time_sum: int (second)
    current running time
    :param task_running_flag: bool
    a flag indicates if the task is running
    :param node_pool: array
    nodes in pool is waiting to run, when node's indegree is zero, it will be put in node_queue
    :param node_queue: queue
    task fetchs node from node_queue, create a thread to run the node
    :param node_dict: dict
    use node id to get node object
    :param edge_pool: array
    edge pool, initialled but not in used
    """

    def __init__(self, graph_id, start_node_id=None):
        self.MAX_RUNING_TIME = 3600
        self.task_id = graph_id
        self.start_node_id = start_node_id
        self.running_time_sum = 0
        self.task_running_flag = True
        self.node_pool = []
        self.node_queue = queue.Queue()
        self.node_dict = {}
        self.edge_pool = []
        self.create_task()
        self.init_indeg()
        

    def create_task(self):
        """
        when creating a Task object,this method is called
        this method create node and edge structures from json file
        run all nodes or run from a specific node are supported now
        :return:
        """
        graph_json = None
        config_json = None
        with open(os.path.join(resource_dir, '{0}.json'.format(self.task_id)), 'r') as graph:
            try:
                graph_json = json.load(graph)
            except IOError as e:
                ErrHandler().handle_err(e)
            except ValueError as e:
                ErrHandler().handle_err(e)
        with open(os.path.join(resource_dir, '{0}_config.json'.format(self.task_id)), 'r') as config:
            try:
                config_json = json.load(config)
            except ValueError as e:
                ErrHandler().handle_err(e)
            except IOError as e:
                ErrHandler().handle_err(e)
        if graph_json and config_json:
            nodes = graph_json.get('source').get('nodes')
            edges = graph_json.get('source').get('edges')
            # run all nodes in the graph
            if not self.start_node_id:
                # todo may be add a timestamp instead of deletion in the feature
                GraphController.delete_db_node_info(graph_id=self.task_id)
                for node in nodes:
                    task_node = NodeFactory.get_node(node=node)
                    task_node.set_config(config_json.get(node.get('id')))
                    self.node_pool.append(task_node)
                    self.node_dict[task_node.id] = task_node
                    GraphController.insert_db_node_info(graph_id=self.task_id, node=task_node)
                for edge in edges:
                    edge_node = TaskEdge(edge=edge)
                    self.edge_pool.append(edge_node)
            # run from specific node
            else:
                inpath = GraphController.get_inpath_by_node(graph_id=self.task_id, node_id=self.start_node_id)
                if inpath:
                    nodes_id_pool = self._get_all_children_node_ids(root_node_id=self.start_node_id, edges=edges)
                    for node in nodes:
                        if node['id'] in nodes_id_pool:
                            task_node = NodeFactory.get_node(node=node)
                            task_node.set_config(config_json.get(node.get('id')))
                            # handle special situation
                            if node['id'] == self.start_node_id:
                                task_node.inpath = inpath
                            elif node['desc'] == 'Prediction':
                                task_node.inpath = GraphController.get_inpath_by_node(graph_id=self.task_id,
                                                                                      node_id=node['id'])
                            self.node_pool.append(task_node)
                            self.node_dict[task_node.id] = task_node
                            GraphController.insert_db_node_info(graph_id=self.task_id, node=task_node)
                    for edge in edges:
                        edge_node = TaskEdge(edge=edge)
                        self.edge_pool.append(edge_node)
                else:
                    return False

    def run_task(self):
        """
        this is a background task
        run task method fetch those node with 0 indegree from node_pool
        this method stop when pool is empty or timeout
        :return:
        """
        ProjectController.modify_project_status(graph_id=self.task_id, status=1)
        while self.task_running_flag and self.running_time_sum <= self.MAX_RUNING_TIME:
            if not self.get_node():
                break
            self.consume_nodes()
            time.sleep(1)
            self.running_time_sum += 1
        if self.task_running_flag:
            ProjectController.modify_project_status(graph_id=self.task_id, status=2)
        else:
            ProjectController.modify_project_status(graph_id=self.task_id, status=3)

    def get_node(self):
        """
        fetch node from pool
        :return:
        """
        if len(self.node_pool) == 0:
            return False
        for node in self.node_pool:
            if node.indeg == 0:
                self.node_pool.remove(node)
                self.node_queue.put(node)
        return True

    def init_indeg(self):
        """
        initial indegree of each node
        :return:
        """
        try:
            for edge in self.edge_pool:
                if edge.source in self.node_dict and edge.target in self.node_dict:
                    self.node_dict[edge.target].indeg += 1
        except KeyError as e:
            ErrHandler.handle_err(e)

    def refresh_next(self, node):
        """
        update children node indegree
        :param node: object
        node object
        :return:
        """
        try:
            if node.status == 2:
                for edge in self.edge_pool:
                    if edge.source == node.id:
                        self.node_dict[edge.target].indeg -= 1
                        self.node_dict[edge.target].inpath.append(node.outpath)
        except KeyError as e:
            ErrHandler.handle_err(e)

    def consume_nodes(self):
        """
        take out nodes in queue and create a thread to run the node
        :return:
        """
        while not self.node_queue.empty():
            node_to_run = self.node_queue.get()
            t = threading.Thread(target=self.run_node, kwargs={'node_to_run': node_to_run})
            t.start()

    def run_node(self, node_to_run):
        """
        run the node
        :param node_to_run: object
        node object
        :return:
        """
        try:
            self._node_before_run_callback(node=node_to_run)
            node_to_run.run()
            self._node_succ_callback(node=node_to_run)
        except Exception as e:
            self._node_fail_callback(node=node_to_run)
            # self.task_running_flag = False

    def _get_all_children_node_ids(self, root_node_id, edges):
        """
        get children node ids used in 'run task from a specific node'
        :param root_node_id: str
        start node id
        :param edges: array
        edges array
        :return: array
        nodes_id_pool contains nodes id, these nodes are waiting to run
        """
        nodes_id_pool = []
        children_node_queue = queue.Queue()
        children_node_queue.put(root_node_id)
        while not children_node_queue.empty():
            node_id = children_node_queue.get()
            nodes_id_pool.append(node_id)
            for edge in edges:
                if edge['source'] == node_id:
                    children_node_queue.put(edge['target'])
        return nodes_id_pool

    def _node_before_run_callback(self, node):
        """
        callback before the node run
        :param node: object
        node object
        :return:
        """
        node.status = 1
        GraphController.modify_db_node_info(graph_id=self.task_id, node=node)

    def _node_succ_callback(self, node):
        """
        callback when the running is successful
        :param node: object
        node object
        :return:
        """
        self.refresh_next(node=node)
        GraphController.modify_db_node_info(graph_id=self.task_id, node=node)

    def _node_fail_callback(self, node):
        """
        callback when the running is fail
        :param node: object
        node object
        :return:
        """
        node.status = 3
        GraphController.modify_db_node_info(graph_id=self.task_id, node=node)
