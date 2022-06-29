from fastapi import APIRouter, HTTPException, status, Depends
import models as _models, schemas as _schemas, oauth2
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: _schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(_models.Post).filter(_models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {vote.post_id} doesn't exist",
        )
    vote_query = db.query(_models.Vote).filter(
        _models.Vote.post_id == vote.post_id,
        _models.Vote.user_id == current_user.id,
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user with id:{current_user.id} already voted for post",
            )
        new_vote = _models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Vote added"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exist"
            )
        vote_query.delete()
        db.commit()
        return {"Message": "Vote deleted"}
