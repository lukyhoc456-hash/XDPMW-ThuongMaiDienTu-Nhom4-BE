import logging
from typing import Any

from fastapi import APIRouter, Depends

from app.helpers.exception_handler import CustomException
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.sche_base import DataResponse
from app.schemas.sche_order import (
    OrderCreateRequest,
    OrderDetailResponse,
    OrderListItemResponse,
    OrderStatusRequest,
)
from app.services.srv_order import OrderService
from app.models import Order

logger = logging.getLogger()
router = APIRouter()


@router.post('', response_model=DataResponse[OrderDetailResponse])
def create_order(order_data: OrderCreateRequest,
                 order_service: OrderService = Depends()) -> Any:
    try:
        new_order = order_service.create_order(order_data)
        return DataResponse().success_response(data=new_order)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get('', response_model=Page[OrderListItemResponse])
def list_orders(params: PaginationParams = Depends()) -> Any:
    try:
        query = OrderService.list_all()
        return paginate(model=Order, query=query, params=params)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.get('/{order_id}', response_model=DataResponse[OrderDetailResponse])
def get_order(order_id: int,
              order_service: OrderService = Depends()) -> Any:
    try:
        order = order_service.get(order_id)
        return DataResponse().success_response(data=order)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))


@router.put('/{order_id}/status', response_model=DataResponse[OrderDetailResponse])
def update_order_status(order_id: int,
                        status_data: OrderStatusRequest,
                        order_service: OrderService = Depends()) -> Any:
    try:
        updated_order = order_service.update_status(order_id, status_data)
        return DataResponse().success_response(data=updated_order)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
