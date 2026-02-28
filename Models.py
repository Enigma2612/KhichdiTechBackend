from pydantic import BaseModel
from typing import Literal

class UserModel(BaseModel):
    name: str
    role: Literal["inputter", "farmer", "processor", "distributor"]


class ItemModel(BaseModel):
    name: str
    category: str  # e.g. "fruit", "vegetable", etc.


class ItemCreateRequest(BaseModel):
    name: str
    category: str
    user_id: str  # the user adding this item to their inventory
    quantity: float  # initial quantity


class InventoryModel(BaseModel):
    item_id: str
    user_id: str
    quantity: float


class TransferModel(BaseModel):
    item_id: str
    from_user: str
    to_user: str
    quantity: float


class TransitModel(BaseModel):
    # Reference to an inventory entry or item transfer
    inventory_id: str = None
    item_id: str = None
    user_id: str = None
    status: Literal["packaging", "shipping", "in_transit", "delivered", "cancelled"]
    tracking_number: str | None = None
    expected_delivery: str | None = None