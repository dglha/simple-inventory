from typing import Optional
from pydantic import BaseModel
from pydantic.types import constr
from datetime import date

class EmployeeCreateSchema(BaseModel):
    last_name: constr(min_length=2, max_length=64)
    first_name: constr(min_length=2, max_length=64)
    birth_date: Optional[date]
    phone: Optional[constr(max_length=32)]
    photo: Optional[constr(max_length=128)]

class EmployeeUpdateSchema(EmployeeCreateSchema):
    pass

class EmployeeInfoSchema(EmployeeCreateSchema):
    id: int

    class Config:
        orm_mode = True