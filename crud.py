from bson import ObjectId
from database import user_collection, item_collection, inventory_collection

# ---------------- USERS ----------------

async def create_user(user_data: dict):
    result = await user_collection.insert_one(user_data)
    return await user_collection.find_one({"_id": result.inserted_id})


async def get_all_users():
    users = []
    async for user in user_collection.find():
        users.append(user)
    return users


async def get_user(user_id: str):
    return await user_collection.find_one({"_id": ObjectId(user_id)})


# ---------------- ITEMS ----------------

async def create_item(item_data: dict):
    result = await item_collection.insert_one(item_data)
    return await item_collection.find_one({"_id": result.inserted_id})


async def get_all_items():
    items = []
    async for item in item_collection.find():
        items.append(item)
    return items


# ---------------- TRANSFER LOGIC ----------------

async def transfer_item(transfer_data: dict):
    item = await item_collection.find_one({"_id": ObjectId(transfer_data["item_id"])})
    from_user = await get_user(transfer_data["from_user"])
    to_user = await get_user(transfer_data["to_user"])

    if not item or not from_user or not to_user:
        return {"error": "Invalid item or user"}

    # --- Role enforcement (linear chain) ---

    valid_chain = (
        (from_user["role"] == "inputter" and to_user["role"] == "farmer") or
        (from_user["role"] == "farmer" and to_user["role"] == "processor") or
        (from_user["role"] == "processor" and to_user["role"] == "distributor")
    )

    if not valid_chain:
        return {"error": "Invalid transfer chain"}

    # Update ownership
    await item_collection.update_one(
        {"_id": ObjectId(transfer_data["item_id"])},
        {"$set": {"owner_id": transfer_data["to_user"]}}
    )

    # Log transfer
    result = await inventory_collection.insert_one(transfer_data)

    return await inventory_collection.find_one({"_id": result.inserted_id})