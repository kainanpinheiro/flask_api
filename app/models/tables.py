from app.main import db


class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name
