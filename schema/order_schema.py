from models.order_detail import OrderDetail
from typing import Optional, List
from pydantic import BaseModel, constr

class OrderDetailBaseSchema(BaseModel):
    product_id: int
    quantity: int
    price: float
    discount: float

class OrderDetailSchema(OrderDetailBaseSchema):
    # id: int

    class Config:
        orm_mode = True
        orm_model = OrderDetail

class OrderBaseSchema(BaseModel):
    # customer_id: int
    user_uid: constr(max_length=128)
    employee_id: int
    shipper_id: int
    shipping_address_id: constr(max_length=128)
    community_id: Optional[constr(max_length=128)]
    payment_method: constr(max_length=128)
    order_details: List[OrderDetailBaseSchema]

class OrderCreateSchema(OrderBaseSchema):
    pass

class OrderInfoSchema(BaseModel):
    id: int
    # customer_id: int
    user_uid: constr(max_length=128)
    employee_id: int
    shipper_id: int
    shipping_address_id: constr(max_length=128)
    community_id: Optional[constr(max_length=128)]
    payment_method: constr(max_length=128)
    order_details: List[OrderDetailSchema]

    class Config:
        orm_mode = True
