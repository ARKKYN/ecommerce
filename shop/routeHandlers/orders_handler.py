from shop.requestForms.create_order_request import CreateOrderRequest
from shop.services.order_service import OrderService
from fastapi import APIRouter, Depends
from shop.models.orders import Order
from shop.utilities.response import ok_response
router = APIRouter()

@router.post("/orders", response_model=Order)
async def create_order(request: CreateOrderRequest, order_service: OrderService = Depends()):
  """
  parameters:
    request: CreateOrderRequest
  returns:
    Order as JSON
  """
  order = await order_service.create_order(request)
  return ok_response(data=order.to_dict())
