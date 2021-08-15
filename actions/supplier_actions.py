from schema.product_schema import ProductsSchema
from pydantic.tools import parse_obj_as
from models.products import Product
from models.suppliers import Supplier
from schema.supplier_schema import (
    SupplierCreateSchema,
    SupplierInfoSchema,
    SuppplierUpdateSchema,
)
from app import db


def create_new_supplier(supplier_request: SupplierCreateSchema):
    sup = Supplier(**supplier_request.dict())
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
    result['total_page'] = products.pages
    if products.has_next:
        result['next_page'] = products.next_num
    result['products'] = [ProductsSchema.from_orm(product).dict() for product in products.items]
    return result
