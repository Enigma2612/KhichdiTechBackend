from fastapi import APIRouter
from Models import UserModel, ItemModel, ItemCreateRequest, InventoryModel, TransferModel
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


@router.get("/items")

async def get_inventory():
    return await crud.get_all_inventory()


# -------- TRANSFER --------

@router.post("/transfer")
async def transfer_item(transfer: TransferModel):
    return await crud.transfer_item(transfer.dict())