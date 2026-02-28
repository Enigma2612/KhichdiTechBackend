from fastapi import APIRouter
from Models import UserModel, ItemModel, TransferModel
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
    return await crud.create_item(item.dict())


@router.get("/items")
async def get_items():
    return await crud.get_all_items()


# -------- TRANSFER --------

@router.post("/transfer")
async def transfer_item(transfer: TransferModel):
    return await crud.transfer_item(transfer.dict())