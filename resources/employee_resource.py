from actions.employee_actions import (
    create_new_employee,
    delete_employee,
    get_employee_info,
    update_employee_info,
)
from models.employee import Employee
from flask_restful import Resource
from flask_pydantic import validate
from schema.employee_schema import *
from app import db


class EmployeeInfo(Resource):
    @validate()
    def get(self, employee_id):
        return get_employee_info(employee_id)

    @validate(body=EmployeeUpdateSchema)
    def put(self, employee_id, body: EmployeeUpdateSchema):
        return update_employee_info(employee_id, body)

    def delete(self, employee_id):
        return delete_employee(employee_id)


class Employees(Resource):
    @validate()
    def post(self):
        return create_new_employee()
