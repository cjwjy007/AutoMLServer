from automl import db


class GraphNode(db.Model):
    __tablename__ = 'graphnode'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    graph_id = db.Column(db.String(20))
    node_id = db.Column(db.String(20))
    status = db.Column(db.Integer)
    type = db.Column(db.String(50))
    desc = db.Column(db.String(50))
    inpath = db.Column(db.String(500))
    outpath = db.Column(db.String(500))
    config = db.Column(db.String(500))

    def __init__(self, graph_id, node_id, status, type, desc, inpath, outpath, config):
        self.graph_id = graph_id
        self.node_id = node_id
        self.status = status
        self.type = type
        self.desc = desc
        self.inpath = inpath
        self.outpath = outpath
        self.config = config