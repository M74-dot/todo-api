from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import TodoSchema, TodoUpdateSchema
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from db import db
from models import TodoModel, UserModel

blp = Blueprint("todos", __name__, description="Operations on todo")


@blp.route('/')
class TodoHome(MethodView):
    def get(self):
        return 'Welcome To TODO APP!'


@blp.route('/user/<int:user_id>/todo')
class TodoList(MethodView):
    # List task
    # @jwt_required()
    @blp.response(200, TodoSchema(many=True))
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        # todo_list = [todo for todo in user.todorel]
        todo_list = [todo for todo in user.todos]
        return todo_list, 200

    # Add task
    # @jwt_required(fresh=True)
    @blp.arguments(TodoSchema)
    @blp.response(201, TodoSchema)
    def post(self, todo_data, user_id):
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


@blp.route('/user/<int:user_id>/todo/<int:todo_id>')
class TodoUpdate(MethodView):
    @jwt_required()
    @blp.arguments(TodoUpdateSchema)
    def put(self, todo_data, todo_id, user_id):
        user = UserModel.query.get_or_404(user_id)
        todo = TodoModel.query.filter_by(id=todo_id, user=user).first_or_404()
        if todo:
            todo.title = todo_data["title"]
            todo.status = todo_data["status"]
        else:
            todo = TodoModel(id=todo_id, **todo_data)

        db.session.add(todo)
        db.session.commit()

        return {"message": "Task Updated successfully"}

    # @jwt_required()
    def delete(self, todo_id, user_id):
        user = UserModel.query.get_or_404(user_id)
        todo = TodoModel.query.filter_by(
            todo_id=todo_id, user=user
        ).first_or_404()
        db.session.delete(todo)
        db.session.commit()
        return {"message": "Task deleted."}
