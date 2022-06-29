from fastapi import FastAPI
from routers.users import router as _users
from routers.posts import router as _posts
from routers.auth import router as _auth
from routers.vote import router as _vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(_users)
app.include_router(_posts)
app.include_router(_auth)
app.include_router(_vote)


@app.get("/")
def index():
    return {"Message": "Hello World"}
