from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class UserModel(BaseModel):
    id: int
    name: str
    role: Literal["inputter", "farmer", "processor", "distributor"]


class ItemModel(BaseModel):
    id: int
    name: str
    type: str


class InventoryModel(BaseModel):
    user_id: int
    item: int
    qty: float
    batch_no: Optional[str] = None


class TransferModel(BaseModel):
    item: int
    from_user: int
    to_user: int
    qty: float


class TransitModel(BaseModel):
    batch_no: str
    user_from: int
    user_to: int
    item: int
    qty: float
    status: Optional[str] = "packaging"
    tracking_number: Optional[str] = None
    expected_delivery: Optional[str] = None
    placed_at: Optional[datetime] = None
    dispatched_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None