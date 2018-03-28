class TaskEdge:
    """
    this class is used to build edge data structure, but is temporary not in further use
    """

    def __init__(self, edge):
        self.id = edge['id']
        self.source = edge['source']
        self.target = edge['target']
