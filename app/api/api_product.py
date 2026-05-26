import logging
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request

from app.helpers.exception_handler import CustomException
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_product import ProductItemResponse, ProductCreateRequest, ProductUpdateRequest
from app.services.srv_product import ProductService
from app.models import Product

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / 'static' / 'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger()
router = APIRouter()

# Get all products
@router.get('', response_model=Page[ProductItemResponse])
def list_products(
    params: PaginationParams = Depends(),
    min_price: float = None,
    max_price: float = None,
) -> Any:
    try:
        query = ProductService.list(active_only=False, min_price=min_price, max_price=max_price)
        return paginate(model=Product, query=query, params=params)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))

# Get product by ID
@router.get('/{product_id}', response_model=DataResponse[ProductItemResponse])
def get_product(product_id: int) -> Any:
    try:
        product = ProductService.get(product_id)
        return DataResponse().success_response(data=product)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.post('', response_model=DataResponse[ProductItemResponse])
def create_product(product_data: ProductCreateRequest, product_service: ProductService = Depends()) -> Any:
    try:
        new_product = product_service.create(product_data)
        return DataResponse().success_response(data=new_product)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.post('/upload-image', response_model=DataResponse)
def upload_product_image(request: Request, file: UploadFile = File(...)) -> Any:
    try:
        allowed_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail='Invalid file type. Please upload JPG, PNG, GIF, or WEBP.')

        filename = f"{uuid4().hex}{Path(file.filename).suffix or '.jpg'}"
        file_path = UPLOAD_DIR / filename
        with file_path.open('wb') as f:
            f.write(file.file.read())

        base_url = str(request.base_url).rstrip('/')
        image_url = f"{base_url}/static/uploads/{filename}"
        return DataResponse().success_response(data={'image_url': image_url})
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.put('/{product_id}', response_model=DataResponse[ProductItemResponse])
def update_product(product_id: int, product_data: ProductUpdateRequest, product_service: ProductService = Depends()) -> Any:
    try:
        updated_product = product_service.update(product_id, product_data)
        return DataResponse().success_response(data=updated_product)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.delete('/{product_id}', response_model=DataResponse[Any])
def delete_product(product_id: int, product_service: ProductService = Depends()) -> Any:
    try:
        product_service.delete(product_id)
        return DataResponse().success_response(data={'deleted': True})
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
