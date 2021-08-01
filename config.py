import os

class Config():
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:212001@localhost:5432/digicierge'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'digicierge inventory'