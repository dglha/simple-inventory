import os
from settings import DB_PWD
class Config():
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{DB_PWD}@18.190.26.255:5432/inventory'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'digicierge inventory'