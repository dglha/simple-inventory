from models.shipper import Shipper
from schema.shippers_schema import ShipperCreateSchema, ShipperInfoSchema, ShipperUpdateSchema
from app import db

"""
    CRUD
"""

# Create
def create_new_shipper(shipper_request: ShipperCreateSchema):
    shipper = Shipper(**shipper_request.dict())
    db.session.add(shipper)
    db.session.commit()
    return ShipperInfoSchema.from_orm(shipper)

# Update
def update_shipper_info(shipper_id, shipper_request: ShipperUpdateSchema):
    shipper = Shipper.query.filter_by(id = shipper_id).first()
    if shipper is None:
        return{'message': 'Shipper doesn\'t exists'}, 404
    shipper.company_name = shipper_request.company_name
    shipper.phone = shipper_request.phone
    db.session.add(shipper)
    db.session.commit()
    return ShipperInfoSchema.from_orm(shipper)

# Delete
def delete_shipper(shipper_id):
    shipper = Shipper.query.filter_by(id = shipper_id).first()
    if shipper is None:
        return{'message': 'Shipper doesn\'t exists'}, 404
    db.session.delete(shipper)
    db.session.commit()
    return {"message": "Shipper deleted!"}, 200

# Read
def get_shipper_info(shipper_id):
    shipper = Shipper.query.filter_by(id = shipper_id).first()
    if shipper is None:
        return{'message': 'Shipper doesn\'t exists'}, 404
    return ShipperInfoSchema.from_orm(shipper)

"""
    ACTIONS
"""