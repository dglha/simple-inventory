from sqlalchemy.orm import backref
from models.order import Order
from app import db

class Shipper(db.Model):
    __tablename__ = 'shipper'
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(128), nullable = False)
    phone = db.Column(db.String(15))

    # One to many relationship to Orders table
    orders = db.relationship(Order, backref = 'shipper')