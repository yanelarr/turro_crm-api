"""coding=utf-8."""

from email.policy import default
from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Integer, Boolean
from ...config.db import Base

class Classification(Base):
    """classification Class contains standard information for a classification."""
 
    __tablename__ = "classification"
    __table_args__ = {'schema' : 'stock'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(30), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_by = Column(String(50), nullable=False, default='foo')
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False, default='foo')
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date
        }
