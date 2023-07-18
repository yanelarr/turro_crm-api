# Routes province.py
from fastapi import APIRouter, Depends, HTTPException, Request
from ...schemas.stock.mark import MarkBase
from ...schemas.resources.result_object import ResultObject
from sqlalchemy.orm import Session
from typing import Dict
from ...app import get_db
from ...services.stock.mark import new, get_one_by_id, delete, update, get_all, associate_mark_product_by_id, desassociate_mark_product_by_id
from starlette import status
from ...auth_bearer import JWTBearer
  
mark_route = APIRouter(
    tags=["Nomenclators"],
    dependencies=[Depends(JWTBearer())]   
)

@mark_route.get("/mark", response_model=Dict, summary="Get list marks of products")
def get_classification(
    request: Request,
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(request=request, page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)


@mark_route.post("/mark", response_model=ResultObject, summary="Create a marks of products")
def create_mark(request:Request, mark: MarkBase, db: Session = Depends(get_db)):
    return new(request=request, mark=mark, db=db)

@mark_route.get("/mark/{id}", response_model=ResultObject, summary="Get a marks of products for your ID.")
def get_mark_by_id(request:Request, id: int, db: Session = Depends(get_db)):
    return get_one_by_id(request, id=id, db=db)

@mark_route.delete("/mark/{id}", response_model=ResultObject, summary="Remove marks of products for your ID")
def delete_mark(request:Request, id: int, db: Session = Depends(get_db)):
    return delete(request=request, id=id, db=db)
    
@mark_route.put("/mark/{id}", response_model=ResultObject, summary="Update marks of products for your ID")
def update_mark(request:Request, id: int, mark: MarkBase, db: Session = Depends(get_db)):
    return update(request=request, db=db, id=id, mark=mark)

@mark_route.put("/mark/associate/{mark_id}{product_id}", response_model=ResultObject, summary="Associae marks and products for yours ID")
def associate_mark_product(request:Request, mark_id: int, product_id: str, db: Session = Depends(get_db)):
    return associate_mark_product_by_id(request=request, db=db, mark_id=mark_id, product_id=product_id)

@mark_route.put("/mark/associate/{mark_id}{product_id}", response_model=ResultObject, summary="Desassociae marks and products for yours ID")
def desassociate_mark_product(request:Request, mark_id: int, product_id: str, db: Session = Depends(get_db)):
    return desassociate_mark_product_by_id()(request=request, db=db, mark_id=mark_id, product_id=product_id)