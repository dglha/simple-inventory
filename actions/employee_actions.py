import re

import regex
from app import db
from flask.globals import request
from models.employee import Employee
from schema.employee_schema import EmployeeInfoSchema, EmployeeUpdateSchema
from utils import imagekit_utils
from utils.re_helper import is_valid_phone


"""
    CRUD
"""


def create_new_employee():
    last_name = request.form.get("last_name", None)
    first_name = request.form.get("first_name", None)
    phone = request.form.get("phone", None)
    image = request.files.get("image", None)

    if last_name is None or first_name is None or phone is None:
        return {"message": "Missing required params"}, 400

    if not is_valid_phone(phone):
        return {"message": "Invalid phone number"}, 400

    image_json = []
    if image:
        image_json = imagekit_utils.upload_image(image)
        if image_json["error"] is not None:
            return {
                "message": "An error occurred while uploading image, please try again"
            }, 500

    emp = Employee(last_name=last_name, first_name=first_name, phone=phone)
    if image_json:
        emp.image = image_json["response"]
    db.session.add(emp)
    db.session.commit()
    return EmployeeInfoSchema.from_orm(emp)


def get_employee_info(employee_id):
    emp = Employee.query.filter_by(id=employee_id).first()
    if not emp:
        return {"message": "Employee doesn't exists"}, 404
    return EmployeeInfoSchema.from_orm(emp)


def update_employee_info(employee_id, employee_request: EmployeeUpdateSchema):
    emp = Employee.query.filter_by(id=employee_id).first()
    if not emp:
        return {"message": "Employee doesn't exists"}, 404
    print(employee_request.dict())

    emp.last_name = employee_request.last_name
    emp.first_name = employee_request.first_name
    emp.birth_date = employee_request.birth_date
    emp.phone = employee_request.phone
    emp.photo = employee_request.photo

    db.session.add(emp)
    db.session.commit()
    return EmployeeInfoSchema.from_orm(emp)


def delete_employee(employee_id):
    emp = Employee.query.filter_by(id=employee_id).first()
    if not emp:
        return {"message": "Employee doesn't exists"}, 404
    db.session.delete(emp)
    db.session.commit()
    return {"message": "Employee deleted"}, 200


"""
    ACTIONS
"""
