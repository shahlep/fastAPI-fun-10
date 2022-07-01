from fastapi.testclient import TestClient
from main import app
from config.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from pytest import fixture


SQLALCHEMY_DATABASE_URL = Settings.TEST_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Test_SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency


@fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
