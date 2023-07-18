"""coding=utf-8."""
 
from datetime import datetime
from pydantic import BaseModel
   
class MarkBase(BaseModel):
    name: str
    description: str
    
class MarkShema(MarkBase):
    id: int
    created_by: str
    created_date: datetime
    updated_by: str
    updated_date: datetime
    
    is_active: bool = True
 
    class Config:
        orm_mode = True
        
        
class ProductMarkskBase(BaseModel):
    mark_id: int
    product_id: str
    
class ProductMarksShema(ProductMarkskBase):
    
    created_by: str
    created_date: datetime
    updated_by: str
    updated_date: datetime
    
    is_active: bool = True
 
    class Config:
        orm_mode = True