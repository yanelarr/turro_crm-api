# Routes province.py
from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.resources.province import ProvinceBase
from ...schemas.resources.result_object import ResultObject
from sqlalchemy.orm import Session
from typing import Dict
from ...app import get_db
from ...services.resources.province import new, get_one_by_id, delete, update, get_all
from starlette import status
from ...auth_bearer import JWTBearer
  
province_route = APIRouter(
    tags=["Nomenclators"],
    dependencies=[Depends(JWTBearer())]   
)

@province_route.get("/province", response_model=Dict, summary="Get list of Province")
def get_province(
    request: Request,
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(request=request, page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)


@province_route.post("/province", response_model=ResultObject, summary="Create a province")
def create_province(request:Request, province: ProvinceBase, db: Session = Depends(get_db)):
    return new(request=request, province=province, db=db)

@province_route.get("/province/{id}", response_model=ResultObject, summary="Get a Province for your ID.")
def get_province_by_id(request:Request, id: int, db: Session = Depends(get_db)):
    return get_one_by_id(request, id=id, db=db)

@province_route.delete("/province/{id}", response_model=ResultObject, summary="Remove province for your ID")
def delete_province(request:Request, id: int, db: Session = Depends(get_db)):
    return delete(request=request, id=id, db=db)
    
@province_route.put("/province/{id}", response_model=ResultObject, summary="Update province for your ID")
def update_province(request:Request, id: int, province: ProvinceBase, db: Session = Depends(get_db)):
    return update(request=request, db=db, id=id, province=province)

