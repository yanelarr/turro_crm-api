"""coding=utf-8."""

from email.policy import default
from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Integer, Boolean
from ...config.db import Base

class Municipality(Base):
    """Municipality Class contains standard information for a Municipality."""
 
    __tablename__ = "municipality"
    __table_args__ = {'schema' : 'resources'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    province_id = Column(Integer, ForeignKey("resources.province.id"))
    is_active = Column(Boolean, nullable=False, default=True)
    
    created_by = Column(String(50), nullable=False, default='foo')
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    updated_by = Column(String(50), nullable=False, default='foo')
    updated_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "province_id": self.province_id,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_by": self.updated_by,
            "updated_date": self.updated_date
        }
    