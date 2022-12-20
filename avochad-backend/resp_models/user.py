from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(..., title="ID", description="ID")
    username: str = Field(..., title="Username", description="Username")
    email: str = Field(..., title="Email", description="Email")

    