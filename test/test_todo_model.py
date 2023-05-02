import unittest.mock as mock
from models.todo import TodoModel
from models.user import UserModel


class MockTodoModel:
    def __init__(self, todo_id, title, status, user_id, user):
        self.todo_id = todo_id
        self.title = title
        self.status = status
        self.user_id = user_id
        self.user = user


def test_todo_model():
    with mock.patch('models.todo.TodoModel', new=MockTodoModel):
        todo = TodoModel(
            todo_id=1,
            title='Test Todo',
            status='Incomplete',
            user_id=1,
            user=UserModel())
        assert todo.todo_id == 1
        assert todo.title == 'Test Todo'
        assert todo.status == 'Incomplete'
        assert todo.user_id == 1
        assert isinstance(todo.user, UserModel)
