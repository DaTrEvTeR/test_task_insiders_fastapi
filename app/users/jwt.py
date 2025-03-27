import jwt
import datetime

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from app.config.settings import settings
from app.db.models.user import User
from app.users.schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user: User) -> str:
    permissions = [perm.name.lower() for perm in user.role.permissions]
    payload = TokenPayload(user_id=user.id, permissions=permissions).model_dump()

    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT__ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.JWT__SECRET_KEY, algorithm=settings.JWT__ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT__SECRET_KEY, algorithms=[settings.JWT__ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
