from datetime import datetime
from app import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.String(500))
    deadline = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    completed_time = db.Column(db.DateTime)
    utc_offset = db.Column(db.Integer)

    def __repr__(self):
        return self.text

    def completed_todo(self):
        self.completed = True
        self.completed_time = datetime.utcnow()

    def no_complited_todo(self):
        self.completed = False
        self.completed_time = None
