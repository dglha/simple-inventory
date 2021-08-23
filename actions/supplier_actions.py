from utils.re_helper import is_valid_email, is_valid_phone
from utils import imagekit_utils
from flask.globals import request
from schema.product_schema import ProductsSchema
from pydantic.tools import parse_obj_as
from models.product import Product
from models.supplier import Supplier
from schema.supplier_schema import (
    SupplierCreateSchema,
    SupplierInfoSchema,
    SuppplierUpdateSchema,
)
from app import db


def create_new_supplier():
    company_name = request.form.get("company_name", None)
    contact_name = request.form.get("contact_name", None)
    contact_title = request.form.get("contact_title", None)
    address = request.form.get("address", None)
    city = request.form.get("city", None)
    country = request.form.get("country", None)
    postal_code = request.form.get("postal_code", None)
    phone = request.form.get("phone", None)
    homepage = request.form.get("homepage", None)
    email = request.form.get("email", None)
    image = request.files.get("image", None)

    if company_name is None or contact_name is None or phone is None or email is None:
        return {"message": "Missing required params"}, 400

    if not is_valid_email(email):
        return {"message": "Invalid email address"}, 400

    if not is_valid_phone(phone):
        return {"message": "Invalid phone number"}, 400

    if image:
        image_json = imagekit_utils.upload_image(image)
        if image_json["error"] is not None:
            return {
                "message": "An error occurred while uploading image, please try again"
            }, 500

    sup = Supplier(
        company_name=company_name,
        contact_name=contact_name,
        contact_title=contact_title,
        address=address,
        city=city,
        country=country,
        postal_code=postal_code,
        phone=phone,
        homepage=homepage,
        email=email,
    )
    if image_json:
        sup.image = image_json["response"]
    db.session.add(sup)
    db.session.commit()
    return SupplierInfoSchema.from_orm(sup)


def get_supplier_info(supplier_id):
    sup = Supplier.query.filter_by(id=supplier_id).first()
    if not sup:
        return {"message": "Supplier doesn't exists"}, 404
    return SupplierInfoSchema.from_orm(sup)


def update_supplier_info(supplier_id, supplier_request: SuppplierUpdateSchema):
    sup = Supplier.query.filter_by(id=supplier_id).first()
    if not sup:
        return {"message": "Supplier doesn't exists"}, 404

    sup.company_name = supplier_request.company_name
    sup.contact_name = supplier_request.contact_name
    sup.contact_title = supplier_request.contact_title
    sup.address = supplier_request.address
    sup.city = supplier_request.city
    sup.country = supplier_request.country
    sup.postal_code = supplier_request.postal_code
    sup.phone = supplier_request.phone
    sup.homepage = supplier_request.homepage
    sup.email = supplier_request.email

    db.session.add(sup)
    db.session.commit()

    return SupplierInfoSchema.from_orm(sup)


def delete_supplier(supplier_id):
    sup = Supplier.query.filter_by(id=supplier_id).first()
    if not sup:
        return {"message": "Supplier doesn't exists"}, 404
    db.session.delete(sup)
    db.session.commit()


"""
    ACTIONS
"""


def get_supplier_products(supplier_id, page, limit):
    sup = Supplier.query.filter_by(id=supplier_id).first()
    if sup is None:
        return {"message": "Supplier not found"}, 404
    products = (
        Product.query.filter_by(supplier_id=sup.id).order_by(Product.id.desc())
        # error_out = True: Return 404 if there is an error (page not found, ...)
        .paginate(page=page, per_page=limit, error_out=True, max_per_page=limit)
    )
    result = {}
    result["total_page"] = products.pages
    if products.has_next:
        result["next_page"] = products.next_num
    result["products"] = [
        ProductsSchema.from_orm(product).dict() for product in products.items
    ]
    return result
