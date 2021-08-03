from pydantic.tools import parse_obj_as
from models.order_details import OrderDetail
from models.orders import Order
from models.products import Product
from flask_pydantic import validate
from flask_restful import Resource
from schema.order_schema import *
from app import db


class Orders(Resource):
    @validate(body=OrderCreateSchema)
    def post(self, body: OrderCreateSchema):
        db.session.begin()
        try:
            order = Order(
                # customer_id=body.customer_id,
                user_uid = body.user_uid,
                shipping_address_id = body.shipping_address_id,
                employee_id=body.employee_id,
                shipper_id=body.shipper_id,
            )
            db.session.add(order)
            db.session.flush()
            for detail in body.order_details:
                # Get product
                product = Product.query.filter_by(id=detail.product_id).first()
                if not product:
                    return {"message": "Product does not exist"}, 400
                # Check product stock
                print (product.units_in_stock)
                if(product.units_in_stock < (-int(detail.quantity))):
                    raise Exception('Not enough product in stock')
                # Update product stock
                product.units_in_stock += detail.quantity
                db.session.add(product)
                # Create order details
                order_detail = OrderDetail(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=detail.quantity,
                    price=detail.price,
                    discount=detail.discount,
                )
                db.session.add(order_detail)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message": "An error has occurred, order cancelled"}
        # Tong tien don hang -> Tru tien khach hang
        return {"message": "Order successfully"}


class OrderInfo(Resource):
    @validate()
    def get(self, order_id):
        order = Order.query.filter_by(id = order_id).first()
        order_details = order.order_details
        total_pay = 0.0
        for detail in order_details:
            total_pay += abs(detail.quantity * detail.price)
        order_res =  OrderSchema.from_orm(order).dict()
        order_res['total_pay'] = total_pay

        return order_res
        # order_details = OrderDetail.query.filter_by(order_id = order.id).all()
        # print(type(order_details))
        # res = {}
        # a = []
        # for d in order_details:
        #     a.append(OrderDetailBaseSchema.from_orm(d).dict())
        # res['info'] = order_res.dict()
        # res['details'] = a
        # return res