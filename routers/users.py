from fastapi import APIRouter, status, HTTPException, Depends
import schemas as _schemas, models as _models, utils
from sqlalchemy.orm import Session
from database import get_db
from typing import List

router = APIRouter(prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=_schemas.ShowUser)
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


@router.get("/", response_model=List[_schemas.ShowUser])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(_models.User).all()
    return users


@router.get("/{id}", response_model=_schemas.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(_models.User).filter(_models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found"
        )
    return user
