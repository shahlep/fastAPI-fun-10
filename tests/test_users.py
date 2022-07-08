from schemas import ShowUser, Token
from jose import jwt
from config.settings import Settings
from pytest import mark


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


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_response = Token(**response.json())
    payload = jwt.decode(
        login_response.access_token, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@mark.parametrize(
    "email,password,status_code",
    [
        ("wrong@exmplae.com", "password123", 403),
        ("test123@example.com", "wrongpassowrd", 403),
        ("wrong@example.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("test123@example.com", None, 422),
        (None, None, 422),
    ],
)
def test_incorrect_login_user(client, email, password, status_code):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
    )

    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid Credentials!"


def test_get_all_user(authorized_client):
    response = authorized_client.get("/users/")

    assert response.status_code == 200

def test_get_user_by_id(authorized_client):
    response = authorized_client.get(f"/users/1")

    assert response.status_code == 200
