import os
from unittest.mock import MagicMock
from app import (
    app,
    token_not_fresh_callback,
    revoked_token_callback,
    expired_token_callback,
    invalid_token_callback,
    missing_token_callback
)


def test_api_title():
    assert app.config['API_TITLE'] == 'TODO REST API'


def test_db_exists():
    with app.app_context():
        assert os.path.exists('instance/db.sqlite')


def test_token_not_fresh_callback():
    with app.test_request_context():
        jwt_header = {}
        jwt_payload = {}
        response = token_not_fresh_callback(jwt_header, jwt_payload)
        assert response[1] == 401
        assert response[1] != 200
        assert response[0].json == {
            "description": "The token is not fresh.",
            "error": "fresh_token_required"
        }
        assert response[0].json != {"error": "fresh_token_required"}


def test_revoked_token_callback():
    with app.test_request_context():
        jwt_header = {"abc": "HSEDSNC"}
        jwt_payload = {"jti": "1234"}
        response = revoked_token_callback(jwt_header, jwt_payload)
        assert response[1] == 401
        assert response[1] != 200
        assert response[0].json == {
            "description": "The token has been revoked.",
            "error": "token_revoked"
        }
        assert b"The token has been revoked." in response[0].data


def test_expired_token_callback():
    with app.test_request_context():
        jwt_header = {"abc": "HSEDSNC"}
        jwt_payload = {"exp": 0}
        response = expired_token_callback(jwt_header, jwt_payload)
        assert response[1] == 401
        assert response[1] != 200
        assert response[0].json == {
            "message": "The token has expired.",
            "error": "token_expired"
        }


def test_invalid_token_callback():
    with app.test_request_context():
        error = MagicMock()
        error.message = "Signature verification failed"
        response = invalid_token_callback(error)
        assert response[1] == 401
        assert response[1] != 200
        assert b"Signature verification failed" in response[0].data


def test_missing_token_callback():
    with app.test_request_context():
        error = MagicMock()
        error.message = "Request does not contain an access token."
        response = missing_token_callback(error)
        assert response[1] == 401
        assert response[1] != 200
        assert b"Request does not contain an access token." in response[0].data
