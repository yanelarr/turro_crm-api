from datetime import datetime
import math

from fastapi import HTTPException, Request
from unicodedata import name
from fastapi import HTTPException

from ...models.stock.classification import Classification
from ...schemas.stock.classification import ClassificationBase, ClassificationShema
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
    str_query = "Select id, name, code, description "
    
    str_from = "FROM stock.classification cla WHERE cla.is_active = True "
    
    str_count += str_from
    str_query += str_from
    
    dict_query = {'name': " AND cla.name ilike '%" + criteria_value + "%'",
                  'code': " AND cla.code ilike '%" + criteria_value + "%'"}
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    str_count += dict_query[criteria_key] if criteria_value else ''
    str_query += dict_query[criteria_key] if criteria_value else ''
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY cla.name"
    
    if page != 0:
        str_query += " LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
         
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, page) for item in lst_data]
    
    return result

def create_dict_row(item, page):
    
    new_row = {'id': item['id'], 'name' : item['name'], 'code' : item['code'], 'description': item['description']}
    if page != 0:
        new_row['selected'] = False
    return new_row
    
def get_one(id: int, db: Session):  
    return db.query(Classification).filter(Classification.id == id).first()

def get_one_by_id(request, id: int, db: Session):  
    result = ResultObject() 
    result.data = db.query(Classification).filter(Classification.id == id).first()
    return result

def new(request, db: Session, classification: ClassificationBase):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_class = Classification(name=classification.name, code=classification.code, description=classification.description, 
                              created_by=currentUser['username'], updated_by=currentUser['username'])
    
    try:
        db.add(db_class)
        db.commit()
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "classification.error_new_classification")
        raise HTTPException(status_code=403, detail=msg)
    
def delete(request: Request, id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    try:
        db_class = db.query(Classification).filter(Classification.id == id).first()
        if db_class:
            db_class.is_active = False
            db_class.updated_by = currentUser['username']
            db_class.updated_date = datetime.now()
            db.commit()
            return result
        else:
            raise HTTPException(status_code=404, detail=_(locale, "classification.not_found"))
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "classification.imposible_delete"))
    
def update(request: Request, id: str, classification: ClassificationBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    db_class = db.query(Classification).filter(Classification.id == id).first()
    
    if db_class:
        db_class.name = classification.name
        db_class.code = classification.code
        db_class.description = classification.description
        
        db_class.updated_by = currentUser['username']
        db_class.updated_date = datetime.now()
            
        try:
            db.add(db_class)
            db.commit()
            return result
        except (Exception, SQLAlchemyError) as e:
            print(e.code)
            if e.code == "gkpj":
                raise HTTPException(status_code=400, detail=_(locale, "classification.already_exist"))
    else:
        raise HTTPException(status_code=404, detail=_(locale, "classification.not_found"))
