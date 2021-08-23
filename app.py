from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_restful import Api
from imagekitio import ImageKit

from settings import (
    IMAGEKIT_PRIVATE_KEY,
    IMAGEKIT_PUBLIC_KEY,
    IMAGEKIT_URL
)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db = SQLAlchemy(app, session_options={"autoflush": False})
migrate = Migrate(app, db)
api = Api(app)

imagekit = ImageKit(
    private_key=IMAGEKIT_PRIVATE_KEY,
    public_key=IMAGEKIT_PUBLIC_KEY,
    url_endpoint=IMAGEKIT_URL
)

from models.employees import Employee
from models.customers import Customer
from models.shippers import Shipper
from models.categories import Category
from models.products import Product
from models.suppliers import Supplier
from models.order_details import OrderDetail
from models.orders import Order

import routes