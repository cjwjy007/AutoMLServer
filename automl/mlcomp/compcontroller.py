import json

import os
import pandas as pd

from automl.errhandler.errhandler import ErrHandler
from automl.mldata.datacontroller import DataController
from filepath import resource_dir


class CompController:
    """
    this controller handle node configs and other details
    """

    def __init__(self):
        pass

    @staticmethod
    def get_data_names(graph_id, node_id):
        """
        get names of dataset which is connected to node
        :param graph_id: string
        ID of graph
        :param node_id: string
        ID of node
        :return: array
        list of data ids and names
        """
        try:
            father_node_names = []
            father_nodes = CompController._get_father_node_ids(graph_id, node_id)
            for node in father_nodes:
                data_info = {
                    'id': CompController._get_nearest_ancestor_data(graph_id, node).id,
                    'name': CompController._get_nearest_ancestor_data(graph_id, node).name
                }
                father_node_names.append(data_info)
            return father_node_names
        except Exception as e:
            ErrHandler().handle_err(e)

    @staticmethod
    def get_data_columns(graph_id, node_id):
        """
        get columns of dataset which is connected to node
        :param graph_id: string
        ID of graph
        :param node_id: string
        ID of node
        :return: array
        list of column names
        """
        try:
            node = CompController._get_nearest_ancestor_data(graph_id, node_id)
            if node:
                df = pd.read_csv(node.path, nrows=1)
                columns_list = df.columns.tolist()
                return columns_list
            return []
        except Exception as e:
            ErrHandler().handle_err(e)

    @staticmethod
    def get_data_columns_detail(graph_id, node_id, col_name):
        """
        get column description of dataset
        :param graph_id: string
        ID of graph
        :param node_id: string
        ID of node
        :param col_name: string
        column name of dataset
        :return: json
        json information of chosen column
        """
        try:
            node = CompController._get_nearest_ancestor_data(graph_id, node_id)
            if node:
                df = pd.read_csv(node.path, nrows=10000)
                col_info = df[col_name].describe().to_dict()
                # avoid int64 problems
                return eval(str(col_info))
        except Exception as e:
            ErrHandler().handle_err(e)

    @staticmethod
    def get_config(graph_id, node_id):
        """
        get config of node
        :param graph_id: string
        ID of graph
        :param node_id: string
        ID of node
        :return: json
        json-like config
        """
        with open(os.path.join(resource_dir, '{0}_config.json'.format(graph_id)), 'r') as file_object:
            try:
                json_config = json.load(file_object)
                if node_id in json_config:
                    ret = json_config[node_id]
                else:
                    ret = {}
                return ret
            except ValueError as e:
                ErrHandler().handle_err(e)
            except IOError as e:
                ErrHandler().handle_err(e)

    @staticmethod
    def set_config(graph_id, node_id, config):
        """
        set config of node
        :param graph_id: string
        ID of graph
        :param node_id: string
        ID of node
        :param config: json
        config of node
        :return: bool
        return if successfully set config
        """
        with open(os.path.join(resource_dir, '{0}_config.json'.format(graph_id)), 'r') as file_object:
            try:
                json_config = json.load(file_object)
                json_config[node_id] = config
            except ValueError as e:
                json_config = {node_id: config}
        with open(os.path.join(resource_dir, '{0}_config.json'.format(graph_id)), 'w') as file_object:
            try:
                file_object.write(json.dumps(json_config))
            except IOError as e:
                ErrHandler().handle_err(e)
            return True

    @staticmethod
    def _get_father_node_ids(graph_id, node_id):
        """
        get father node ids
        :param graph_id: string
        ID of graph
        :param node_id: string
        ID of node
        :return: array
        node ids array
        """
        try:
            with open(os.path.join(resource_dir, '{0}.json'.format(graph_id)), 'r') as graph:
                graph_json = json.load(graph)
            if graph_json:
                father_nodes = []
                edges = graph_json.get('source').get('edges')
                cur_node_id = node_id
                for edge in edges:
                    if edge.get('target') == cur_node_id:
                        father_nodes.append(edge.get('source'))
                return father_nodes
            return []
        except Exception as e:
            ErrHandler().handle_err(e)

    @staticmethod
    def _get_nearest_ancestor_data(graph_id, node_id):
        """
        get nearest ancestor dataset node, then return the dataset path
        :param graph_id: string
        ID of graph
        :param node_id: string
        ID of node
        :return: Node
        dataset node object
        """
        try:
            with open(os.path.join(resource_dir, '{0}.json'.format(graph_id)), 'r') as graph:
                graph_json = json.load(graph)
            with open(os.path.join(resource_dir, '{0}_config.json'.format(graph_id)), 'r') as config:
                config_json = json.load(config)
            if graph_json and config_json:
                nodes = graph_json.get('source').get('nodes')
                node_type_dict = {node['id']: node['type'] for node in nodes}
                edges = graph_json.get('source').get('edges')
                cur_node_id = node_id
                model_found = False
                while True:
                    flag = False
                    if node_type_dict[cur_node_id] == 'model':
                        model_found = True
                        break
                    for edge in edges:
                        if edge.get('target') == cur_node_id:
                            flag = True
                            cur_node_id = edge.get('source')
                    if not flag:
                        break
                if model_found:
                    if cur_node_id in config_json and 'dataId' in config_json[cur_node_id]:
                        data_id = config_json[cur_node_id]['dataId']
                        return DataController.get_data_by_id(id=data_id)
                else:
                    return None
        except Exception as e:
            ErrHandler().handle_err(e)
