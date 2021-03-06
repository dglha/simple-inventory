from app import db
from models.orders import Order

class Customer(db.Model):
    __tablename__ = 'customers'
    user_uid = db.Column(db.Integer, primary_key = True)
    user_uuid = db.Column(db.String(64))
    company_name = db.Column(db.String(128))
    contact_name = db.Column(db.String(64))
    contact_title = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(16))
    country = db.Column(db.String(16))
    postal_code = db.Column(db.String(10))
    phone = db.Column(db.String(24))
    
    # One to Many relationship to Orders table
    # orders = db.relationship(Order, backref = 'customer')
