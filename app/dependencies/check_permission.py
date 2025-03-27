import jwt

from fastapi import Depends, HTTPException, status
from jwt import PyJWTError

from app.config.settings import settings
from app.users.jwt import oauth2_scheme
from app.users.schemas import TokenPayload


def check_permission(req_permissions: list[str], token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT__SECRET_KEY, algorithms=[settings.JWT__ALGORITHM])
        token_payload = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    if not any([req_permission in token_payload.permissions for req_permission in req_permissions]):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return token_payload
