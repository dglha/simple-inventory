from models.categories import Category
from schema.category_schema import CategoryModel, CategoryPostModel, CategoryQueryModel
from typing import List
from flask_restful import Resource
from pydantic import parse_obj_as
from flask_pydantic import validate
from models.shippers import Shipper
from app import db

class Categories(Resource):
    def get(self):
        pass

    @validate(body=CategoryPostModel)
    def post(self, body: CategoryPostModel):
        category = Category(**body.dict())
        db.session.add(category)
        db.session.commit()
        return CategoryModel.from_orm(category)
class CategoryInfo(Resource):
    @validate()
    def get(self, id):
        category = Category.query.filter_by(id = id).first()
        if not category:
            return {
                'message': 'Category not found'
            }, 404
        return CategoryModel.from_orm(category)

    @validate(body=CategoryPostModel)
    def put(self, id, body: CategoryPostModel):
        category = Category.query.filter_by(id = id).first()
        if not category:
            return {
                'message': 'Category not found'
            }, 404
        category.category_name = body.category_name
        category.description = body.description
        category.picture = body.picture
        db.session.add(category)
        db.session.commit()
        return CategoryModel.from_orm(category)

    def delete(self, id):
        category = Category.query.filter_by(id = id).first()
        if not category:
            return {
                'message': 'Category not found'
            }, 404
        db.session.delete(category)
        db.session.commit()
        return {
            'message': 'Category deleted'
        }, 200