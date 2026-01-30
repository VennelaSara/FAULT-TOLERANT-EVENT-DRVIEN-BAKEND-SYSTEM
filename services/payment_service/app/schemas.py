from pydantic import BaseModel

class PaymentCreate(BaseModel):
    order_id: int
    user_id: int
