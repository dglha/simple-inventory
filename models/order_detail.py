from app import db

class OrderDetail(db.Model):
    __tablename__ = 'order_detail'
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    quantity = db.Column(db.SmallInteger, nullable = False)
    price = db.Column(db.Float(15), nullable = False)
    discount = db.Column(db.Float)

    # One to One relationship to Products table