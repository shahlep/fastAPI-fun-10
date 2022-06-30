from fastapi.testclient import TestClient
from main import app
from schemas import ShowUser
from config.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db,Base


SQLALCHEMY_DATABASE_URL = Settings.TEST_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Test_SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)

# Dependency
def override_get_db():
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World"}


def test_create_user():
    response = client.post(
        "/users/", json={"email": "test123@example.com", "password": "password123"}
    )
    new_user = ShowUser(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test123@example.com"
