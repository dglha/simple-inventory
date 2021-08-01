from sqlalchemy.orm import backref
from models.products import Product
from app import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    picture = db.Column(db.String(128))

    # One to many relationship 
    products = db.relationship(Product, backref = 'category')
