from fastapi import Depends, HTTPException
from db_models.user import User
from utils.security import decode_jwt_token, is_authenticated, TokenPayload

async def get_current_user(payload: TokenPayload | None = Depends(decode_jwt_token)) -> User:
    if not is_authenticated(payload):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = await User.get_or_none(id = payload.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user