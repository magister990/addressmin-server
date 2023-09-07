from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

from .base import Base

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    @validates('name')
    def validate_name(self, field_name, value):
        return self.validate_unique(field_name, value)
