from fastapi_sqlalchemy import db

from app.models import Product
from app.schemas.sche_product import ProductCreateRequest, ProductUpdateRequest


class ProductService(object):
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(product_id: int) -> Product:
        product = db.session.query(Product).get(product_id)
        if not product:
            raise Exception('Product not found')
        return product

    @staticmethod
    def list(active_only: bool = True, min_price: float = None, max_price: float = None):
        query = db.session.query(Product)
        if active_only:
            query = query.filter(Product.is_active == True)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        return query.order_by(Product.created_at.desc())

    @staticmethod
    def create(data: ProductCreateRequest) -> Product:
        product = Product(
            name=data.name,
            description=data.description,
            category=data.category,
            image_url=data.image_url,
            specifications=data.specifications,
            price=data.price,
            inventory=data.inventory or 0,
            is_active=data.is_active if data.is_active is not None else True,
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update(product_id: int, data: ProductUpdateRequest) -> Product:
        product = db.session.query(Product).get(product_id)
        if not product:
            raise Exception('Product not found')
        product.name = product.name if data.name is None else data.name
        product.description = product.description if data.description is None else data.description
        product.category = product.category if data.category is None else data.category
        product.image_url = product.image_url if data.image_url is None else data.image_url
        product.specifications = product.specifications if data.specifications is None else data.specifications
        product.price = product.price if data.price is None else data.price
        product.inventory = product.inventory if data.inventory is None else data.inventory
        product.is_active = product.is_active if data.is_active is None else data.is_active
        db.session.commit()
        return product

    @staticmethod
    def delete(product_id: int) -> None:
        product = db.session.query(Product).get(product_id)
        if not product:
            raise Exception('Product not found')
        db.session.delete(product)
        db.session.commit()
