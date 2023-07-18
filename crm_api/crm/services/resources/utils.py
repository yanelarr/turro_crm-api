
import math
import os
import shutil
from fastapi import FastAPI, Request, UploadFile, File
from os import getcwd, remove

# from fastapi import Request
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ...schemas.resources.result_object import ResultData, ResultObject

def get_result_count(page: int, per_page: int, str_count: str, db: Session): 
    if page != 0:
        result = ResultData(page=page, per_page=per_page)  
        
        result.total = db.execute(str_count).scalar()
        result.total_pages=result.total/result.per_page if (result.total % result.per_page == 0) else math.trunc(result.total / result.per_page) + 1
    else:
        result = ResultObject()
        
    return result
