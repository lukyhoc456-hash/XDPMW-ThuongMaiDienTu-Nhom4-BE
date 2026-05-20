from typing import Any, List
from fastapi import APIRouter, Depends
from fastapi_sqlalchemy import db

from app.schemas.sche_base import DataResponse
from app.schemas.sche_product import ProductResponse
from app.services.srv_product import ProductService

router = APIRouter()

@router.get("", response_model=DataResponse[List[ProductResponse]])
def get_products():
    try:
        products = ProductService.get_list()
        return DataResponse().success_response(data=products)
    except Exception as e:
        return DataResponse().custom_response(code="400", message=str(e), data=None)

@router.get("/{product_id}", response_model=DataResponse[ProductResponse])
def get_product(product_id: int):
    try:
        product = ProductService.get(product_id)
        return DataResponse().success_response(data=product)
    except Exception as e:
        return DataResponse().custom_response(code="400", message=str(e), data=None)

