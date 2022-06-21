from fastapi import APIRouter, Depends, status, HTTPException, Response
import schemas as _schemas, models as _models
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter(
    prefix="/posts"
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=_schemas.ShowPost
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


@router.get("/", response_model=List[_schemas.ShowPost])
def get_all_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(_models.Post).all()
    return posts


@router.get("/latest", response_model=_schemas.ShowPost)
def get_latest_post(db: Session = Depends(get_db)):
    # post = my_posts[len(my_posts) - 1]
    post = db.query(_models.Post).order_by(_models.Post.id.desc())
    return post


@router.get("/{id}", response_model=_schemas.ShowPost)
def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(_models.Post).filter(_models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=_schemas.ShowPost)
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
