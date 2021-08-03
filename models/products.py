from datetime import datetime
from app import db
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(128), nullable = False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    quantity_per_unit = db.Column(db.String(32))
    unit_quoted_price = db.Column(db.Float(15))
    units_in_stock = db.Column(db.SmallInteger)
    description = db.Column(db.Text, default = '')
    image = db.Column(JSONB)
    # timestamp https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime/33532154#33532154
    last_edited = db.Column(db.DateTime, default=func.now(), onupdate=func.now())