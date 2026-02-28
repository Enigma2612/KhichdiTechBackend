from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    id: str
    type: str  # e.g., "inputter", "farmer", "processor", "distributor"
    email: Optional[str] = None
    name: Optional[str] = None

class InputterModel(BaseModel):
    inputter_id : str

class FarmerModel(BaseModel):
    inputter_id: str
    
class FarmerReq(BaseModel):
    seed_type: str
    quantity: float

class ProcessorModel(BaseModel):
    processor_id: str
    
class ProcessorReq(BaseModel):
    crop_type: str
    quantity: float
    farmer_id: str

class DistributorModel(BaseModel):
    distributor_id : str

class DistributorReq(BaseModel):
    crop_type: str
    quantity: float
    farmer_id: str
