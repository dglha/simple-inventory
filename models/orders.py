from app import db
from models.order_details import OrderDetail
from datetime import datetime
from sqlalchemy import func
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable = False)
    user_uid = db.Column(db.String(128), nullable = False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable = False)
    shipper_id = db.Column(db.Integer, db.ForeignKey('shippers.id'), nullable = False)
    shipping_address_id = db.Column(db.String(128), nullable = False)
    order_date = db.Column(db.DateTime(), default = func.now())

    # shipping address

    order_details = db.relationship(OrderDetail, backref='order')