from app import api

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