from pydantic.types import constr
from models.categories import Category
from typing import List, Optional
from pydantic import validator
from pydantic.main import BaseModel


class CategoryPostSchema(BaseModel):
    category_name: constr(max_length=128, min_length=1)
    description: Optional[str]
    picture: Optional[str]

# For PUT, DELETE and response
class CategorySchema(CategoryPostSchema):
    id: int

    @validator('id')
    def id_must_be_greater_than_zero(cls, id):
        if id<= 0 :
            raise ValueError('Id must be greater than 0')
        return id

    class Config:
        orm_mode = True

class CategoryQuerySchema(BaseModel):
    id: int

    @validator('id')
    def id_must_be_greater_than_zero(cls, id):
        if id<= 0 :
            raise ValueError('Id must be greater than 0')
        return id
