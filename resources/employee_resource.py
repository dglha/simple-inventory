from models.employees import Employee
from flask_restful import Resource
from flask_pydantic import validate
from schema.employee_schema import *
from app import db

class EmployeeInfo(Resource):
    @validate()
    def get(self, employee_id):
        emp = Employee.query.filter_by(id = employee_id).first()
        if not emp:
            return {
                'message': 'Employee not found'
            }
        return EmployeeSchema.from_orm(emp)

    @validate(body=EmployeeUpdateSchema)
    def put(self, employee_id, body: EmployeeUpdateSchema):
        emp = Employee.query.filter_by(id = employee_id).first()
        if not emp:
            return {
                'message': 'Employee not found'
            }
        print(body.dict())
        
        emp.last_name = body.last_name
        emp.first_name = body.first_name
        emp.birth_date = body.birth_date
        emp.phone = body.phone
        emp.photo = body.photo
            
        db.session.add(emp)
        db.session.commit()
        return EmployeeSchema.from_orm(emp)

    def delete(self, employee_id):
        emp = Employee.query.filter_by(id = employee_id).first()
        if not emp:
            return {
                'message': 'Employee not found'
            }
        db.session.delete(emp)
        db.session.commit()
        return {
            'message': 'Employee deleted'
        }

class Employees(Resource):
    @validate(body=EmployeeCreateSchema)
    def post(self, body: EmployeeCreateSchema):
        emp = Employee(**body.dict())
        db.session.add(emp)
        db.session.commit()

        return EmployeeSchema.from_orm(emp)