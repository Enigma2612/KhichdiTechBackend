from bson import ObjectId
from database import get_db
from Models import UserModel, ItemModel, InventoryModel, TransferModel, TransitModel

db = get_db()

Users = db.get_collection("users")
Items = db.get_collection("items")
Inventory = db.get_collection("inventory")
Transit = db.get_collection("transit")

# ---------------- USERS ----------------

async def create_user(user_data: dict):
    result = await Users.insert_one(user_data)
    return await Users.find_one({"_id": result.inserted_id})


async def get_all_users():
    users = []
    async for user in Users.find():
        users.append(user)
    return users


async def get_user(user_id: str):
    return await Users.find_one({"_id": ObjectId(user_id)})


# ---------------- ITEMS ----------------
# classification table: name + category

async def create_item(item_data: ItemModel):
    """Insert a new item type (e.g. banana -> fruit)."""
    item_dict = item_data.dict()
    result = await Items.insert_one(item_dict)
    return await Items.find_one({"_id": result.inserted_id})


async def get_all_items():
    items = []
    async for item in Items.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items


# ---------------- INVENTORY ----------------

async def create_inventory_entry(inv_data: InventoryModel):
    """Add quantity of an item for a user."""
    inv_dict = inv_data.dict()
    # convert reference ids to ObjectId where possible
    try:
        inv_dict["item_id"] = ObjectId(inv_dict["item_id"])
    except Exception:
        pass
    try:
        inv_dict["user_id"] = ObjectId(inv_dict["user_id"])
    except Exception:
        pass

    result = await Inventory.insert_one(inv_dict)
    rec = await Inventory.find_one({"_id": result.inserted_id})
    if rec:
        rec["_id"] = str(rec["_id"])
        if "item_id" in rec and isinstance(rec["item_id"], ObjectId):
            rec["item_id"] = str(rec["item_id"])
        if "user_id" in rec and isinstance(rec["user_id"], ObjectId):
            rec["user_id"] = str(rec["user_id"])
    return rec


async def get_inventory_for_user(user_id: str):
    records = []
    async for rec in Inventory.find({"user_id": ObjectId(user_id)}):
        records.append(rec)
    return records


async def get_all_inventory():
    records = []
    async for rec in Inventory.find():
        records.append(rec)
    return records


async def display_inventory():
    """Return inventory entries with item name/category and user info."""
    rows = []
    async for rec in Inventory.find():
        rec["_id"] = str(rec["_id"])
        # convert refs
        if "item_id" in rec:
            rec["item_id"] = str(rec["item_id"])
            item = await Items.find_one({"_id": ObjectId(rec["item_id"])})
            if item:
                item["_id"] = str(item["_id"])
                rec["item"] = item
        if "user_id" in rec:
            rec["user_id"] = str(rec["user_id"])
            user = await Users.find_one({"_id": ObjectId(rec["user_id"])})
            if user:
                user["_id"] = str(user["_id"])
                rec["user"] = user
        rows.append(rec)
    return rows


# ---------------- TRANSIT ----------------

async def create_transit_entry(transit_data: TransitModel):
    """Create a transit record describing packaging/shipping status for inventory or item."""
    t = transit_data.dict()
    # convert possible refs
    for key in ("inventory_id", "item_id", "user_id"):
        if key in t and t[key] is not None:
            try:
                t[key] = ObjectId(t[key])
            except Exception:
                pass

    result = await Transit.insert_one(t)
    rec = await Transit.find_one({"_id": result.inserted_id})
    if rec:
        rec["_id"] = str(rec["_id"])
        for key in ("inventory_id", "item_id", "user_id"):
            if key in rec and isinstance(rec[key], ObjectId):
                rec[key] = str(rec[key])
    return rec


async def get_all_transit():
    rows = []
    async for rec in Transit.find():
        rec["_id"] = str(rec["_id"])
        # embed inventory/item/user when available
        if "inventory_id" in rec and rec["inventory_id"]:
            try:
                inv = await Inventory.find_one({"_id": ObjectId(rec["inventory_id"])})
                if inv:
                    inv["_id"] = str(inv["_id"])
                    rec["inventory"] = inv
            except Exception:
                pass
        if "item_id" in rec and rec["item_id"]:
            try:
                item = await Items.find_one({"_id": ObjectId(rec["item_id"])})
                if item:
                    item["_id"] = str(item["_id"])
                    rec["item"] = item
            except Exception:
                pass
        if "user_id" in rec and rec["user_id"]:
            try:
                user = await Users.find_one({"_id": ObjectId(rec["user_id"])})
                if user:
                    user["_id"] = str(user["_id"])
                    rec["user"] = user
            except Exception:
                pass
        rows.append(rec)
    return rows


async def update_transit_status(transit_id: str, status: str, tracking_number: str = None, expected_delivery: str = None):
    """Update transit status and optional tracking info."""
    update = {"status": status}
    if tracking_number is not None:
        update["tracking_number"] = tracking_number
    if expected_delivery is not None:
        update["expected_delivery"] = expected_delivery

    await Transit.update_one({"_id": ObjectId(transit_id)}, {"$set": update})
    rec = await Transit.find_one({"_id": ObjectId(transit_id)})
    if rec:
        rec["_id"] = str(rec["_id"])
        for key in ("inventory_id", "item_id", "user_id"):
            if key in rec and isinstance(rec[key], ObjectId):
                rec[key] = str(rec[key])
    return rec


# ---------------- TRANSFER LOGIC ----------------

async def transfer_item(transfer_data: TransferModel):
    """Move quantity of a given item from one user's inventory to another's."""
    item_id = ObjectId(transfer_data.item_id)
    from_uid = ObjectId(transfer_data.from_user)
    to_uid = ObjectId(transfer_data.to_user)
    qty = transfer_data.quantity

    item = await Items.find_one({"_id": item_id})
    from_user = await get_user(transfer_data.from_user)
    to_user = await get_user(transfer_data.to_user)

    if not item or not from_user or not to_user:
        return {"error": "Invalid item or user"}

    # enforce role chain same as before
    valid_chain = (
        (from_user["role"] == "inputter" and to_user["role"] == "farmer") or
        (from_user["role"] == "farmer" and to_user["role"] == "processor") or
        (from_user["role"] == "processor" and to_user["role"] == "distributor")
    )
    if not valid_chain:
        return {"error": "Invalid transfer chain"}

    # ensure from inventory has enough
    from_record = await Inventory.find_one({"item_id": item_id, "user_id": from_uid})
    if not from_record or from_record.get("quantity", 0) < qty:
        return {"error": "Insufficient quantity"}

    # decrement from
    await Inventory.update_one(
        {"_id": from_record["_id"]},
        {"$inc": {"quantity": -qty}}
    )

    # increment to (create if missing)
    to_record = await Inventory.find_one({"item_id": item_id, "user_id": to_uid})
    if to_record:
        await Inventory.update_one(
            {"_id": to_record["_id"]},
            {"$inc": {"quantity": qty}}
        )
    else:
        await Inventory.insert_one({"item_id": item_id, "user_id": to_uid, "quantity": qty})

    # log transfer entry (optional)
    # optionally log the transfer data itself as record
    result = await Inventory.insert_one(transfer_data.dict())
    return await Inventory.find_one({"_id": result.inserted_id})