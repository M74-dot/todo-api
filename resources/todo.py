from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import TodoSchema, TodoUpdateSchema
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from db import db
from models import TodoModel

blp = Blueprint("todos", __name__, description="Operations on todo")


@blp.route('/')
class TodoHome(MethodView):
    def get(self):
        return 'Welcome To TODO APP!'


@blp.route('/todo')
class TodoList(MethodView):
    @jwt_required()
    @blp.response(200, TodoSchema(many=True))
    def get(self):
        return TodoModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(TodoSchema)
    @blp.response(201, TodoSchema)
    def post(self, todo_data):
        todo = TodoModel(**todo_data)
        try:
            db.session.add(todo)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A Task with that Title already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return todo


@blp.route('/todo/<int:todo_id>')
class TodoUpdate(MethodView):
    @jwt_required()
    @blp.arguments(TodoUpdateSchema)
    def put(self, todo_data, todo_id):
        todo = TodoModel.query.get(todo_id)
        if todo:
            todo.title = todo_data["title"]
            todo.status = todo_data["status"]
        else:
            todo = TodoModel(id=todo_id, **todo_data)

        db.session.add(todo)
        db.session.commit()

        return {"message": "Updated successfully"}

    @jwt_required()
    def delete(self, todo_id):
        todo = TodoModel.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return {"message": "Task deleted."}
