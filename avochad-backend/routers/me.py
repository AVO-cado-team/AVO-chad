import datetime
from fastapi import FastAPI, Query
from resp_models.me import MeResponse

from utils.security import (
    TokenPayload, 
    create_jwt_token, 
    decode_jwt_token, 
    hash_password, 
    check_password
)
from db_models.user import User
from tortoise import queryset

me_router = FastAPI(
    title="Me",
    description="Me API",
    version="0.1.0",
)


@me_router.get("/me")
async def me(token: str = Query(...)) -> MeResponse:
    if not token:
        return {"detail": "Not authenticated"}
    
    payload = decode_jwt_token(token)
    if not payload:
        return {"detail": "Not authenticated"}
    
    if payload.exp < datetime.datetime.utcnow():
        return {"detail": "Token expired"}
    
    user = await User.get_or_none(id=payload.id)
    if not user:
        return {"detail": "User not found"}
    
    return MeResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )
    
    
