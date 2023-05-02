import pytest
from app import app
from unittest.mock import MagicMock, patch, Mock
from models.user import UserModel
from models.todo import TodoModel
from resources.todo import TodoList


@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client


def test_todo_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Welcome To TODO APP!"


def test_get_todo_list(client, mocker):
    mock_user_model = mocker.Mock(spec=UserModel)
    mock_user_model.id = 1
    mock_user_model.username = 'testuser'
    mock_user_model.todos.all.return_value = [
        MagicMock(
            todo_id=1,
            title='Reading Book',
            status='Not Done',
            user=mock_user_model
        )
    ]
    mocker.patch('models.user.UserModel', return_value=mock_user_model)

    with app.app_context():
        mock_token = "mock_jwt_token"
        headers = {'Authorization': f'Bearer {mock_token}'}
        response = client.get('/user/1/todo', headers=headers)

        assert mock_user_model.id == 1
        assert mock_user_model.username == 'testuser'
        assert len(mock_user_model.todos.all()) == 1

        assert response.status_code == 200
        assert len(response.json) == 1


def test_get_todos(client):
    with patch('models.user.UserModel.query') as query_mock:
        user_mock = Mock()
        user_mock.todos = [Mock(), Mock()]
        query_mock.get_or_404.return_value = user_mock

        with app.app_context():
            response = client.get('/user/1/todo')
            assert response.status_code == 200
            assert len(response.json) == 2


def test_post_todo_success():
    with app.app_context():
        with patch("models.todo.TodoModel") as mock_todo_model:
            mock_todo = mock_todo_model.return_value
            mock_todo.id = 1
            mock_todo.title = "Test Todo"
            mock_todo.status = "Incomplete"
            mock_todo.user_id = 1

            with patch("app.db.session.add") as mock_add:
                with patch("app.db.session.commit") as mock_commit:
                    response = TodoList.post(
                        TodoList(),
                        todo_data={
                            "title": "Test Todo", "status": "Incomplete"
                        },
                        user_id=1
                    )
                    assert response == {
                        "todo_id": 1,
                        "title": "Test Todo",
                        "status": "Incomplete",
                        "user": 1
                    }
                    mock_add.assert_called_once_with(mock_todo)
                    mock_commit.assert_called_once()
   