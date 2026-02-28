from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List

app = FastAPI()

# -----------------------
# MongoDB Setup
# -----------------------

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.farm_tracker

users_collection = db.users
batches_collection = db.batches
shipments_collection = db.shipments


# -----------------------
# Utility
# -----------------------

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# -----------------------
# Schemas
# -----------------------

class User(BaseModel):
    name: str
    role: str  # farmer / distributor / retailer


class Batch(BaseModel):
    crop_name: str
    quantity: float
    farmer_id: str
    status: str = "harvested"


class Shipment(BaseModel):
    batch_id: str
    from_location: str
    to_location: str
    status: str = "in_transit"


# -----------------------
# Routes
# -----------------------

@app.post("/users")
async def create_user(user: User):
    result = await users_collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}


@app.post("/batches")
async def create_batch(batch: Batch):
    result = await batches_collection.insert_one(batch.dict())
    return {"id": str(result.inserted_id)}


@app.post("/shipments")
async def create_shipment(shipment: Shipment):
    result = await shipments_collection.insert_one(shipment.dict())
    return {"id": str(result.inserted_id)}


@app.get("/batches")
async def get_batches():
    batches = []
    async for batch in batches_collection.find():
        batches.append(serialize(batch))
    return batches