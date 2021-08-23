from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import backref
from models.product import Product
from sqlalchemy.dialects.postgresql import JSONB
from app import db


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    picture = db.Column(MutableDict.as_mutable(JSONB))
    # One to many relationship
    products = db.relationship(Product, backref="category")
