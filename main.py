from fastapi import FastAPI, Response, status, HTTPException, Depends
import schemas as _schemas, models as _models
from config.settings import Settings
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine, get_db
from sqlalchemy.orm import Session


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


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: _schemas.Post, db: Session = Depends(get_db)):
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
    return {"new_post": new_post}


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(_models.Post).all()
    return {"Posts": posts}


@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    # post = my_posts[len(my_posts) - 1]
    post = db.query(_models.Post).order_by(_models.Post.id.desc())
    return {"detail": post}


@app.get("/posts/{id}")
def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(_models.Post).filter(_models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )
    return {"Posts": post}


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


@app.put("/posts/{id}")
def update_post(id: int, updated_post: _schemas.Post, db: Session = Depends(get_db)):
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
    return {"Updated Post": post_query.first()}


@app.get("/sqlalchemy")
def test_sql_alchemy_db_conn(db: Session = Depends(get_db)):
    posts = db.query(_models.Post).all()
    return {"status": posts}
