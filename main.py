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
    post_dict['id']= randrange(0,1000)
    my_posts.append(post_dict)
    return {"new_post": my_posts}
