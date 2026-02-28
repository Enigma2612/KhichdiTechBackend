from fastapi import APIRouter, Body
from Models import UserModel, ItemModel, ItemCreateRequest, InventoryModel, TransferModel, TransitModel
import crud

router = APIRouter()

# -------- USERS --------

@router.post("/users")
async def create_user(user: UserModel):
    return await crud.create_user(user.dict())


@router.get("/users")
async def get_users():
    return await crud.get_all_users()


# -------- ITEMS --------

@router.post("/items")
async def create_item(item_req: ItemCreateRequest):
    # Create the item classification
    item_model = ItemModel(name=item_req.name, category=item_req.category)
    created_item = await crud.create_item(item_model)
    
    # Create the inventory entry for this item
    inventory_model = InventoryModel(
        item_id=str(created_item["_id"]),
        user_id=item_req.user_id,
        quantity=item_req.quantity
    )
    await crud.create_inventory_entry(inventory_model)
    
    return created_item

# ------- INVENTORY --------

@router.get("/inventory")
async def get_inventory():
    return await crud.get_all_inventory()

@router.get("/inventory")
async def get_inventory_for_user(user_id: str):
    return await crud.get_inventory_for_user(user_id)


# -------- TRANSFER --------

@router.post("/transfer")
async def transfer_item(transfer: TransferModel):
    return await crud.transfer_item(transfer.dict())


# -------- TRANSIT --------

@router.post("/transit")
async def create_transit(transit: TransitModel):
    return await crud.create_transit_entry(transit)


@router.get("/transit")
async def list_transit():
    return await crud.get_all_transit()


@router.patch("/transit/{transit_id}/status")
async def patch_transit_status(transit_id: str, payload: dict = Body(...)):
    # payload expected to contain at least {"status": "shipping"}
    status = payload.get("status")
    tracking = payload.get("tracking_number")
    expected = payload.get("expected_delivery")
    return await crud.update_transit_status(transit_id, status, tracking, expected)