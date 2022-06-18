from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = []


@app.get("/")
def index():
    return {"Message": "Hello World"}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000)
    my_posts.append(post_dict)
    return {"new_post": my_posts}

@app.get("/posts")
def get_all_posts():
    return {"Posts": my_posts}

def get_posts(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/posts/{id}")
def get_posts_by_id(id: int):
    post = get_posts(id)
    return {"Posts": post}
