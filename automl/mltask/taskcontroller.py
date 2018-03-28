from automl import celery
from automl.mltask.task import Task


class TaskController:
    """
    TaskController put the task to background(using celery)
    """

    def __init__(self):
        pass

    @staticmethod
    @celery.task
    def run_task(graph_id):
        """
        running a task
        :param graph_id: str
        ID of graph
        :return: bool
        return if success
        """
        task = Task(graph_id=graph_id)
        task.run_task()
        return True

    @staticmethod
    @celery.task
    def run_task_from_node(graph_id, node_id):
        """
        running a task from a node
        :param graph_id: str
        ID of graph
        :param node_id: str
        ID of node
        :return: bool
        return if success
        """
        task = Task(graph_id=graph_id, start_node_id=node_id)
        task.run_task()
        return True
