from fastapi import APIRouter, Body
from typing import List
from Models import UserModel, ItemModel, InventoryModel, TransferModel, TransitModel
import crud

router = APIRouter()

# -------- USERS --------

@router.post("/users", response_model=UserModel)
async def create_user(user: UserModel):
    return await crud.create_user(user.dict())


@router.get("/users", response_model=List[UserModel])
async def get_users():
    return await crud.get_all_users()


# -------- ITEMS --------

@router.post("/items", response_model=ItemModel)
async def create_item(item: ItemModel):
    return await crud.create_item(item)


@router.get("/items", response_model=List[ItemModel])
async def get_items():
    return await crud.get_all_items()


# -------- INVENTORY --------

@router.post("/inventory", response_model=InventoryModel)
async def create_inventory(inv: InventoryModel):
    return await crud.create_inventory_entry(inv)


@router.get("/inventory", response_model=List[InventoryModel])
async def get_inventory():
    return await crud.get_all_inventory()


@router.get("/inventory/{user_id}", response_model=List[InventoryModel])
async def get_inventory_for_user(user_id: int):
    return await crud.get_inventory_for_user(user_id)


# -------- TRANSFER --------

@router.post("/transfer")
async def transfer_item(transfer: TransferModel):
    return await crud.transfer_item(transfer.dict())


# -------- TRANSIT --------

@router.post("/transit", response_model=TransitModel)
async def create_transit(transit: TransitModel):
    return await crud.create_transit_entry(transit)


@router.get("/transit", response_model=List[TransitModel])
async def list_transit():
    return await crud.get_all_transit()


@router.patch("/transit/{batch_no}/status")
async def patch_transit_status(batch_no: str, payload: dict = Body(...)):
    return await crud.update_transit_status(
        batch_no,
        payload.get("status"),
        payload.get("tracking_number"),
        payload.get("expected_delivery"),
    )