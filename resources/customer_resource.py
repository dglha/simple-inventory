from app import db
from schema.customer_schema import CustomerCreateSchema, CustomerSchema, CustomerUpdateSchema
from models.customers import Customer
from typing import List
from flask_restful import Resource
from pydantic import parse_obj_as
from flask_pydantic import validate

class CustomerInfo(Resource):
    @validate()
    def get(self, customer_id):
        customer = Customer.query.filter_by(id = customer_id).first()
        if not customer:
            return {
                'message': 'Customer not found'
            }
        return CustomerSchema.from_orm(customer)
    
    @validate(body=CustomerUpdateSchema)
    def put(self, customer_id, body: CustomerUpdateSchema):
        customer = Customer.query.filter_by(id = customer_id).first()
        if not customer:
            return {
                'message': 'Customer not found'
            }
        customer.company_name = body.company_name
        customer.contact_name = body.contact_name
        customer.contact_title = body.contact_title
        customer.address= body.address
        customer.city = body.city
        customer.country = body.country
        customer.postal_code = body.postal_code
        customer.phone = body.phone

        db.session.add(customer)
        db.session.commit()
        return CustomerSchema.from_orm(customer)
    
    def delete(self, customer_id):
        customer = Customer.query.filter_by(id = customer_id).first()
        if not customer:
            return {
                'message': 'Customer not found'
            }
        db.session.delete(customer)
        db.session.commit()
        return {
            'message': 'Customer deleted'
        }

class Customers(Resource):
    @validate(body=CustomerCreateSchema)
    def post(self, body: CustomerCreateSchema):
        customer = Customer(**body.dict())
        db.session.add(customer)
        db.session.commit()

        return CustomerSchema.from_orm(customer)