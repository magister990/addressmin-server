import ipaddress
from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

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

    @validates('address')
    def validate_address(self, field_name, value):
        # TODO validate if the address is actually inside the supernet.
        address = ipaddress.ip_address(value)
        return self.validate_unique(field_name, value)

    @validates('supernet_id')
    def validate_supernet_id(self, field_name, value):
        return self.validate_exists(
            field_name,
            value,
            other_class = Supernet,
            other_field = Supernet.id)
