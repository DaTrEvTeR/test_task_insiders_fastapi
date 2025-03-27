import jwt
import datetime
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from app.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(minutes=settings.JWT__ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT__SECRET_KEY, algorithm=settings.JWT__ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT__SECRET_KEY, algorithms=[settings.JWT__ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
