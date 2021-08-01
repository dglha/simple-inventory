from flask import Flask
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_migrate import Migrate, migrate
from config import Config
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from models.employees import Employee
from models.customers import Customer
from models.shippers import Shipper
from models.categories import Category
from models.products import Product
from models.suppliers import Supplier
from models.order_details import OrderDetail
from models.orders import Order

from resources.shipper_resource import ShipperInfo, Shippers
from resources.category_resource import CategoryInfo, Categories

api.add_resource(ShipperInfo, '/shipper')
api.add_resource(Shippers, '/shippers')

api.add_resource(CategoryInfo, '/category')
api.add_resource(Categories, '/category/all')


