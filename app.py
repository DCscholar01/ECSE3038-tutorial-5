import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["ecse3038"]
devices = db["tutorial5"]

app = FastAPI()


class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


# Your handlers go below this line.
#GET /devices, every device
@app.get("/devices")
async def get_devices():
    device_list = list(devices.find())
    return device_list

#GET /devices/{device_id}, a specific device
@app.get("/devices/{device_id}")
async def get_device(device_id: str):
    device = devices.find_one({"_id": device_id})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device