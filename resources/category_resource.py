from schema.category_schema import *
from flask_restful import Resource
from flask_pydantic import validate
from actions.category_actions import (
    create_new_category,
    delete_category,
    get_category_list,
    get_category_products,
    update_category_info,
)


class Categories(Resource):
    @validate(response_many=True)
    def get(self):
        return get_category_list(offset=0, limit=10)

    @validate(body=CategoryPostSchema)
    def post(self, body: CategoryPostSchema):
        return create_new_category(body)


class CategoryInfo(Resource):
    @validate(response_many=True)
    def get(self, category_id):
        return get_category_products(category_id, term="", offset=0, limit=10)

    @validate(body=CategoryPostSchema)
    def put(self, id, body: CategoryPostSchema):
        return update_category_info(id, body)

    def delete(self, id):
        return delete_category(id)
