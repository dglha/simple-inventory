from actions.product_actions import (
    add_new_image_to_product,
    create_new_product,
    delele_image_of_product,
    delete_product,
    get_images_of_product,
    get_product_info,
    get_product_list,
    update_product_info,
)
from flask import request
from flask_restful import Resource
from flask_pydantic import validate
from schema.product_schema import *


class ProductInfo(Resource):
    @validate()
    def get(self, product_id):
        return get_product_info(product_id)

    # PUT method using ProductUpdateSchema to validate request
    @validate(body=ProductUpdateSchema)
    def put(self, product_id, body: ProductUpdateSchema):
        return update_product_info(product_id, request_body=body)

    def delete(self, product_id):
        return delete_product(product_id)


class Products(Resource):
    @validate()
    def post(self):
        return create_new_product()

    @validate(response_many=True)
    def get(self, offset=0, limit=11):
        return get_product_list(offset, limit)


class ProductImage(Resource):
    def post(self, product_id):
        images = request.files.getlist("image")
        return add_new_image_to_product(product_id, images=images)

    def get(self, product_id):
        return get_images_of_product(product_id)

    def delete(self, product_id):
        file_id = request.json["file_id"]
        return delele_image_of_product(product_id, image_id=file_id)
