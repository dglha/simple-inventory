from app import db
from models.order_detail import OrderDetail
from datetime import datetime
from sqlalchemy import func
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key = True)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable = False)
    user_uid = db.Column(db.String(128), nullable = False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable = False)
    shipper_id = db.Column(db.Integer, db.ForeignKey('shipper.id'), nullable = False)
    shipping_address_id = db.Column(db.String(128), nullable = False)
    community_id = db.Column(db.String(128))
    payment_method = db.Column(db.String(128))
    order_date = db.Column(db.DateTime(), default = func.now())

    # shipping address

    order_details = db.relationship(OrderDetail, backref='order')