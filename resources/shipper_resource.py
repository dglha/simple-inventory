from typing import List
from flask_restful import Resource
from pydantic import parse_obj_as
from flask_pydantic import validate
from schema.shippers_schema import ShipperGetModel, ShipperPostModel
from models.shippers import Shipper
from app import db

class ShipperInfo(Resource):
    @validate(body=ShipperPostModel)
    def post(self, body: ShipperPostModel):
        shipper = Shipper(**body.dict())
        db.session.add(shipper)
        db.session.commit()
        return ShipperGetModel.from_orm(shipper)

    @validate(query=ShipperGetModel)
    def get(self, query: ShipperGetModel):
        shipper = Shipper.query.filter_by(id=query.id).first()
        return ShipperGetModel.from_orm(shipper)

class Shippers(Resource):
        @validate(response_many=True)
        def get(self, offset = 0, limit = 10):
            shippers = Shipper.query.offset(offset).limit(limit).all()

            return parse_obj_as(List[ShipperGetModel], shippers)