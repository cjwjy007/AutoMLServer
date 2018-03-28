import json

import os
import pandas as pd
from flask import send_file

from automl import db
from automl.errhandler.errhandler import ErrHandler
from automl.mlgraph.graphmodel import GraphNode
from automl.mlproject.projectcontroller import ProjectController
from filepath import resource_dir


class GraphController:
    """
    GraphController
    """
    def __init__(self):
        pass

    @staticmethod
    def get_graph(graph_id):
        """
        get json-like graph from .json file
        :param graph_id: str
        ID of graph
        :return: json
        json-like graph
        """
        with open(os.path.join(resource_dir, '{0}.json'.format(graph_id)), 'r') as file_object:
            try:
                ret = json.load(file_object)
                return ret
            except IOError as e:
                ErrHandler().handle_err(e)
            except ValueError as e:
                ErrHandler().handle_err(e)

    @staticmethod
    def save_graph(graph_id, data):
        """
        save json-like graph to .json file
        :param graph_id: str
        ID of graph
        :param data: object
        data of graph
        :return: bool
        return if saving is successful
        """
        js_obj = json.dumps(data)
        with open(os.path.join(resource_dir, '{0}.json'.format(graph_id)), 'w') as file_object:
            try:
                file_object.write(js_obj)
            except IOError as e:
                ErrHandler().handle_err(e)
            ProjectController.modify_db_update_time(graph_id=graph_id)
            return True

    @staticmethod
    def get_nodes_status(graph_id):
        """
        get status of all nodes in graph, this function is used to refresh node colors in client
        :param graph_id: str
        ID of graph
        :return: array
        return node status array
        """
        status_arr = []
        try:
            nodes = GraphNode.query.filter_by(graph_id=graph_id).all()
            for node in nodes:
                status_info = {
                    'node_id': node.node_id,
                    'node_status': node.status
                }
                status_arr.append(status_info)
            return status_arr
        except Exception as e:
            ErrHandler().handle_err(e)


    @staticmethod
    def insert_db_node_info(graph_id, node):
        """
        insert node information to database, doing this before running a task
        :param graph_id: str
        ID of graph
        :param node: object
        node object
        node object(inherits BaseNode)
        :return: bool
        return if success
        """
        try:
            if GraphNode.query.filter_by(node_id=node.id, graph_id=graph_id).first():
                GraphController.modify_db_node_info(graph_id=graph_id, node=node)
            else:
                node_id = node.id
                status = 0
                type = node.type
                desc = node.desc
                inpath = str(node.inpath)
                outpath = node.outpath
                config = str(node.config)
                graph_node = GraphNode(graph_id, node_id, status, type, desc, inpath, outpath, config)
                db.session.add(graph_node)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            ErrHandler().handle_err(e)
        return True

    @staticmethod
    def modify_db_node_info(graph_id, node):
        """
        modify node information in database
        :param graph_id: str
        ID of graph
        :param node: object
        node object
        node object(inherits BaseNode)
        :return: bool
        return if success
        """
        try:
            graph_node = GraphNode.query.filter_by(node_id=node.id, graph_id=graph_id).first()
            if graph_node:
                graph_node.status = node.status
                graph_node.type = node.type
                graph_node.desc = node.desc
                graph_node.inpath = str(node.inpath)
                graph_node.outpath = node.outpath
                graph_node.config = str(node.config)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            ErrHandler().handle_err(e)
        return True

    @staticmethod
    def delete_db_node_info(graph_id, node_id=None):
        """
        delete node information in database
        :param graph_id: str
        ID of graph
        :param node_id: str or None
        Id of node. All nodes will be deleted if node_id not given
        :return: bool
        return if success
        """
        try:
            if node_id is None:
                graph_nodes = GraphNode.query.filter_by(graph_id=graph_id).all()
                for gn in graph_nodes:
                    db.session.delete(gn)
                db.session.commit()
            else:
                graph_node = GraphNode.query.filter_by(graph_id=graph_id, node_id=node_id).first()
                if graph_node:
                    db.session.delete(graph_node)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            ErrHandler().handle_err(e)
        return True

    @staticmethod
    def get_inpath_by_node(graph_id, node_id):
        """
        get input path by graph_id and node_id
        :param graph_id: str
        ID of graph
        :param node_id: str
        ID of node
        :return: list
        return input path list
        """
        try:
            graph_node = GraphNode.query.filter_by(node_id=node_id, graph_id=graph_id).first()
            if graph_node:
                return list(eval(graph_node.inpath))
        except Exception as e:
            ErrHandler().handle_err(e)

    @staticmethod
    def get_data_output_preview_by_node(graph_id, node_id):
        """
        dump node output and display in client
        :param graph_id: str
        ID of graph
        :param node_id: str
        ID of node
        :return: json
        return node output json data
        """
        try:
            graph_node = GraphNode.query.filter_by(node_id=node_id, graph_id=graph_id).first()
            if graph_node:
                path = graph_node.outpath
                if path and path.split('.')[-1] == 'csv':
                    return pd.read_csv(path, nrows=50).to_json()
                elif path and path.split('.')[-1] == 'model':
                    split_path = path.split('.')
                    split_path[-1] = 'csv'
                    csv_path = '.'.join(split_path)
                    return pd.read_csv(csv_path, nrows=5).to_json()

        except Exception as e:
            ErrHandler().handle_err(e)

    @staticmethod
    def download_data_output_by_node(graph_id, node_id):
        """
        download node output file
        :param graph_id: str
        ID of graph
        :param node_id: str
        ID of node
        :return: File Stream Response
        return node output download stream
        """
        try:
            graph_node = GraphNode.query.filter_by(node_id=node_id, graph_id=graph_id).first()
            if graph_node and graph_node.outpath:
                return send_file(graph_node.outpath)
        except Exception as e:
            ErrHandler().handle_err(e)
