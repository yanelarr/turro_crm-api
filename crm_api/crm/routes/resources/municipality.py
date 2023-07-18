# Routes municipality.py
from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.resources.municipality import MunicipalityBase
from ...schemas.resources.result_object import ResultObject
from sqlalchemy.orm import Session
from typing import Dict
from ...app import get_db
from ...services.resources.municipality import new, get_one_by_id, delete, update, get_all, get_municipalities_by_province_id
from starlette import status
from ...auth_bearer import JWTBearer
  
municipality_route = APIRouter(
    tags=["Nomenclators"],
    dependencies=[Depends(JWTBearer())]   
)

@municipality_route.get("/municipality", response_model=Dict, summary="Get list of Municipalities")
def get_municipalities(
    request: Request,
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(request=request, page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)


@municipality_route.post("/municipality", response_model=ResultObject, summary="Create a Municipality")
def create_municipality(request:Request, municipality: MunicipalityBase, db: Session = Depends(get_db)):
    return new(request=request, municipality=municipality, db=db)

@municipality_route.get("/municipality/{id}", response_model=ResultObject, summary="Get a Municipality for your ID.")
def get_municipality_by_id(request:Request, id: int, db: Session = Depends(get_db)):
    return get_one_by_id(request, id=id, db=db)

@municipality_route.delete("/municipality/{id}", response_model=ResultObject, summary="Remove municipality for your ID")
def delete_municipality(request:Request, id: int, db: Session = Depends(get_db)):
    return delete(request=request, id=id, db=db)
    
@municipality_route.put("/municipality/{id}", response_model=ResultObject, summary="Update municipality for your ID")
def update_municipality(request:Request, id: int, municipality: MunicipalityBase, db: Session = Depends(get_db)):
    return update(request=request, db=db, id=id, municipality=municipality)

@municipality_route.get("/municipality/province/{id}", response_model=ResultObject, summary="Get list of Municipalities for province")
def get_municipalities_by_province(request:Request, province_id: int, db: Session = Depends(get_db)):
    return get_municipalities_by_province_id(request, province_id=province_id, db=db)

