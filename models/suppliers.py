from sqlalchemy.orm import backref
from models.products import Product
from app import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(128), nullable = False)
    contact_name = db.Column(db.String(128), nullable = False)
    contact_title = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(16))
    country = db.Column(db.String(16))
    postal_code = db.Column(db.String(10))
    phone = db.Column(db.String(24))
    homepage = db.Column(db.Text)
    email = db.Column(db.String(128))

    # One to many relationship to Products table
    products = db.relationship(Product, backref = 'supplier')