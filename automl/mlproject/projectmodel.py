from automl import db


class Project(db.Model):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20))
    graph_id = db.Column(db.String(20), unique=True)
    status = db.Column(db.Integer)
    create_time = db.Column(db.String(30))
    update_time = db.Column(db.String(30))

    def __init__(self, project_name, graph_id, status, create_time, update_time):
        self.project_name = project_name
        self.graph_id = graph_id
        self.status = status
        self.create_time = create_time
        self.update_time = update_time
