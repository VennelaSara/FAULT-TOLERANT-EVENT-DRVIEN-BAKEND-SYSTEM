from sqlalchemy import Column, Integer, String, Boolean
from .db import Base

class Shipping(Base):
    __tablename__ = "shipping"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, unique=True)
    user_id = Column(Integer, nullable=False)
    item = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    status = Column(String, default="pending")
    processed = Column(Boolean, default=False)
