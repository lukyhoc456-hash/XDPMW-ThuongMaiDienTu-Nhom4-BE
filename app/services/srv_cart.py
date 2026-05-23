from fastapi_sqlalchemy import db
from app.models import (
    Cart,
    CartItem,
    Product,
)


class CartService:
    def __init__(self):
        pass

    def get_or_create_cart(self, user_id: int):
        cart = db.session.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
            db.session.refresh(cart)
        return cart

    def add_to_cart(self, user_id: int, product_id: int, quantity: int):
        cart = self.get_or_create_cart(user_id)

        cart_item = (
            db.session.query(CartItem)
            .filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
            .first()
        )

        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )
            db.session.add(cart_item)

        db.session.commit()
        return self._format_cart_response(cart)

    def update_cart_quantity(self, user_id: int, product_id: int, quantity: int):
        cart = db.session.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            raise Exception("Giỏ hàng không tồn tại")

        cart_item = (
            db.session.query(CartItem)
            .filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
            .first()
        )

        if not cart_item:
            raise Exception("Món hàng không có trong giỏ")

        cart_item.quantity = quantity
        db.session.commit()

        return self._format_cart_response(cart)

    def remove_from_cart(self, user_id: int, product_id: int):
        cart = db.session.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            raise Exception("Giỏ hàng không tồn tại")

        cart_item = (
            db.session.query(CartItem)
            .filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
            .first()
        )

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

        return self._format_cart_response(cart)

    def _format_cart_response(self, cart):
        db_items = db.session.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        formatted_items = []
        for item in db_items:
            product_detail = (
                db.session.query(Product).filter(Product.id == item.product_id).first()
            )
            formatted_items.append(
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "cart_id": item.cart_id,
                    "product": product_detail,
                }
            )
        return {"id": cart.id, "user_id": cart.user_id, "items": formatted_items}

    def get_user_cart(self, user_id: int):
        cart = self.get_or_create_cart(user_id)
        return self._format_cart_response(cart)
