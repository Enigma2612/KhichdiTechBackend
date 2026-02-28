from bson import ObjectId
from database import user_collection, resources, shipment_collection
from Models import UserModel

# -------- user --------

async def create_user(user_data: UserModel):
    user_dict = user_data.dict()
    result = await user_collection.insert_one(user_dict)
    return await user_collection.find_one({"_id": result.inserted_id})


async def get_all_users():
    users = []
    async for user in user_collection.find():
        users.append(user)
    return users


# -------- BATCH --------

async def create_batch(batch_data: dict):
    result = await resources.insert_one(batch_data)
    return await resources.find_one({"_id": result.inserted_id})


async def get_all_batches():
    batches = []
    async for batch in resources.find():
        batches.append(batch)
    return batches


# -------- SHIPMENT --------

async def create_shipment(shipment_data: dict):
    result = await shipment_collection.insert_one(shipment_data)
    return await shipment_collection.find_one({"_id": result.inserted_id})


async def get_all_shipments():
    shipments = []
    async for shipment in shipment_collection.find():
        shipments.append(shipment)
    return shipments