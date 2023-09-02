from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base
from .customer import Customer
from .supernet import Supernet

class Subnet(Base):
    __tablename__ = "subnet"

    id = Column(Integer, primary_key=True)
    network = Column(String, nullable=False)
    mask = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    supernet_id = Column(Integer, nullable=False)
    advertised_from = Column(String, nullable=False)
    reserve_network_and_broadcast = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    customer = relationship("Customer", foreign_keys=customer_id)
    supernet = relationship("Supernet", foreign_keys=supernet_id)

    __table_args__ = (
        ForeignKeyConstraint(
            [customer_id],
            [Customer.id],
            onupdate="CASCADE", 
            ondelete="RESTRICT"
        ),
        ForeignKeyConstraint(
            [supernet_id],
            [Supernet.id],
            onupdate="CASCADE", 
            ondelete="RESTRICT"
        ),
    )
