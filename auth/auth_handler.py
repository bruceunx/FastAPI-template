import time
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from services.users import get_user

SECRET_KEY = "35216a95925db818a0b4881f95fab0cc9fff254d65a9ea6d831b0e5bda4db2f3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES = 3600 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/user/token")


def generate_token(username: str) -> tuple[str, str]:
    data = {
        "username": username,
        "expires": time.time() + ACCESS_TOKEN_EXPIRES
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    data["expires"] = time.time() + ACCESS_TOKEN_EXPIRES * 3
    refresh_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token, refresh_token


def verify_token(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str | None = payload.get("username", None)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    expires: float | None = payload.get("expires", None)
    if expires is None or time.time() > expires:
        raise jwt.ExpiredSignatureError
    return username


def generate_new_token(token: str) -> str:
    username = verify_token(token)
    data = {
        "username": username,
        "expires": time.time() + ACCESS_TOKEN_EXPIRES
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_rol_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    username = get_current_user(token)
    rol = await check_group(username)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication levels",
        )
    return username


async def check_group(username: str) -> int:
    user = await get_user(username)
    return user.group
