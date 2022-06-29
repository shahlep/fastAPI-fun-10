from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World"}


def test_create_user():
    response = client.post("/users/",json={"email":"test123@example.com",
                                           "password":"password123"})
    assert response.status_code ==201
    assert response.json().get("email") == "test123@example.com"

