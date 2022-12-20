from pydantic import BaseModel, Field
from fastapi import Response

class RegisterResponse(BaseModel):
    jwt: str = Field(..., title="JWT token", description="JWT token")


class RegisterUnsuccessful(Response):
    status_code: int = 401
    detail: str = "Register unsuccessful"
    headers: dict[str, str] = {"WWW-Authenticate": "Bearer"}