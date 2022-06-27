from fastapi import APIRouter, Depends, status, HTTPException, Response
import schemas as _schemas, models as _models, oauth2
from sqlalchemy.orm import Session
from database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=_schemas.ShowPost)
def create_posts(
    post: _schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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
    new_post = _models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#@router.get("/", response_model=List[_schemas.ShowPost])
@router.get("/")
def get_all_posts(
    limit: int = None,
    search: Optional[str] = "",
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = (
        db.query(_models.Post)
        .filter(_models.Post.title.contains(search))
        .limit(limit)
        .all()
    )
    results = (
        db.query(_models.Post, func.count(_models.Vote.post_id).label("votes"))
        .join(_models.Vote, _models.Post.id == _models.Vote.post_id, isouter=True)
        .group_by(_models.Post.id).all()
    )
    print(results)
    return posts


@router.get("/latest", response_model=_schemas.ShowPost)
def get_latest_post(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    # post = my_posts[len(my_posts) - 1]
    post = db.query(_models.Post).order_by(_models.Post.id.desc())
    return post


@router.get("/{id}", response_model=_schemas.ShowPost)
def get_posts_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(_models.Post).filter(_models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(_models.Post).filter(_models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Yor are not allowed to delete the post!",
        )

    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=_schemas.ShowPost)
def update_post(
    id: int,
    updated_post: _schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #   """UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
    #  (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(_models.Post).filter(_models.Post.id == id).first()
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} doesn't exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Yor are not allowed to delete the post!",
        )
    post_query.update(updated_post.dict())
    db.commit()
    return post_query.first()
