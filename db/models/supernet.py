from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base
from .customer import Customer

class Supernet(Base):
    __tablename__ = "supernet"

    id = Column(Integer, primary_key=True)
    network = Column(String, nullable=False)
    mask = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    customer = relationship("Customer", foreign_keys=customer_id)

    __table_args__ = (
        ForeignKeyConstraint(
            [customer_id],
            [Customer.id],
            onupdate="CASCADE", 
            ondelete="RESTRICT"
        ),
    )
