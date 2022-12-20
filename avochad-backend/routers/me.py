import datetime

from fastapi import FastAPI, Query, Depends
from resp_models.user import UserResponse
from deps import get_current_user

from utils.security import (
    TokenPayload, 
    create_jwt_token, 
    decode_jwt_token, 
    is_authenticated,
    hash_password, 
    check_password
)
from db_models.user import User


me_router = FastAPI(
    title="Me",
    description="Me API",
    version="0.1.0",
)


@me_router.get("/me")
async def me(
    user: User = Depends(get_current_user),
    ) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )

@me_router.post("/update")
async def update_me(
    user: User = Depends(get_current_user),
    first_name: str = Query(None, min_length=2, max_length=50),
    last_name: str = Query(None, min_length=2, max_length=50),
    username: str = Query(None, min_length=2, max_length=50),
    email: str = Query(None, min_length=2, max_length=50, regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    password: str = Query(None, min_length=2, max_length=50),
    ) -> UserResponse:
    if first_name != None:
        user.first_name = first_name
    if last_name != None:
        user.last_name = last_name
    if username != None:
        user.username = username
    if email != None:
        user.email = email
    if password != None:
        user.password = hash_password(password)
    await user.save()
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )


@me_router.post("/delete")
async def delete_me(
    user: User = Depends(get_current_user),
    ) -> UserResponse:
    await user.delete()
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )

