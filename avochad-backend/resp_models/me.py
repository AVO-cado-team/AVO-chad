from pydantic import BaseModel, Field


class MeResponse(BaseModel):
    id: int = Field(..., title="ID", description="ID")
    username: str = Field(..., title="Username", description="Username")
    email: str = Field(..., title="Email", description="Email")

    