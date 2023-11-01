from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext

from schemas.users import UserTokenSchema
from services.users import get_user  # type: ignore
from auth.auth_handler import generate_token, generate_new_token  # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_user = await get_user(form_data.username)
    if db_user is None:
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password")
    password = form_data.password
    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password")
    accss_token, refresh_token = generate_token(db_user.username)

    return {
        "access_token": accss_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh-token/")
async def refresh_token(token: UserTokenSchema):
    try:
        new_access_token = generate_new_token(token.refresh_token)
        return {"access_token": new_access_token}
    except jwt.ExpiredSignatureError:
        return {"error": "Refresh token has expired."}
    except HTTPException:
        return {"error": "Invalid refresh token."}
