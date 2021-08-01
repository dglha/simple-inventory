from typing import Optional
from pydantic import BaseModel, validator
from pydantic.types import constr

class ShipperPostModel(BaseModel):
    company_name: constr(max_length=128, min_length=5)
    phone: constr(max_length=15)

class ShipperGetModel(BaseModel):
    id: int
    company_name: Optional[str]
    phone: Optional[str]

    @validator('id')
    def id_must_be_greater_than_zero(cls, id):
        if id<= 0 :
            raise ValueError('Id must be greater than 0')
        return id

    class Config:
        orm_mode = True