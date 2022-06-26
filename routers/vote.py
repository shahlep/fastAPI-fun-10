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
    if vote.dir == 1:
        pass
    else:
        pass
