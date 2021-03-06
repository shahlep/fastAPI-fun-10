from jose import jwt, JWTError
from datetime import datetime, timedelta
from config.settings import Settings
import schemas as _schemas, models as _models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=Settings.ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = _schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Failed to validate the credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(_models.User).filter(_models.User.id == token.id).first()
    return user
