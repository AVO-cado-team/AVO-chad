from fastapi import FastAPI, Response, status
from fastapi.exceptions import RequestValidationError
from routers.auth import auth_router
from routers.me import me_router
from routers.chat import chat_router
from tortoise import Tortoise
from settings import settings

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return Response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


app.include_router(auth_router.router, tags=["Auth"], prefix="/auth")
app.include_router(me_router.router, tags=["Me"], prefix="/me")
app.include_router(chat_router.router, tags=["Chat"], prefix="/chat")


# TODO: USE WebSockets
# TODO: https://fastapi.tiangolo.com/advanced/websockets/



@app.on_event("startup")
async def startup():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["db_models.user", "db_models.chat", "db_models.message"]}
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)