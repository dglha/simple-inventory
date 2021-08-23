from actions.shippper_actions import create_new_shipper, delete_shipper, get_shipper_info, update_shipper_info
from typing import List
from flask_restful import Resource
from pydantic import parse_obj_as
from flask_pydantic import validate
from schema.shippers_schema import ShipperCreateSchema, ShipperUpdateSchema
from models.shipper import Shipper
from app import db

class ShipperInfo(Resource):
    @validate()
    def get(self, shipper_id):
        return get_shipper_info(shipper_id)

    @validate(body=ShipperUpdateSchema)
    def put(self, shipper_id, body: ShipperUpdateSchema):
        return update_shipper_info(shipper_id, body)

    def delete(self, shipper_id):
        return delete_shipper(shipper_id)

class Shippers(Resource):
    @validate(body=ShipperCreateSchema)
    def post(self, body: ShipperCreateSchema):
        return create_new_shipper(body)