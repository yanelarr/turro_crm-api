# Routes province.py
from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.resources.province import ProvinceBase
from ...schemas.resources.result_object import ResultObject
from sqlalchemy.orm import Session
from typing import Dict
from ...app import get_db
from ...services.stock.classification import new, get_one_by_id, delete, update, get_all
from starlette import status
from ...auth_bearer import JWTBearer
  
classification_route = APIRouter(
    tags=["Nomenclators"],
    dependencies=[Depends(JWTBearer())]   
)

@classification_route.get("/classification", response_model=Dict, summary="Get list classification of products")
def get_classification(
    request: Request,
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(request=request, page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)


@classification_route.post("/classification", response_model=ResultObject, summary="Create a classification of products")
def create_classification(request:Request, classification: ProvinceBase, db: Session = Depends(get_db)):
    return new(request=request, classification=classification, db=db)

@classification_route.get("/classification/{id}", response_model=ResultObject, summary="Get a classification of products for your ID.")
def get_classification_by_id(request:Request, id: int, db: Session = Depends(get_db)):
    return get_one_by_id(request, id=id, db=db)

@classification_route.delete("/classification/{id}", response_model=ResultObject, summary="Remove classification of products for your ID")
def delete_classification(request:Request, id: int, db: Session = Depends(get_db)):
    return delete(request=request, id=id, db=db)
    
@classification_route.put("/classification/{id}", response_model=ResultObject, summary="Update classification of products for your ID")
def update_classification(request:Request, id: int, classification: ProvinceBase, db: Session = Depends(get_db)):
    return update(request=request, db=db, id=id, classification=classification)