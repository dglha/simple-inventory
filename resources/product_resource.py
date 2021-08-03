from datetime import datetime

from flask import request
from models.suppliers import Supplier
from models.categories import Category
from models.products import Product
from flask_restful import Resource
from flask_pydantic import validate
from schema.product_schema import *
from app import db, imagekit


class ProductInfo(Resource):
    @validate()
    def get(self, product_id):
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return {"message": "Product not found"}, 404

        return ProductSchema.from_orm(product)

    @validate(body=ProductUpdateSchema)
    def put(self, product_id, body: ProductUpdateSchema):
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return {"message": "Product not found"}, 404

        cate = Category.query.filter_by(id=body.category_id).first()
        if not cate:
            return {"message": "Category does not exist"}, 400

        sup = Supplier.query.filter_by(id=body.supplier_id).first()
        if not sup:
            return {"message": "Supplier does not exist"}, 400

        product.product_name = body.product_name
        product.supplier_id = body.supplier_id
        product.category_id = body.category_id
        product.quantity_per_unit = body.quantity_per_unit
        product.unit_quoted_price = body.unit_quoted_price
        product.units_in_stock = body.units_in_stock
        product.description = body.description
        product.last_edited = datetime.utcnow()

        db.session.add(product)
        db.session.commit()

    def delete(self, product_id):
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return {"message": "Product not found"}, 404
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}


class Products(Resource):
    @validate()
    def post(self):
        # Get data from form
        product_name = request.form.get("product_name", "")
        supplier_id = request.form.get("supplier_id", "")
        category_id = request.form.get("category_id", "")
        quantity_per_unit = request.form.get("quantity_per_unit", "")
        unit_quoted_price = request.form.get("unit_quoted_price", "")
        units_in_stock = request.form.get("units_in_stock", "")
        description = request.form.get("description", "")
        image = request.files.get("image", None)

        # Validate

        # dung form
        cate = Category.query.filter_by(id=category_id).first()
        if not cate:
            return {"message": "Category does not exist"}, 400

        sup = Supplier.query.filter_by(id=supplier_id).first()
        if not sup:
            return {"message": "Supplier does not exist"}, 400

        # Upload image
        image_json = imagekit.upload_file(
            file=image,
            file_name=image.filename,
            options={
                "folder": '/inventory',
                "is_private_file": False,
                "use_unique_file_name": True,
            },
        )
        product = Product(
            product_name=product_name,
            supplier_id=supplier_id,
            category_id=category_id,
            quantity_per_unit=quantity_per_unit,
            unit_quoted_price=unit_quoted_price,
            units_in_stock=units_in_stock,
            description=description,
            image=image_json['response'],
        )
        db.session.add(product)
        db.session.commit()
        return ProductSchema.from_orm(product)
