from models.orders import Order
from sqlalchemy.orm import backref
from app import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import func

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(32))
    image = db.Column(MutableDict.as_mutable(JSONB))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    # One to many relationship to Orders table
    orders = db.relationship(Order, backref = 'employee')
