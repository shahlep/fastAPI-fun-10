from fastapi.testclient import TestClient
from main import app
from config.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from pytest import fixture
from oauth2 import create_access_token
import models


SQLALCHEMY_DATABASE_URL = Settings.TEST_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Test_SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency


@fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@fixture(scope="function")
def test_user(client):
    user_data = {
        "email": "test123@example.com",
        "password": "password123",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@fixture(scope="function")
def test_user2(client):
    user_data = {
        "email": "test124@example.com",
        "password": "password123",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@fixture(scope="function")
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@fixture(scope="function")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"bearer {token}",
    }
    return client


@fixture(scope="function")
def test_posts(test_user, session,test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user["id"],
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user["id"],
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    # map to post model
    post_map = map(create_post_model, posts_data)

    # to list
    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()

    return posts
