from fastapi_sqlalchemy import db

from app.models import Order, OrderItem, Product
from app.schemas.sche_order import OrderCreateRequest, OrderStatusRequest
from app.helpers.enums import OrderStatus
from app.models import User


class OrderService(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(order_id: int) -> Order:
        order = db.session.query(Order).get(order_id)
        if not order:
            raise Exception('Order not found')
        return order

    @staticmethod
    def list_all():
        return db.session.query(Order).order_by(Order.created_at.desc())

    @staticmethod
    def list_by_user(user_id: int):
        return db.session.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc())

    @staticmethod
    def create_order(data: OrderCreateRequest, user: User = None) -> Order:
        if len(data.items) == 0:
            raise Exception('Order must contain at least one item')
        order = Order(
            user_id=user.id if user else None,
            customer_name=data.customer_name,
            customer_email=str(data.customer_email),
            shipping_address=data.shipping_address,
            status=OrderStatus.PENDING.value,
        )
        total_price = 0.0
        for item in data.items:
            product = db.session.query(Product).get(item.product_id)
            if not product:
                raise Exception(f'Product {item.product_id} not available')
            unit_price = float(product.price)
            total_price += unit_price * item.quantity
            order_item = OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=unit_price,
            )
            order.order_items.append(order_item)
        order.total_price = total_price
        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def update_status(order_id: int, data: OrderStatusRequest) -> Order:
        order = db.session.query(Order).get(order_id)
        if not order:
            raise Exception('Order not found')
        order.status = data.status.value
        db.session.commit()
        return order
