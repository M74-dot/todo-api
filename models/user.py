from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # todorel = db.relationship(
    #     'TodoModel', backref='user', lazy=True
    # )
    todos = db.relationship(
        'TodoModel', backref='user', lazy=True
    )
