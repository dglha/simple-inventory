from actions.supplier_actions import create_new_supplier, delete_supplier, get_supplier_info, get_supplier_products, update_supplier_info
from schema.product_schema import ProductsSchema
from typing import List
from pydantic.tools import parse_obj_as
from models.product import Product
import flask_pydantic
from models.supplier import Supplier
from flask_restful import Resource
from flask_pydantic import validate
from schema.supplier_schema import *
from flask import request
from app import db

class SupplierInfo(Resource):
    @validate()
    def get(self, supplier_id):
        return get_supplier_info(supplier_id)

    @validate(body=SuppplierUpdateSchema)
    def put(self, supplier_id, body: SuppplierUpdateSchema):
        return update_supplier_info(supplier_id, body)

    def delete(self, supplier_id):
        return delete_supplier(supplier_id)

class Suppliers(Resource):
    @validate()
    def post(self):
        return create_new_supplier()

class SupplierProduct(Resource):
    # @validate(response_many=True)
    @validate()
    def get(self, supplier_id, page = 0, limit = 5):
        page = request.args.get('page', 0, type=int)
        if page <= 0:
            page = 1
        return get_supplier_products(supplier_id, page, limit)