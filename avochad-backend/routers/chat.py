import datetime

from fastapi import FastAPI, HTTPException, Query, Depends
from deps import get_current_user
from resp_models.user import UserResponse
from resp_models.chat import ChatResponse
from resp_models.message import MessageResponse

from utils.invite import (
    is_invite_valid,
    create_invite_token,
    decode_invite_token,
)
from db_models.user import User
from db_models.chat import Chat
from db_models.message import Message


chat_router = FastAPI(
    title="Chat",
    description="Chat API",
    version="0.1.0",
)

async def convert_chat_to_chat_response(chat: Chat) -> ChatResponse:
    chat_users = [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        ) for user in await chat.users.all()
    ]

    cadmin = await chat.admin

    chat_admin = UserResponse(
        id=cadmin.id,
        username=cadmin.username,
        email=cadmin.email,
    )
    chat_messages = [
        MessageResponse(
            id=message.id,
            text=message.text,
            chat=(await message.chat).id,
            user=UserResponse(
                id=(await message.user).id,
                username=(await message.user).username,
                email=(await message.user).email,
            ),
            reply_to=await convert_message_to_message_response(await message.reply_to) if message.reply_to else None,
            date=message.date.strftime("%Y-%m-%d %H:%M:%S"),
        ) for message in await chat.messages.limit(10)
    ]

    return ChatResponse(
        id=chat.id,
        name=chat.name,
        chat_name=chat.chat_name,
        users=chat_users,
        admin=chat_admin,
        messages=chat_messages,
        date=chat.date.strftime("%Y-%m-%d %H:%M:%S"),
        is_private=chat.is_private,
    )


async def convert_message_to_message_response(message: Message) -> MessageResponse:
    user = await message.user
    user = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )

    return MessageResponse(
        id=message.id,
        text=message.text,
        chat=(await message.chat).id,
        user=user,
        reply_to=await convert_message_to_message_response(await message.reply_to) if message.reply_to else None,
        date=message.date.strftime("%Y-%m-%d %H:%M:%S"),
    )


@chat_router.post("/create")
async def create_chat(
    user: User = Depends(get_current_user),
    name: str = Query(..., min_length=2, max_length=50),
    chat_name: str = Query(..., min_length=2, max_length=50),
    is_private: bool = Query(False),
    ) -> ChatResponse:
    if await Chat.filter(chat_name=chat_name).exists():
        raise HTTPException(status_code=400, detail="Chat with this name already exists")
    
    chat = await Chat.create(
        name=name,
        chat_name=chat_name,
        admin=user,
        is_private=is_private,
    )

    await chat.users.add(user)
    await chat.save()

    return await convert_chat_to_chat_response(chat)


@chat_router.get("/list")
async def list_chats(
    user: User = Depends(get_current_user),
    ) -> list[ChatResponse]:
    chats = await Chat.filter(users__id=user.id).all()

    resp = []
    for chat in chats:
        resp.append(await convert_chat_to_chat_response(chat))
    return resp


@chat_router.get("/{chat_name}")
async def get_chat(
    user: User = Depends(get_current_user),
    chat_name: str = Query(..., min_length=2, max_length=50),
    ) -> ChatResponse:

    chat = await Chat.filter(chat_name=chat_name).first()
    if chat == None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not await chat.users.filter(id=user.id).exists():
        raise HTTPException(status_code=403, detail="You are not in this chat")

    return await convert_chat_to_chat_response(chat)


@chat_router.get("/invite")
async def get_invite_code(
    user: User = Depends(get_current_user),
    chat_name: str = Query(..., min_length=2, max_length=50),
    ) -> str:

    chat: Chat = await Chat.filter(chat_name=chat_name).first()
    if chat == None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not await chat.users.filter(id=user.id).exists():
        raise HTTPException(status_code=403, detail="You are not in this chat")
    if not (await chat.admin).id == user.id:
        raise HTTPException(status_code=403, detail="You are not admin of this chat")
    
    return create_invite_token(chat.id)


@chat_router.post("/join/{chat_name}")
async def join_chat(
    user: User = Depends(get_current_user),
    chat_name: str = Query(..., min_length=2, max_length=50),
    invite_code: str = Query(None, min_length=2, max_length=90),
    ) -> ChatResponse:

    chat = await Chat.filter(chat_name=chat_name).first()
    if chat == None:
        raise HTTPException(status_code=404, detail="Chat not found")

    if await chat.users.filter(id=user.id).exists():
        raise HTTPException(status_code=403, detail="You are already in this chat")
    
    invite_code_payload = decode_invite_token(invite_code)

    if chat.is_private:
        if not invite_code_payload:
            raise HTTPException(status_code=403, detail="This chat is private")

        if is_invite_valid(invite_code_payload):
            raise HTTPException(status_code=403, detail="Invite code expired")

        if invite_code_payload.id != chat.id:
            raise HTTPException(status_code=403, detail="Invalid invite code")

    await chat.users.add(user)
    await chat.save()

    return await convert_chat_to_chat_response(chat)


@chat_router.post("/leave/{chat_name}")
async def leave_chat(
    user: User = Depends(get_current_user),
    chat_name: str = Query(..., min_length=2, max_length=50),
    ) -> ChatResponse:

    chat = await Chat.filter(chat_name=chat_name).first()
    if chat == None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not await chat.users.filter(id=user.id).exists():
        raise HTTPException(status_code=403, detail="You are not in this chat")
    if (await chat.admin).id == user.id:
        raise HTTPException(status_code=403, detail="You are admin of this chat")

    await chat.users.remove(user)
    await chat.save()

    return await convert_chat_to_chat_response(chat)


@chat_router.post("/delete/{chat_name}")
async def delete_chat(
    user: User = Depends(get_current_user),
    chat_name: str = Query(..., min_length=2, max_length=50),
    ) -> ChatResponse:

    chat = await Chat.filter(chat_name=chat_name).first()
    if chat == None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not chat.admin.id == user.id:
        raise HTTPException(status_code=403, detail="You are not admin of this chat")

    await chat.delete()

    return await convert_chat_to_chat_response(chat)


@chat_router.post("/send/{chat_name}")
async def send_message(
    user: User = Depends(get_current_user),
    chat_name: str = Query(..., min_length=2, max_length=50),
    message: str = Query(..., min_length=1, max_length=500),
    reply_to: int = Query(None, ge=0),
    ) -> MessageResponse:

    chat = await Chat.filter(chat_name=chat_name).first()
    if chat == None:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not await chat.users.filter(id=user.id).exists():
        raise HTTPException(status_code=403, detail="You are not in this chat")
    
    if reply_to:
        reply_to_message = await Message.filter(id=reply_to).first()
        if reply_to_message == None:
            raise HTTPException(status_code=404, detail="Message not found")
        if (await reply_to_message.chat).id != chat.id:
            raise HTTPException(status_code=403, detail="Message not in this chat")

    print(chat.messages)
    msg = await Message.create(
        text=message,
        reply_to=reply_to_message if reply_to else None,
        chat=chat,
        user=user,
    )
    await msg.save()
    await chat.messages.add(msg)

    return await convert_message_to_message_response(msg)