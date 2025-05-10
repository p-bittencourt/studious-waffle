from fastapi import APIRouter, Depends, status

from app.core.auth.current_user import ShopperUser
from app.core.db.conn import DbSession
from app.services.order.model import OrderPublic, OrderCreate, OrderUpdate

from .service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_service(db: DbSession):
    return OrderService(db)


@router.get("/", response_model=list[OrderPublic])
def get_orders(service: OrderService = Depends(get_order_service)):
    orders = service.get_orders()
    return orders


@router.get("/{order_id}", response_model=OrderPublic)
def get_order_id(order_id: str, service: OrderService = Depends(get_order_service)):
    order = service.get_order_id
    return order


@router.post("/", response_model=OrderPublic)
def register_order(
    shopper_user: ShopperUser,
    order_data: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    return service.register_order(shopper_id=shopper_user.id, order_data=order_data)


@router.patch("/{order_id}", response_model=OrderPublic)
def update_order(
    shopper_user: ShopperUser,
    order_id: str,
    order_data: OrderUpdate,
    service: OrderService = Depends(get_order_service),
):
    return service.update_order(order_id, order_data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    shopper_user: ShopperUser,
    order_id: str,
    service: OrderService = Depends(get_order_service),
):
    return service.delete_order(order_id)
