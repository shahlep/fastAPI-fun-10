from fastapi import FastAPI, Response, status, HTTPException, Depends
import schemas as _schemas, models as _models
from config.settings import Settings
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
import utils


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

my_posts = [
    {"title": "test title", "content": "test content", "published": False, "id": 1},
    {"title": "test title2", "content": "test content2", "published": False, "id": 2},
]


@app.get("/")
def index():
    return {"Message": "Hello World"}


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=_schemas.ShowPost
)
def create_posts(post: _schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #   """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #   (
    #      post.title,
    #     post.content,
    #     post.published,
    # ),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = _models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_model=List[_schemas.ShowPost])
def get_all_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(_models.Post).all()
    return posts


@app.get("/posts/latest", response_model=_schemas.ShowPost)
def get_latest_post(db: Session = Depends(get_db)):
    # post = my_posts[len(my_posts) - 1]
    post = db.query(_models.Post).order_by(_models.Post.id.desc())
    return post


@app.get("/posts/{id}", response_model=_schemas.ShowPost)
def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(_models.Post).filter(_models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(_models.Post).filter(_models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )

    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=_schemas.ShowPost)
def update_post(
    id: int, updated_post: _schemas.PostCreate, db: Session = Depends(get_db)
):
    # cursor.execute(
    #   """UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    #  (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(_models.Post).filter(_models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )
    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first()


@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=_schemas.ShowUser
)
def create_user(user: _schemas.UserCreate, db: Session = Depends(get_db)):
    # hashing a password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = _models.User(**user.dict())
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}",response_model=_schemas.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(_models.User).filter(_models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found"
        )
    return user
