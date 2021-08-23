from actions.order_actions import create_new_order, get_order_info
from pydantic.tools import parse_obj_as
from models.order_detail import OrderDetail
from models.order import Order
from models.product import Product
from flask_pydantic import validate
from flask_restful import Resource
from schema.order_schema import *
from app import db


class Orders(Resource):
    # Validate request using OrderCreateSchema
    @validate(body=OrderCreateSchema)
    def post(self, body: OrderCreateSchema):
       return create_new_order(body)


class OrderInfo(Resource):
    @validate()
    def get(self, order_id):
        return get_order_info(order_id=order_id)