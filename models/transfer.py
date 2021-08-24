from app import db

class Transfer(db.Model):
    __tablename__ = 'transfer'
    id = db.Column(db.BigInteger, primary_key = True)
    sender = db.Column(db.String(64), nullable = False)
    receiver = db.Column(db.String(64), nullable = False)
    currency = db.Column(db.String(64), nullable = False)
    total = db.Column(db.Float, nullable = False) 
    method = db.Column(db.String(64), nullable = False)