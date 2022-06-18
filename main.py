from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def index():
    return {"Message": "Hello World"}


@app.post("/create_posts")
def create_posts(post: Post):
    print(post)
    return {"new_post": f"{post.content}"}
