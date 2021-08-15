from typing import List

from werkzeug.datastructures import FileStorage

from app import db
from flask import request
from models.categories import Category
from models.products import Product
from models.suppliers import Supplier
from pydantic.tools import parse_obj_as
from schema.product_schema import ProductInfoSchema, ProductsSchema, ProductUpdateSchema
from utils import imagekit_utils

"""
    CRUD
"""

# CREATE
def create_new_product():
    # Get data from form
    product_name = request.form.get("product_name", None)
    supplier_id = request.form.get("supplier_id", None)
    category_id = request.form.get("category_id", None)
    quantity_per_unit = request.form.get("quantity_per_unit", None)
    unit_quoted_price = request.form.get("unit_quoted_price", None)
    units_in_stock = request.form.get("units_in_stock", None)
    description = request.form.get("description", None)
    image = request.files.get("image", None)

    # Validate
    if (
        product_name is None
        or supplier_id is None
        or category_id is None
        or unit_quoted_price is None
    ):
        return {"message": "Missing required params"}, 400
    #  Convert price to float and make sure it greater than 0
    try:
        unit_quoted_price = float(unit_quoted_price)
        if unit_quoted_price <= 0:
            raise AttributeError
    except ValueError:
        return {"message": "Price must be float"}
    except AttributeError:
        return {"message": "Price must be greater than zero"}
    # Convert units in stock
    try:
        units_in_stock = int(units_in_stock)
        if units_in_stock <= 0:
            raise AttributeError
    except ValueError:
        return {"message": "Units in stock must be number"}
    except AttributeError:
        return {"message": "Units in stock must be greater than zero"}

    cate = Category.query.filter_by(id=category_id).first()
    if not cate:
        return {"message": "Category does not exist"}, 400

    sup = Supplier.query.filter_by(id=supplier_id).first()
    if not sup:
        return {"message": "Supplier does not exist"}, 400

    # Upload image
    if image is None:
        image_response = None
    else:
        image_response = []
        image_json = imagekit_utils.upload_image(image)
        if image_json["error"] is not None:
            return {
                "message": "An error occurred while uploading image, please try again"
            }, 500
        else:
            image_response.append(image_json["response"])

    product = Product(
        product_name=product_name,
        supplier_id=supplier_id,
        category_id=category_id,
        quantity_per_unit=quantity_per_unit,
        unit_quoted_price=unit_quoted_price,
        units_in_stock=units_in_stock,
        description=description,
        image=image_response,
    )
    db.session.add(product)
    db.session.commit()
    # Using ProductInfoSchema to parse product from ORM model to dict(json)
    # with ProductInfoSchema format
    return ProductInfoSchema.from_orm(product)


# READ
def get_product_info(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return {"message": "Product not found"}, 404
    # Using ProductInfoSchema to parse product from ORM model to dict(json)
    # with ProductInfoSchema format
    return ProductInfoSchema.from_orm(product)


# UPDATE
def update_product_info(product_id, request_body: ProductUpdateSchema):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return {"message": "Product not found"}, 404

    cate = Category.query.filter_by(id=request_body.category_id).first()
    if not cate:
        return {"message": "Category does not exist"}, 400

    sup = Supplier.query.filter_by(id=request_body.supplier_id).first()
    if not sup:
        return {"message": "Supplier does not exist"}, 400

    product.product_name = request_body.product_name
    product.supplier_id = request_body.supplier_id
    product.category_id = request_body.category_id
    product.quantity_per_unit = request_body.quantity_per_unit
    product.unit_quoted_price = request_body.unit_quoted_price
    product.units_in_stock = request_body.units_in_stock
    product.description = request_body.description

    db.session.add(product)
    db.session.commit()

    return {"message": "Product updated!"}, 200


# DELETE (DELETE)
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return {"message": "Product not found"}, 404
    db.session.delete(product)
    db.session.commit()
    return {"message": "Product deleted"}, 200


"""
    ACTIONS
"""


def get_product_list(offset, limit):
    products = Product.query.offset(offset).limit(limit).all()
    return parse_obj_as(List[ProductsSchema], products)


"""
    PRODUCT IMAGE 
"""

# CREATE (POST)
def add_new_image_to_product(product_id, images: List[FileStorage]):
    if images is None:
        return {"message": "Missing required param"}, 400
    # Find product with id
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return {"message": "Product doesn't exists"}, 404
    old_images = product.image
    # Upload images
    image_list = []
    for image in images:
        image_json = imagekit_utils.upload_image(image)
        # If there is an error
        if image_json["error"] is not None:
            for i in image_list:
                # Delete all image upload before
                imagekit_utils.delete_image(i["fileId"])
            return {
                "message": "An error occurred while uploading image, please try again"
            }, 400
        else:
            # Add result to image_list
            image_list.append(image_json["response"])
    # Add new images to product
    old_images.extend(image_list)
    product.image = old_images
    db.session.add(product)
    db.session.commit()
    return {"images": product.image}, 201


def get_images_of_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return {"messsage": "Product doesn't exists"}
    return product.image, 200


def delele_image_of_product(product_id, image_id):
    if image_id is None:
        return {"message": "Missing required param"}, 400
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        return {"message": "Product doesn't exists"}, 404
    print("Deleted-", imagekit_utils.delete_image(image_id=image_id))
    # Put outt deleted image from images list
    image_list = [image for image in product.image if not (image["fileId"] == image_id)]
    # Assign new images list to product
    product.image = image_list
    db.session.add(product)
    db.session.commit()
    return {"message": "Image deleted"}, 200
