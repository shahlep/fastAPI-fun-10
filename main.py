from fastapi import FastAPI
import models
from database import engine
from routers.users import router as _users
from routers.posts import router as _posts
from routers.auth import router as _auth
from config.settings import Settings

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(_users)
app.include_router(_posts)
app.include_router(_auth)


@app.get("/")
def index():
    return {"Message": "Hello World"}
