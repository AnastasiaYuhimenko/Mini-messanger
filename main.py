from fastapi import FastAPI
from .routers.users import router as register_new_user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Это будет мессенджер"}


app.include_router(register_new_user)
