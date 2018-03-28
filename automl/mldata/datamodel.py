from automl import db


class DataSet(db.Model):
    __tablename__ = 'dataset'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    path = db.Column(db.String(100))
    desc = db.Column(db.String(200))
    create_time = db.Column(db.String(30))

    def __init__(self, name, path, desc, create_time):
        self.name = name
        self.path = path
        self.desc = desc
        self.create_time = create_time


