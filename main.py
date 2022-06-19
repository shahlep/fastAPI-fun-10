from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at:str


my_posts = [
    {"title": "test title", "content": "test content", "published": False, "id": 1},
    {"title": "test title2", "content": "test content2", "published": False, "id": 2},
]


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


def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}


@app.get("/posts/{id}")
def get_posts_by_id(id: int, response: Response):
    post = get_posts(id)
    if post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )
    return {"Posts": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_index_post(id)
    if post_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )
    my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
