from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base
from .subnet import Subnet

class Assignment(Base):
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    hostname = Column(String, nullable=False)
    subnet_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    subnet = relationship("Subnet", foreign_keys=subnet_id)

    __table_args__ = (
        ForeignKeyConstraint(
            [subnet_id],
            [Subnet.id],
            onupdate="CASCADE", 
            ondelete="RESTRICT"
        ),
    )
