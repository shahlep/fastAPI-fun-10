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
    vote_query =db.query(_models.Vote).filter(
        _models.Vote.post_id==vote.post_id,_models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        pass
    else:
        pass
