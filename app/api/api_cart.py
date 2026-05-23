# Sửa lại file api_cart.py cho chuẩn chỉnh:
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
from app.schemas.sche_base import DataResponse
from app.schemas.sche_cart import CartItemCreate, CartResponse, CartItemUpdate
from app.services.srv_user import UserService
from app.services.srv_cart import CartService
from app.models import User

router = APIRouter()


@router.post("/add", response_model=DataResponse[CartResponse])
def add_item_to_cart(
    payload: CartItemCreate, current_user: User = Depends(UserService.get_current_user)
):
    try:
        result_data = CartService().add_to_cart(
            user_id=current_user.id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )

        return DataResponse().success_response(data=result_data)

    except Exception as e:
        return DataResponse().custom_response(code="400", message=str(e), data=None)


@router.put("/update", response_model=DataResponse[CartResponse])
def update_item_quantity(
    payload: CartItemUpdate,
    current_user: User = Depends(UserService.get_current_user),
):
    try:
        result_data = CartService().update_cart_quantity(
            user_id=current_user.id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
        return DataResponse().success_response(data=result_data)
    except Exception as e:
        return DataResponse().custom_response(code="400", message=str(e), data=None)


@router.delete("/remove/{product_id}", response_model=DataResponse[CartResponse])
def remove_item_from_cart(
    product_id: int,
    current_user: User = Depends(UserService.get_current_user),
):
    try:
        result_data = CartService().remove_from_cart(
            user_id=current_user.id, product_id=product_id
        )
        return DataResponse().success_response(data=result_data)
    except Exception as e:
        return DataResponse().custom_response(code="400", message=str(e), data=None)


@router.get("", response_model=DataResponse[CartResponse])
def get_cart(current_user: User = Depends(UserService.get_current_user)):
    try:
        result_data = CartService().get_user_cart(user_id=current_user.id)
        return DataResponse().success_response(data=result_data)
    except Exception as e:
        return DataResponse().custom_response(code="400", message=str(e), data=None)
