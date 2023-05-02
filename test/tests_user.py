from unittest.mock import MagicMock, patch
from flask import Flask
from resources.user import UserRegister, UserLogin
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token


def test_user_register_post_success():
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    app = Flask(__name__)
    with app.test_request_context('/register', json=user_data, method='POST'):
        with patch('models.user.UserModel.query.filter') as mock_query_filter:
            with patch('models.user.UserModel') as mock_user_model:
                with patch('app.db.session.add') as mock_add:
                    with patch('app.db.session.commit') as mock_commit:
                        mock_query_filter.return_value.first.return_value = None
                        UserRegister().post(user_data=user_data)
                        mock_user_model.assert_called_once_with(
                            username=user_data["username"],
                            password=pbkdf2_sha256.hash(user_data["password"]),
                        )
                        mock_add.assert_called_once()
                        mock_commit.assert_called_once()


def test_user_login_post_success():
    # creating mock UserModel instance
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.username = "test_user"
    mock_user.password = pbkdf2_sha256.hash("test_password")

    # creating a mock UserSchema instance
    mock_schema = MagicMock()
    mock_schema.load.return_value = {
        "username": mock_user.username,
        "password": "test_password",
    }

    # creating a mock JWTManager instance
    mock_jwt_manager = MagicMock()
    mock_jwt_manager.create_access_token.return_value = create_access_token(
        identity=mock_user.id, fresh=True
    )
    mock_jwt_manager.create_refresh_token.return_value = create_refresh_token(
        mock_user.id
    )

    # mock UserModel query
    mock_query = MagicMock()
    mock_query.filter.return_value.first.return_value = mock_user

    # mock db.session object
    mock_session = MagicMock()
    mock_session.__enter__.return_value.query.return_value = mock_query

    # mock db object
    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    # mock Flask app instance
    mock_app = MagicMock()
    mock_app.config = {}

    # UserLogin instance
    user_login = UserLogin()
    user_login.db = mock_db
    user_login.jwt = mock_jwt_manager
    user_login.schema = mock_schema

    # Call the post method with a mock request context
    with patch("flask.request") as mock_request:
        mock_request.json = {
            "username": mock_user.username,
            "password": "test_password",
        }
        response, status_code = user_login.post()

    # Check that the JWTManager methods were called correctly
    mock_jwt_manager.create_access_token.assert_called_once_with(
        identity=mock_user.id, fresh=True
    )
    mock_jwt_manager.create_refresh_token.assert_called_once_with(mock_user.id)

    # Check that the response and status code are correct
    expected_response = {
        "access_token": mock_jwt_manager.create_access_token.return_value,
        "refresh_token": mock_jwt_manager.create_refresh_token.return_value,
    }
    assert response == expected_response
    assert status_code == 200
