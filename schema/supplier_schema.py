from pydantic import BaseModel, constr
from typing import Optional, Text

from pydantic.networks import EmailStr

class SupplierBaseSchema(BaseModel):
    company_name: constr(min_length=3, max_length=128)
    contact_name: constr(min_length=3, max_length=64)
    contact_title: constr(min_length=3, max_length=64)
    address: Optional[constr(max_length=64)]
    city: Optional[constr(max_length=16)]
    country: Optional[constr(max_length=64)]
    postal_code: Optional[constr(max_length=10)]
    phone: Optional[constr(max_length=24)]
    homepage: Optional[Text]
    email: Optional[EmailStr]

class SupplierInfoSchema(SupplierBaseSchema):
    id: int

    class Config:
        orm_mode = True

class SuppplierUpdateSchema(SupplierBaseSchema):
    pass

class SupplierCreateSchema(SupplierBaseSchema):
    pass