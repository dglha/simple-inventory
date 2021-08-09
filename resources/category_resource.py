from sqlalchemy.ext.mutable import MutableList
from schema.product_schema import ProductsSchema
from models.products import Product
from models.categories import Category
from schema.category_schema import *
from typing import List
from flask_restful import Resource
from pydantic import parse_obj_as
from flask_pydantic import validate
from models.shippers import Shipper
from app import db


class Categories(Resource):
    def get(self):
        pass

    @validate(body=CategoryPostSchema)
    def post(self, body: CategoryPostSchema):
        category = Category(**body.dict())
        db.session.add(category)
        db.session.commit()
        return CategorySchema.from_orm(category)


class CategoryInfo(Resource):
    @validate(response_many=True)
    def get(self, category_id):
        # Get products of category
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return {"message": "Category not found"}, 404
        products = Product.query.join(Category).filter_by(id=category.id).all() 
        return parse_obj_as(List[ProductsSchema], products)

    @validate(body=CategoryPostSchema)
    def put(self, id, body: CategoryPostSchema):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return {"message": "Category not found"}, 404
        category.category_name = body.category_name
        category.description = body.description
        category.picture = body.picture
        db.session.add(category)
        db.session.commit()
        return CategorySchema.from_orm(category)

    def delete(self, id):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return {"message": "Category not found"}, 404
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted"}, 200
