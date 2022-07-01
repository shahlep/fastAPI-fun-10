from schemas import ShowUser
from .database import client, session
from pytest import fixture


@fixture(scope="function")
def test_user(client):
    user_data = {
        "email": "test123@example.com",
        "password": "password123",
    }
    response = client.post("/users/",json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World"}


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "test123@example.com", "password": "password123"}
    )
    new_user = ShowUser(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test123@example.com"


def test_login_user(client,test_user):
    response = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    assert response.status_code == 200
