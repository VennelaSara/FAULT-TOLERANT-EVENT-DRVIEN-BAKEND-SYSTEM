from pydantic import BaseModel

class ShippingCreate(BaseModel):
    order_id: int
    user_id: int
    item: str
    quantity: int
    address: str

class ShippingStatus(BaseModel):
    shipping_id: int
    order_id: int
    status: str
