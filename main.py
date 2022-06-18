from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
def index():
    return {"Message": "Hello World"}


@app.post("/create_posts")
def create_posts(post:Post):
    print(post)
    return {"new_post": f"{post.content}"}
