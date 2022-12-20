from fastapi import FastAPI, Query
from resp_models.login import LoginResponse, LoginUnsuccessful
from resp_models.register import RegisterResponse, RegisterUnsuccessful

from utils.security import (
    TokenPayload, 
    create_jwt_token, 
    decode_jwt_token, 
    hash_password, 
    check_password
)
from db_models.user import User
from tortoise import queryset

auth_router = FastAPI(
    title="Auth",
    description="Auth API",
    version="0.1.0",
)



@auth_router.post("/register")
async def register(
    first_name: str = Query(..., min_length=2, max_length=50),
    last_name: str = Query(..., min_length=2, max_length=50),
    username: str = Query(..., min_length=2, max_length=50),
    email: str = Query(..., min_length=2, max_length=50, regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    password: str = Query(..., min_length=2, max_length=50),
) -> RegisterResponse | RegisterUnsuccessful:
    user: User | None = await User.get_or_none(
        queryset.Q(username=username) | queryset.Q(email=email)
    )
    if user != None:
        return RegisterUnsuccessful()
    
    hashed_password = hash_password(password)
    user = await User.create(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=hashed_password
    )
    token = create_jwt_token(user)
    return RegisterResponse(jwt=token)


@auth_router.get("/login")
async def login(
    username: str = Query(..., min_length=2, max_length=50),
    password: str = Query(..., min_length=2, max_length=50),
) -> LoginResponse | LoginUnsuccessful:
    user: User | None = await User.get_or_none(queryset.Q(username=username))
    if user == None:
        return LoginUnsuccessful()
    
    if not check_password(password, user.password):
        return LoginUnsuccessful()

    token = create_jwt_token(user)
    return LoginResponse(jwt=token)
