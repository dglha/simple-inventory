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

from resources.shipper_resource import ShipperInfo, Shippers
from resources.category_resource import CategoryInfo, Categories
from resources.customer_resource import CustomerInfo, Customers
from resources.employee_resource import EmployeeInfo, Employees
from resources.supplier_resource import SupplierInfo, Suppliers, SupplierProduct
from resources.product_resource import ProductInfo, Products, ProductImage
from resources.order_resource import Orders, OrderInfo

api.add_resource(Shippers, '/shipper')
api.add_resource(ShipperInfo, '/shipper/<int:shipper_id>')

api.add_resource(CategoryInfo, '/category/<int:category_id>')
api.add_resource(Categories, '/category')

api.add_resource(CustomerInfo, '/customer/<int:customer_id>')
api.add_resource(Customers, '/customer')

api.add_resource(Employees, '/employee')
api.add_resource(EmployeeInfo, '/employee/<int:employee_id>')

api.add_resource(Suppliers, '/supplier')
api.add_resource(SupplierInfo, '/supplier/<int:supplier_id>')
api.add_resource(SupplierProduct, '/supplier/<int:supplier_id>/product')

api.add_resource(Products, '/product')
api.add_resource(ProductInfo, '/product/<int:product_id>')
api.add_resource(ProductImage, '/product/<int:product_id>/images')

api.add_resource(Orders, '/order')
api.add_resource(OrderInfo, '/order/<int:order_id>')