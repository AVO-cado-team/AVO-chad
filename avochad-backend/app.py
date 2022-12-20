from fastapi import FastAPI
from routers.auth import auth_router
from routers.me import me_router
from tortoise import Tortoise
from settings import settings

app = FastAPI()

app.include_router(auth_router.router, tags=["Auth"], prefix="/auth")
app.include_router(me_router.router, tags=["Me"], prefix="/me")


@app.on_event("startup")
async def startup():
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["db_models.user"]}
    )
    await Tortoise.generate_schemas()

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)