# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.model_base import Base  # noqa
from app.models.model_user import User  # noqa
from app.models.model_product import Product  # noqa
from app.models.model_order import Order  # noqa
from app.models.model_order_item import OrderItem  # noqa
from app.models.model_cart import Cart  # noqa
from app.models.model_cart_item import CartItem  # noqa