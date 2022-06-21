from fastapi import FastAPI, Response, status, HTTPException, Depends
import schemas as _schemas, models as _models
from config.settings import Settings
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
import utils


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


try:
    conn = psycopg2.connect(
        host=Settings.POSTGRESS_SERVER,
        database=Settings.POSTGRESS_DB,
        user=Settings.POSTGRESS_USER,
        password=Settings.POSTGRESS_PASSWORD,
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("connection to database was successful")
except Exception as error:
    print("connection was failed.")
    print("Error: ", error)

my_posts = [
    {"title": "test title", "content": "test content", "published": False, "id": 1},
    {"title": "test title2", "content": "test content2", "published": False, "id": 2},
]


@app.get("/")
def index():
    return {"Message": "Hello World"}


