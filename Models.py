from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class UserModel(BaseModel):
    user_id: str
    name: str
    role: Literal["inputter", "farmer", "processor", "distributor"]


class ItemModel(BaseModel):
    item_id: str
    name: str
    category: str  # e.g. "fruit", "vegetable", etc.


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
    quantity: float  # quantity being shipped
    status: Literal["packaging", "shipping", "in_transit", "delivered", "cancelled"]
    tracking_number: str | None = None
    expected_delivery: str | None = None
    placed_at: Optional[datetime] = None
    dispatched_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None