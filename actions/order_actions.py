from settings import MONGO_BE_URL
from models.product import Product
from app import db
from schema.order_schema import OrderCreateSchema, OrderInfoSchema
from models.order import Order
from models.order_detail import OrderDetail
import requests

"""
    Oder CRUD
"""


def create_new_order(order_request: OrderCreateSchema):
    db.session.begin()
    try:
        if order_request.payment_method not in ["digicoin"]:
            raise Exception("Payment method not allowed")
        order = Order(
            # customer_id=body.customer_id,
            user_uid=order_request.user_uid,
            shipping_address_id=order_request.shipping_address_id,
            employee_id=order_request.employee_id,
            shipper_id=order_request.shipper_id,
            payment_method=order_request.payment_method,
            community_id=order_request.community_id,
        )
        db.session.add(order)
        db.session.flush()
        total_pay = 0.0
        for order_detail in order_request.order_details:
            # Get product
            product = Product.query.filter_by(id=order_detail.product_id).first()
            if not product:
                raise Exception("Product does not exist")
            # Check products in stock
            if product.units_in_stock < (-int(order_detail.quantity)):
                raise Exception("Not enough product in stock")
            # Update product stock
            product.units_in_stock += order_detail.quantity
            db.session.add(product)
            # Calculate the discount (fop demo only)?
            discount = 0.0
            if order_detail.quantity >= 10:
                discount = 0.1
            # Create order details
            order_detail = OrderDetail(
                order_id=order.id,
                product_id=product.id,
                quantity=order_detail.quantity,
                price=order_detail.price,
                discount=discount,
            )
            # Add order_detail to Database session
            db.session.add(order_detail)
            # Calculate the total payment
            total_pay += abs(order_detail.quantity * order_detail.price) * (
                1 - order_detail.discount
            )
        # TODO (10-8-2021)
        # What payment method is use for this order? (Digicoin/Invidual or Community Wallet)
        # Check user wallet (invidual or community)
        # Next, update the wallet
        # Then, clear the user cart
        # Calculate total payment -> Update user wallet / Community wallet

        if order.community_id is None:
            # Using invidual wallet
            resp = requests.get(url=f"{MONGO_BE_URL}/user/{order.user_uid}/wallet")
            # Check is request successful
            if not resp.ok:
                # If not, return error message
                if resp.json["message"] is None:
                    raise Exception("Server error, please try again")
                raise Exception(resp.json["message"])
            # Get user wallet
            user_coins = resp.json()["coins"]
            if user_coins < total_pay * 100:
                raise Exception("You don't have enough coin yet! Please top-up")

            # Update user wallet
            payload_data = {"total": total_pay, "payment_method": order.payment_method}
            update_resp = requests.post(
                url=f"{MONGO_BE_URL}/user/{order.user_uid}/wallet", json=payload_data
            )
            if not update_resp.ok:
                if update_resp.json["message"] is None:
                    raise Exception("Server error, please try again")
                raise Exception(resp.json["message"])
            print(update_resp.json)

        else:
            # Using community wallet
            params = {"user_id": order.user_uid, "community_id": order.community_id}
            resp = requests.get(url=f"{MONGO_BE_URL}/community/wallet", params=params)
            # Check is request successful
            if not resp.ok:
                # If not, return error message
                if resp.json["message"] is None:
                    raise Exception("Server error, please try again")
                raise Exception(resp.json["message"])
            # Get user wallet
            user_coins = resp.json()["wallet"]
            if user_coins < total_pay * 100:
                raise Exception("You don't have enough coin yet! Please top-up")

            # Update user wallet (Reuse params for payload_data)
            params["total"] = total_pay
            params["payment_method"] = order.payment_method
            update_resp = requests.post(
                url=f"{MONGO_BE_URL}/community/wallet", json=params
            )
            if not update_resp.ok:
                if update_resp.json["message"] is None:
                    raise Exception("Server error, please try again")
                raise Exception(resp.json["message"])
            print(update_resp.json)

        # Commit all data to database session
        db.session.commit()
    except Exception as e:
        # If there is an error or exception, rollback everything
        db.session.rollback()
        print("Error:" + str(e))
        return {
            "error": "An error has occurred, order cancelled",
            "message": str(e),
        }, 500

    return {"message": "Order successfully", "order_id": order.id}, 200


"""
    ACTIONS
"""

def get_order_info(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if order is None:
        return {"message": "Order does not exists"}, 404
    order_details = order.order_details
    total = 0.0
    # Each element in order_details is a product (detail)
    for product in order_details:
        total += abs(product.quantity * product.price) * (1 - product.discount)
    # Using OrderSchema to parse from order model to dict(json)
    response = OrderInfoSchema.from_orm(order).dict()
    response["total"] = total

    return response
