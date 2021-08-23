import os

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

class Config():
    # SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/inventory'
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:212001@localhost:5432/inventory'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'digicierge inventory'