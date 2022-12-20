import datetime
import bcrypt
import jwt

from db_models.user import User
from settings import settings
from dataclasses import dataclass

@dataclass
class TokenPayload:
    id: int
    email: str
    exp: datetime.datetime


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_jwt_token(user: User) -> str:
    return jwt.encode(
        {
            "id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

def decode_jwt_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        payload["exp"] = datetime.datetime.fromtimestamp(payload["exp"])
        return TokenPayload(**payload)
    except jwt.PyJWTError:
        return None