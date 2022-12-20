import datetime
import jwt

from dataclasses import dataclass
from settings import settings

@dataclass
class InvitePayload:
    id: int
    exp: datetime.datetime


def create_invite_token(chat_id: int) -> str:
    return jwt.encode(
        {
            "id": chat_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=50),
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )

def decode_invite_token(token: str) -> InvitePayload | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        payload["exp"] = datetime.datetime.fromtimestamp(payload["exp"])
        return InvitePayload(**payload)
    except jwt.PyJWTError:
        return None

def is_invite_valid(payload: InvitePayload | None) -> bool:
    if payload == None:
        return False
    return payload.exp > datetime.datetime.utcnow()