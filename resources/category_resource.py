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

class CategoryInfo(Resource):
    @validate(body=CategoryPostModel)
    def post(self, body: CategoryPostModel):
        category = Category(**body.dict())
        db.session.add(category)
        db.session.commit()
        return CategoryModel.from_orm(category)

    @validate(query=CategoryQueryModel)
    def get(self, query: CategoryQueryModel):
        category = Category.query.filter_by(id = query.id).first()
        if not category:
            return {
                'message': 'Category not found'
            }, 404
        return CategoryModel.from_orm(category)

    @validate(body=CategoryModel)
    def put(self, body: CategoryModel):
        category = Category.query.filter_by(id = body.id).first_or_404()
        return 200
