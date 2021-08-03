from typing import Optional, Text
from pydantic import BaseModel, constr
from pydantic.class_validators import validator
from pydantic.types import Json

class ProductBaseSchema(BaseModel):
    product_name: constr(min_length=3, max_length=128)
    supplier_id: int
    category_id: int
    quantity_per_unit: Optional[constr(max_length=32)] = ''
    unit_quoted_price: float
    units_in_stock: int
    description: Optional[Text] = ''

    @validator('unit_quoted_price')
    def price_must_be_greater_than_zero(cls, price):
        if price <= 0 :
            raise ValueError('Unit quoted price must be greater than 0')
        return price

    @validator('units_in_stock')
    def unit_in_stock_must_be_greater_than_zero(cls, stock):
        if stock < 0 :
            raise ValueError('Units in stock must be greater than 0')
        return stock

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductUpdateSchema(ProductCreateSchema):
    pass

class ProductSchema(ProductBaseSchema):
    id: int
    image: dict

    class Config:
        orm_mode = True