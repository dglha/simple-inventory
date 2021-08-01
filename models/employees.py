from models.orders import Order
from sqlalchemy.orm import backref
from app import db

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(32))
    photo = db.Column(db.String(128))

    # One to many relationship to Orders table
    orders = db.relationship(Order, backref = 'employee')
