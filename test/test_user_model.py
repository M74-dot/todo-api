import unittest.mock as mock
from models.user import UserModel
from app import db


class MockUserModel:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.todos = db.relationship(
            'TodoModel', back_populates='user', lazy="dynamic"
        ).append([])


def test_user_model():
    with mock.patch('models.user.UserModel', new=MockUserModel):
        user = UserModel(id=1, username='test_user', password='test_password')
        assert user.id == 1
        assert user.username == 'test_user'
        assert user.password == 'test_password'
        assert isinstance(user.todos, list)
