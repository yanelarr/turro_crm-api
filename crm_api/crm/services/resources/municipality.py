from datetime import datetime
import math

from fastapi import HTTPException, Request
from unicodedata import name
from fastapi import HTTPException

from ...models.resources.municipality import Municipality
from ...schemas.resources.municipality import MunicipalityBase, MunicipalityShema
from ...schemas.resources.result_object import ResultData, ResultObject

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext

from ...auth_bearer import decodeJWT
from ...functions_jwt import get_current_user
from ...app import _
from ...services.resources.utils import get_result_count

from ...services.resources.province import get_one as get_one_province

def get_all(request:Request, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_count = "Select count(mun.*) "
    str_query = "Select mun.id mun_id, mun.name mun_name, mun.description mun_descrip, province_id, " +\
        "prov.name prov_name "
    
    str_from = "FROM resources.municipality mun JOIN resources.province prov ON mun.province_id = prov.id " +\
        "WHERE mun.is_active = True "
    
    str_count += str_from
    str_query += str_from
    
    dict_query = {'name': " AND mun.name ilike '%" + criteria_value + "%'",
                  'prov_name': " AND prov_name ilike '%" + criteria_value + "%'"}
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    str_count += dict_query[criteria_key] if criteria_value else ''
    str_query += dict_query[criteria_key] if criteria_value else ''
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY prov_name, mun.id"
    
    if page != 0:
        str_query += " LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
         
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, page) for item in lst_data]
    
    return result

def create_dict_row(item, page):
    
    new_row = {'id': item['mun_id'], 'name' : item['mun_name'], 'description': item['mun_descrip'],
               'province_id': item['province_id'], 'prov_name' : item['prov_name']}
    if page != 0:
        new_row['selected'] = False
    return new_row
    
def get_one(id: int, db: Session):  
    return db.query(Municipality).filter(Municipality.id == id).first()

def get_one_by_id(id: int, db: Session):  
    result = ResultObject() 
    result.data = db.query(Municipality).filter(Municipality.id == id).first()
    return result

def get_municipalities_by_province_id(request, province_id: int, db: Session):  
    
    result = ResultObject() 
    result.data = []
    
    str_query = "Select mun.id mun_id, mun.name mun_name " +\
        "FROM resources.municipality mun " +\
        "WHERE mun.is_active = True AND province_id = " + str(province_id)
        
    lst_data = db.execute(str_query)
    for item in lst_data:
        result.data.append({'id': item['mun_id'], 'name' : item['mun_name']})
    
    return result

def new(request, db: Session, municipality: MunicipalityBase):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    province = get_one_province(municipality.province_id, db=db)
    if not province:
        HTTPException(status_code=404, detail=_(locale, "province.not_found"))
    
    db_municipality = Municipality(name=municipality.name, description=municipality.description, 
                                   province_id = municipality.province_id,
                                   created_by=currentUser['username'], updated_by=currentUser['username'])
    
    try:
        db.add(db_municipality)
        db.commit()
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "municipality.error_new_municipality")
        raise HTTPException(status_code=403, detail=msg)
    
def delete(request: Request, id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    try:
        db_municipality = db.query(Municipality).filter(Municipality.id == id).first()
        if db_municipality:
            db_municipality.is_active = False
            db_municipality.updated_by = currentUser['username']
            db_municipality.updated_date = datetime.now()
            db.commit()
            return result
        else:
            raise HTTPException(status_code=404, detail=_(locale, "municipality.not_found"))
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "municipality.imposible_delete"))
    
def update(request: Request, id: str, municipality: MunicipalityBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    db_municipality = db.query(Municipality).filter(Municipality.id == id).first()
    
    if db_municipality:
        db_municipality.name = municipality.name
        db_municipality.description = municipality.description
        
        db_municipality.updated_by = currentUser['username']
        db_municipality.updated_date = datetime.now()
            
        try:
            db.add(db_municipality)
            db.commit()
            return result
        except (Exception, SQLAlchemyError) as e:
            print(e.code)
            if e.code == "gkpj":
                raise HTTPException(status_code=400, detail=_(locale, "municipality.already_exist"))
    else:
        raise HTTPException(status_code=404, detail=_(locale, "municipality.not_found"))
