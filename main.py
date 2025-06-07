from fastapi import FastAPI
from .routers.users import router as register_new_user
from .routers.chats import router as chat_router
from .routers.messages import router as message_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Это будет мессенджер"}


app.include_router(register_new_user)
app.include_router(chat_router)
app.include_router(message_router)
