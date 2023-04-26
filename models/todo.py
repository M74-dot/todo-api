from db import db


class TodoModel(db.Model):
    __tablename__ = "todos"

    todo_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("UserModel", back_populates="todorel")