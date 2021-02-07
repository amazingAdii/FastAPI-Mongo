from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient

from route import router
from config import DB_URL, DB_NAME

app = FastAPI()

@app.get("/")
async def root():
    return {"message": DB_URL}

@app.on_event("startup")
async def start_up():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shut_down():
    app.mongodb_client.close()

app.include_router(router)