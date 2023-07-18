from datetime import datetime
import math

from fastapi import HTTPException, Request
from unicodedata import name
from fastapi import HTTPException

from ...models.stock.mark import Marks, ProductMarks
from ...schemas.stock.mark import MarkBase, ProductMarksShema
from ...schemas.resources.result_object import ResultData, ResultObject

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext

from ...auth_bearer import decodeJWT
from ...functions_jwt import get_current_user
from ...app import _
from ...services.resources.utils import get_result_count

def get_all(request:Request, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_count = "Select count(*) "
    str_query = "Select id, name, description "
    
    str_from = "FROM stock.marks mar WHERE mar.is_active = True "
    
    str_count += str_from
    str_query += str_from
    
    dict_query = {'name': " AND mar.name ilike '%" + criteria_value + "%'",
                  'description': " AND mar.description ilike '%" + criteria_value + "%'"}
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    str_count += dict_query[criteria_key] if criteria_value else ''
    str_query += dict_query[criteria_key] if criteria_value else ''
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY mar.name"
    
    if page != 0:
        str_query += " LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
         
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, page) for item in lst_data]
    
    return result

def create_dict_row(item, page):
    
    new_row = {'id': item['id'], 'name' : item['name'], 'description': item['description']}
    if page != 0:
        new_row['selected'] = False
    return new_row
    
def get_one(id: int, db: Session):  
    return db.query(Marks).filter(Marks.id == id).first()

def get_one_by_id(request, id: int, db: Session):  
    result = ResultObject() 
    result.data = db.query(Marks).filter(Marks.id == id).first()
    return result

def new(request, db: Session, mark: MarkBase):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_mark = Marks(name=mark.name, description=mark.description, 
                    created_by=currentUser['username'], updated_by=currentUser['username'])
    
    try:
        db.add(db_mark)
        db.commit()
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "mark.error_new_mark")
        raise HTTPException(status_code=403, detail=msg)
    
def delete(request: Request, id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    try:
        db_mark = db.query(Marks).filter(Marks.id == id).first()
        if db_mark:
            db_mark.is_active = False
            db_mark.updated_by = currentUser['username']
            db_mark.updated_date = datetime.now()
            db.commit()
            return result
        else:
            raise HTTPException(status_code=404, detail=_(locale, "mark.not_found"))
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "mark.imposible_delete"))
    
def update(request: Request, id: str, mark: MarkBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    db_mark = db.query(Marks).filter(Marks.id == id).first()
    
    if db_mark:
        db_mark.name = mark.name
        db_mark.description = mark.description
        
        db_mark.updated_by = currentUser['username']
        db_mark.updated_date = datetime.now()
            
        try:
            db.add(db_mark)
            db.commit()
            return result
        except (Exception, SQLAlchemyError) as e:
            print(e.code)
            if e.code == "gkpj":
                raise HTTPException(status_code=400, detail=_(locale, "mark.already_exist"))
    else:
        raise HTTPException(status_code=404, detail=_(locale, "mark.not_found"))
    
def associate_mark_product_by_id(request: Request, mark_id: int, product_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    assoc_mark_prod = db.query(ProductMarks).filter(ProductMarks.mark_id == mark_id).\
        filter(ProductMarks.product_id == product_id).\
        filter(ProductMarks.is_active == True).first()
    
    if assoc_mark_prod:
        return True
    
    db_assoc_mark_prod = ProductMarks(mark_id=mark_id, product_id=product_id, is_active=True,
                                      created_by=currentUser['username'], updated_by=currentUser['username'])
    
    try:
        db.add(db_assoc_mark_prod)
        db.commit()
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "mark.error_new_mark")
        raise HTTPException(status_code=403, detail=msg)
    
def desassociate_mark_product_by_id(request: Request, mark_id: int, product_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    assoc_mark_prod = db.query(ProductMarks).filter(ProductMarks.mark_id == mark_id).\
        filter(ProductMarks.product_id == product_id).\
        filter(ProductMarks.is_active == True).first()
    
    if not assoc_mark_prod:
        return True
    
    try:
        assoc_mark_prod.is_active = False
        
        assoc_mark_prod.updated_by = currentUser['username']
        assoc_mark_prod.updated_date = datetime.now()
        
        db.add(assoc_mark_prod)
        db.commit()
        
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "mark.error_new_mark")
        raise HTTPException(status_code=403, detail=msg)
    