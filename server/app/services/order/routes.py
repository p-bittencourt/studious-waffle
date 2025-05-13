# pylint: disable=unused-argument
# pylint: disable=unused-import
"""
Order routes module defining API endpoints for order operations.

This module defines all FastAPI routes for order-related operations,
including order creation, retrieval, updating, and deletion.
Routes require shopper authentication for operations that modify orders.
"""

from fastapi import APIRouter, Depends, status

from app.core.auth.current_user import ShopperUser
from app.core.db.conn import DbSession
from app.services.order.model import OrderPublic, OrderCreate, OrderUpdate

# These exceptions are referenced in docstrings
from app.core.utils.exceptions import (
    BadRequest,
    NotFound,
    CredentialsException,
)

from .service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_service(db: DbSession):
    """Get an instance of the OrderService.

    Args:
        db (DbSession): Database session dependency

    Returns:
        OrderService: Service instance for order operations
    """
    return OrderService(db)


@router.get("/", response_model=list[OrderPublic])
def get_orders(service: OrderService = Depends(get_order_service)):
    """Retrieve a list of all orders.

    Args:
        service (OrderService): Order service dependency

    Returns:
        list[OrderPublic]: List of all orders
    """
    orders = service.get_orders()
    return orders


@router.get("/{order_id}", response_model=OrderPublic)
def get_order_id(order_id: str, service: OrderService = Depends(get_order_service)):
    """Retrieve a specific order by its ID.

    Args:
        order_id (str): Unique identifier of the order to retrieve
        service (OrderService): Order service dependency

    Returns:
        OrderPublic: The requested order

    Raises:
        NotFound: If order with given ID doesn't exist (404)
    """
    order = service.get_order_id(order_id)  # Fixed function call
    return order


@router.post("/", response_model=OrderPublic)
def register_order(
    shopper_user: ShopperUser,
    order_data: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    """Register a new order in the system.

    Requires authentication as a shopper user.

    Args:
        shopper_user (ShopperUser): Current authenticated shopper
        order_data (OrderCreate): Order creation data
        service (OrderService): Order service dependency

    Returns:
        OrderPublic: The newly created order

    Raises:
        BadRequest: If order data is invalid
        CredentialsException: If authentication fails (401)
    """
    return service.register_order(shopper_id=shopper_user.id, order_data=order_data)


@router.patch("/{order_id}", response_model=OrderPublic)
def update_order(
    shopper_user: ShopperUser,
    order_id: str,
    order_data: OrderUpdate,
    service: OrderService = Depends(get_order_service),
):
    """Update an order's information.

    Requires authentication as a shopper user.

    Args:
        shopper_user (ShopperUser): Current authenticated shopper
        order_id (str): Unique identifier of the order to update
        order_data (OrderUpdate): New data for the order
        service (OrderService): Order service dependency

    Returns:
        OrderPublic: The updated order

    Raises:
        NotFound: If order with given ID doesn't exist (404)
        BadRequest: If no valid update data is provided (400)
        CredentialsException: If authentication fails (401)
    """
    return service.update_order(order_id, order_data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    shopper_user: ShopperUser,
    order_id: str,
    service: OrderService = Depends(get_order_service),
):
    """Delete an order from the system.

    Requires authentication as a shopper user.

    Args:
        shopper_user (ShopperUser): Current authenticated shopper
        order_id (str): Unique identifier of the order to delete
        service (OrderService): Order service dependency

    Returns:
        None

    Raises:
        NotFound: If order with given ID doesn't exist (404)
        CredentialsException: If authentication fails (401)
    """
    return service.delete_order(order_id)
