from jose import jwt, JWTError
from datetime import datetime, timedelta
from config.settings import Settings
import schemas as _schemas


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,Settings.SECRET_KEY,algorithms=Settings.ALGORITHM)
        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = _schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
