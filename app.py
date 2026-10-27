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
    device_list = list(devices.find({}, {"_id": 0}))
    return device_list

#GET /devices/{name}, a specific device
@app.get("/devices/{name}")
async def get_device(name: str):
    device = devices.find_one({"name": name}, {"_id": 0})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

#POST /devices, add a new device
@app.post("/devices")
async def add_device(device: Device):
    devices.insert_one(device.dict())
    return device


#PUT /devices/{name}, update a specific device
@app.put("/devices/{name}")
async def update_device(name: str, device: Device):
    result = devices.update_one({"name": name}, {"$set": device.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Device not found")
    return device