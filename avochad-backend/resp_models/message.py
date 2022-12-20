from pydantic import BaseModel
from .user import UserResponse

class MessageResponse(BaseModel):
    id: int
    text: str
    chat: int
    user: UserResponse
    date: str
    reply_to: 'MessageResponse' = None

    class Config:
        orm_mode = True