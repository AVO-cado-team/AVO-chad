from pydantic import BaseModel, Field

class RegisterResponse(BaseModel):
    jwt: str = Field(..., title="JWT token", description="JWT token")


class RegisterUnsuccessful(BaseModel):
    status_code: int = Field(401, title="Status code", description="Status code")
    detail: str = Field("Register unsuccessful", title="Detail", description="Detail")
    headers: dict[str, str] = Field({"WWW-Authenticate": "Bearer"}, title="Headers", description="Headers")