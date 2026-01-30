from sqlalchemy import Column, Integer, String, Boolean
from .db import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, unique=True)
    user_id = Column(Integer, nullable=False)
    status = Column(String, default="pending")
    processed = Column(Boolean, default=False)
