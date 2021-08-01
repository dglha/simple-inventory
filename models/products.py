from app import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(128), nullable = False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    quantity_per_unit = db.Column(db.String(32))
    unit_quoted_price = db.Column(db.Float(15))
    units_in_stock = db.Column(db.SmallInteger)