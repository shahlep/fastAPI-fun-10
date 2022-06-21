from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models as _models, schemas as _schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: _schemas.UserLogin, db: Session = Depends(get_db)):
    user = (
        db.query(_models.User)
        .filter(_models.User.email == user_credentials.email)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials!"
        )
