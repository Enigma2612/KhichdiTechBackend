from fastapi import APIRouter, Body
from Models import UserModel, ItemModel, InventoryModel, TransferModel, TransitModel
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
async def create_item(item: ItemModel):
    return await crud.create_item(item)


@router.get("/items")
async def get_items():
    return await crud.get_all_items()


# ------- INVENTORY --------

@router.post("/inventory")
async def create_inventory(inv: InventoryModel):
    return await crud.create_inventory_entry(inv)


@router.get("/inventory")
async def get_inventory():
    return await crud.get_all_inventory()


@router.get("/inventory/{user_id}")
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
    return await crud.update_transit_status(
        transit_id,
        payload.get("status"),
        payload.get("tracking_number"),
        payload.get("expected_delivery"),
    )