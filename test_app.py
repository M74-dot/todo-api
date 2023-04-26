from app import app, db
import json
import pytest
from models import TodoModel, UserModel
from passlib.hash import pbkdf2_sha256


@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope="module")
def access_token(test_client):
    user = UserModel(
        username="testuser",
        password=pbkdf2_sha256.hash("testpassword")
    )
    db.session.add(user)
    db.session.commit()
    response = test_client.post(
        "/login", data=json.dumps(
            {"username": "testuser", "password": "testpassword"}
        ), content_type="application/json"
    )
    access_token = response.json["access_token"]
    return access_token


# def test_todo_home(test_client):
#     response = test_client.get("/")
#     assert response.status_code == 200
#     assert response.data == b"Welcome To TODO APP!"


def test_get_todos(test_client, access_token):
    user = UserModel(username="testuser", password="testpassword")
    db.session.add(user)

    todo = TodoModel(title="test todo", status="not done", user=user)
    db.session.add(todo)
    db.session.commit()

    response = test_client.get(
        f"/user/{user.id}/todo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json == [
        {
            "id": todo.id,
            "title": "test todo",
            "status": "not done",
            "user_id": user.id
        }
    ]


# def test_create_todo_with_existing_title(test_client, access_token):
#     user = UserModel(username="testuser")
#     db.session.add(user)
#     db.session.commit()

#     todo = TodoModel(title="test todo", user=user)
#     db.session.add(todo)
#     db.session.commit()

#     response = test_client.post(
#         f"/user/{user.id}/todo",
#         data=json.dumps({"title": "test todo", "status": "Incomplete"}),
#         content_type="application/json",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 400
#     assert response.json["message"] == "A Task with that Title already exists."


# def test_create_todo_successfully(test_client, access_token):
#     user = UserModel(username="testuser")
#     db.session.add(user)
#     db.session.commit()

#     response = test_client.post(
#         f"/user/{user.id}/todo",
#         data=json.dumps({"title": "test todo", "status": "Incomplete"}),
#         content_type="application/json",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 201
#     assert response.json["title"] == "test todo"
#     assert response.json["status"] == "Incomplete"
#     assert response.json["user_id"] == user.id


# def test_update_todo_successfully(test_client, access_token):
#     user = UserModel(username="testuser")
#     db.session.add(user)
#     db.session.commit()

#     todo = TodoModel(title="test todo", user=user)
#     db.session.add(todo)
#     db.session.commit()

#     response = test_client.put(
#         f"/user/{user.id}/todo/{todo.id}",
#         data=json.dumps({"title": "updated todo", "status": "Completed"}),
#         content_type="application/json",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     assert response.status_code == 200
#     assert response