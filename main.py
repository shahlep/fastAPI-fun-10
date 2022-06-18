from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def index():
    return {"Message": "Hello World"}


@app.post("/create_posts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"Title: {payload['title']} Content: {payload['content']}"}
