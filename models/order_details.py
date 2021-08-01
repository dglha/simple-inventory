from app import db

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)
    quantity = db.Column(db.SmallInteger, nullable = False)
    price = db.Column(db.Float(15), nullable = False)
    discound = db.Column(db.Float)

    # One to One relationship to Products table