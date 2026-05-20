from fastapi_sqlalchemy import db
from app.models.model_product import Product

class ProductService:
    @staticmethod
    def get_list():
        return db.session.query(Product).all()

    @staticmethod
    def get(product_id: int):
        product = db.session.query(Product).get(product_id)
        if product is None:
            raise Exception('Product not exists')
        return product
