from fastapi import FastAPI
import models
from database import engine
from routers.users import router as _users
from routers.posts import router as _posts


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(_users)
app.include_router(_posts)

@app.get("/")
def index():
    return {"Message": "Hello World"}
