"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
   
class ProvinceBase(BaseModel):
    name: str
    description: str
    
class ProvinceShema(ProvinceBase):
    id: int
    created_by: str
    created_date: datetime
    updated_by: str
    updated_date: datetime
    
    is_active: bool = True
 
    class Config:
        orm_mode = True
