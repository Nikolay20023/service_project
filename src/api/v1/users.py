from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from jose import jwt, JWTError


from db.db import get_session
from utils.users import (
    create_access_token,
    verify_password,
    get_password_hash,
    credentials_exception
)
from core.config import app_setting
from schema.user import User, UserCreate, Token, TokenData
from service.users import user_crud


router = APIRouter()

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/signin")


async def get_current_user(
    token: Annotated[str, Depends(oath2_scheme)],
    db: AsyncSession = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token, app_setting.secret_key, algorithms=app_setting.algorithm
        )
        username = payload.get("sub")
        if username is None:
            credentials_exception()
        token_data = TokenData(username=username)
    except JWTError:
        credentials_exception()

    user = await user_crud.get(db, username=token_data.username)

    if user is None:
        credentials_exception()
    return user


async def authenticate_user(db, username, password):
    user = await user_crud.get(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post(
    '/signup',
    description="New User registrations",
    status_code=status.HTTP_201_CREATED,
    response_model=User
)
async def signup(
    user: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    password = user.hashed_password
    user.hashed_password = get_password_hash(password)
    try:
        new_user = await user_crud.create(db=db, obj_in=user)
    except IntegrityError:
        return {
            "data": "username is already"
        }
    except SQLAlchemyError:
        raise
    return User(**new_user.__dict__)


@router.post(
    "/signin",
)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(
        db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise credentials_exception("Incorrect username or password")
    access_token_expires = timedelta(
        minutes=app_setting.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def read_own_users(user: Annotated[User, Depends(get_current_user)]):
    return user
