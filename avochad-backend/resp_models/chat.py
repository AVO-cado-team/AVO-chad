from pydantic import BaseModel
from .user import UserResponse
from .message import MessageResponse

class ChatResponse(BaseModel):
    id: int
    name: str
    chat_name: str
    users: list[UserResponse]
    admin: UserResponse
    messages: list[MessageResponse]
    is_private: bool
    date: str