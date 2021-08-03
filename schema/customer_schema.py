from typing import Optional
from pydantic import BaseModel, validator
from pydantic.types import constr

class CustomerCreateSchema(BaseModel):
    company_name: constr(min_length=5, max_length=128)
    contact_name: constr(min_length=5, max_length=64)
    contact_title: constr(min_length=5, max_length=64)
    address: Optional[constr(max_length=64)]
    city: Optional[constr(max_length=16)]
    country: Optional[constr(max_length=64)]
    postal_code: Optional[constr(max_length=10)]
    phone: Optional[constr(max_length=24)]

class CustomerUpdateSchema(CustomerCreateSchema):
    pass

class CustomerSchema(CustomerCreateSchema):
    id: int

    class Config:
        orm_mode = True