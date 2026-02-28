from pydantic import BaseModel
from typing import Literal

class UserModel(BaseModel):
    name: str
    role: Literal["inputter", "farmer", "processor", "distributor"]


class ItemModel(BaseModel):
    name: str
    quantity: float
    owner_id: str
    stage: Literal["raw", "processed", "packaged"]


class TransferModel(BaseModel):
    item_id: str
    from_user: str
    to_user: str