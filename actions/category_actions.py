from pydantic.tools import parse_obj_as
from schema.product_schema import ProductsSchema
from models.products import Product
from schema.category_schema import *
from app import db

"""
    CRUD
"""


def create_new_category(category_request: CategoryPostSchema):
    category = Category(**category_request.dict())
    db.session.add(category)
    db.session.commit()
    return CategorySchema.from_orm(category)


def delete_category(category_id):
    category = Category.query.filter_by(id=id).first()
    if not category:
        return {"message": "Category not found"}, 404
    db.session.delete(category)
    db.session.commit()
    return {"message": "Category deleted"}, 200


def update_category_info(category_id, category_request: CategoryPostSchema):
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return {"message": "Category not found"}, 404
    category.category_name = category_request.category_name
    category.description = category_request.description
    category.picture = category_request.picture
    db.session.add(category)
    db.session.commit()
    return CategorySchema.from_orm(category)


"""
    ACTIONS
"""


def get_category_products(categroy_id: int, term: str, offset: int, limit: int):
    category = Category.query.filter_by(id=categroy_id).first()
    if category is None:
        return {"message": "Category doesn't exists"}, 404
    products = (
        Product.query.join(Category)
        .filter_by(id=category.id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return parse_obj_as(List[ProductsSchema], products)

def get_category_list(offset:int , limit: int):
    categories = Category.query.offset(offset).limit(limit).all()
    return parse_obj_as(List[CategorySchema], categories)
