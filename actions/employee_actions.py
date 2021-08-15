from schema.employee_schema import (
    EmployeeCreateSchema,
    EmployeeInfoSchema,
    EmployeeUpdateSchema,
)
from models.employees import Employee
from app import db


"""
    CRUD
"""


def create_new_employee(employee_request: EmployeeCreateSchema):
    emp = Employee(**employee_request.dict())
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