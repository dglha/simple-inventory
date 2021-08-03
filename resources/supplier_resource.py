import flask_pydantic
from models.suppliers import Supplier
from flask_restful import Resource
from flask_pydantic import validate
from schema.supplier_schema import *
from app import db

class SupplierInfo(Resource):
    @validate()
    def get(self, supplier_id):
        sup = Supplier.query.filter_by(id = supplier_id).first()
        if not sup:
            return {
                'message': 'Supplier not found'
            }
        return SupplierSchema.from_orm(sup)

    @validate(body=SuppplierUpdateSchema)
    def put(self, supplier_id, body: SuppplierUpdateSchema):
        sup = Supplier.query.filter_by(id = supplier_id).first()
        if not sup:
            return {
                'message': 'Supplier not found'
            }
        
        sup.company_name = body.company_name
        sup.contact_name = body.contact_name
        sup.contact_title = body.contact_title
        sup.address = body.address
        sup.city = body.city
        sup.country = body.country
        sup.postal_code = body.postal_code
        sup.phone = body.phone
        sup.homepage = body.homepage

        db.session.add(sup)
        db.session.commit()

        return SupplierSchema.from_orm(sup)

    def delete(self, supplier_id):
        sup = Supplier.query.filter_by(id = supplier_id).first()
        if not sup:
            return {
                'message': 'Supplier not found'
            }
        db.session.delete(sup)
        db.session.commit()

        return {
            'message': 'Supplier deleted'
        }

class Suppliers(Resource):
    @validate(body=SupplierCreateSchema)
    def post(self, body: SupplierCreateSchema):
        sup = Supplier(**body.dict())
        db.session.add(sup)
        db.session.commit()

        return SupplierSchema.from_orm(sup)