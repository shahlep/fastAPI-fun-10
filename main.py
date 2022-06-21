from fastapi import FastAPI
from config.settings import Settings
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine
from routers.users import router as _users
from routers.posts import router as _posts


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


@app.get("/")
def index():
    return {"Message": "Hello World"}
