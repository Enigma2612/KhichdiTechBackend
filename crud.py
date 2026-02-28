from datetime import datetime, timezone
from database import users, items, inventory, transit


# ---------------- USERS ----------------

async def create_user(user_data: dict):
    users.append(user_data)
    return user_data


async def get_all_users():
    return users


async def get_user(user_id: str):
    for user in users:
        if user["user_id"] == user_id:
            return user
    return None


# ---------------- ITEMS ----------------

async def create_item(item_data):
    item_dict = item_data.dict()
    items.append(item_dict)
    return item_dict


async def get_all_items():
    return items


# ---------------- INVENTORY ----------------

async def create_inventory_entry(inv_data):
    inv_dict = inv_data.dict()
    inventory.append(inv_dict)
    return inv_dict


async def get_inventory_for_user(user_id: str):
    return [rec for rec in inventory if rec["user_id"] == user_id]


async def get_all_inventory():
    return inventory


# ---------------- TRANSIT ----------------

async def create_transit_entry(transit_data):
    t = transit_data.dict()
    t["placed_at"] = datetime.now(timezone.utc).isoformat()
    transit.append(t)
    return t


async def get_all_transit():
    return transit


async def update_transit_status(transit_id: str, status: str, tracking_number: str = None, expected_delivery: str = None):
    for t in transit:
        if t.get("inventory_id") == transit_id:
            t["status"] = status
            if tracking_number:
                t["tracking_number"] = tracking_number
            if expected_delivery:
                t["expected_delivery"] = expected_delivery

            now = datetime.now(timezone.utc).isoformat()
            if status in ("shipping", "in_transit"):
                t["dispatched_at"] = now
            elif status == "delivered":
                t["delivered_at"] = now

            return t
    return {"error": "Transit not found"}


# ---------------- TRANSFER LOGIC ----------------

async def transfer_item(transfer_data: dict):
    item_id = transfer_data["item_id"]
    from_uid = transfer_data["from_user"]
    to_uid = transfer_data["to_user"]
    qty = transfer_data["quantity"]

    from_user = await get_user(from_uid)
    to_user = await get_user(to_uid)

    if not from_user or not to_user:
        return {"error": "Invalid user"}

    valid_chain = (
        (from_user["role"] == "inputter" and to_user["role"] == "farmer") or
        (from_user["role"] == "farmer" and to_user["role"] == "processor") or
        (from_user["role"] == "processor" and to_user["role"] == "distributor")
    )

    if not valid_chain:
        return {"error": "Invalid transfer chain"}

    from_record = None
    for rec in inventory:
        if rec["item_id"] == item_id and rec["user_id"] == from_uid:
            from_record = rec
            break

    if not from_record or from_record["quantity"] < qty:
        return {"error": "Insufficient quantity"}

    from_record["quantity"] -= qty

    to_record = None
    for rec in inventory:
        if rec["item_id"] == item_id and rec["user_id"] == to_uid:
            to_record = rec
            break

    if to_record:
        to_record["quantity"] += qty
    else:
        inventory.append({
            "item_id": item_id,
            "user_id": to_uid,
            "quantity": qty
        })

    return {"message": "Transfer successful"}