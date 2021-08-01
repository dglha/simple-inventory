from models.order_details import OrderDetail
from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable = False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable = False)
    shipper_id = db.Column(db.Integer, db.ForeignKey('shippers.id'), nullable = False)
    order_date = db.Column(db.DateTime(), default = datetime.utcnow)

    order_details = db.relationship(OrderDetail, backref='order')