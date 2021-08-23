from app import db

class PaymentLog(db.Model):
    __tablename__ = 'payment_log'

    user_id = db.Column(db.String(64), nullable = False)
    