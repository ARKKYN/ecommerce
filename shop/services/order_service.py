from fastapi import Depends
from uuid import UUID
from shop.models.orders import Order
from shop.repository.order_repository import OrderRepository
from shop.repository.product_repository import ProductRepository
from shop.exceptions.product_not_found_exception import ProductNotFoundException
from shop.exceptions.outofstock_exception import OutOfStockException
from shop.requestForms.create_order_request import CreateOrderRequest
from shop.models.orders import OrderItem
from shop.models.product import Product
from typing import List

class OrderService:
  repository: OrderRepository
  product_repository: ProductRepository

  def __init__(self, order_repository: OrderRepository = Depends(), product_repository: ProductRepository = Depends()):
    self.repository = order_repository
    self.product_repository = product_repository

  def __get_map_of_products(self, products: list[Product]):
    return {str(product.id): product for product in products}

  def __build_missing_products_list(self, orderItems: dict[UUID, OrderItem], productMap: dict[str, Product]):
    missing_products = []
    for i in orderItems.keys():
      order = orderItems.get(i)
      if productMap.get(i, None) is None:
        missing_products.append(order.product_id)
    return missing_products

  def __get_missing_products(self, orderItems: dict[UUID, OrderItem], products: list[Product]):
    if len(products) == 0:
      return [str(orderItems.get(i, None).product_id) for i in orderItems]
    productMap = self.__get_map_of_products(products)
    missing_products = self.__build_missing_products_list(orderItems=orderItems, productMap=productMap)
    return missing_products

  async def __raise_exception_if_product_not_found(self, order: CreateOrderRequest):
    products = await self.product_repository.get_all_by_id(ids=order.to_order_ids_list())
    missing_products = self.__get_missing_products(orderItems=order.to_order_item_map(), products=products)
    if len(missing_products) > 0:
      raise ProductNotFoundException(f"Products not found: {missing_products}")

  async def __raise_exception_if_out_of_stock(self, order: CreateOrderRequest):
    order_items_map = order.to_order_item_map()
    products = await self.product_repository.get_all_by_id(ids=order.to_order_ids_list())
    out_of_stock_items = []
    for product in products:
      if product.stock < order_items_map[str(product.id)].quantity:
        out_of_stock_items.append(product.get_id_as_str())
    if len(out_of_stock_items) > 0:
      raise OutOfStockException(f"Products with following ids are out of stock: {', '.join(out_of_stock_items)}")

  async def __build_order(self, order: CreateOrderRequest):
    order_items = []
    total_price = 0
    products = await self.product_repository.get_all_by_id(ids=order.to_order_ids_list())
    product_map = self.__get_map_of_products(products)
    for item in order.items:
      order_items.append(OrderItem(item.product_id, item.quantity))
      total_price += item.quantity * product_map[str(item.product_id)].price
    return Order(total_price=total_price, status="success", items=order_items)

  async def create_order(self, order: CreateOrderRequest) -> Order:
    await self.__raise_exception_if_product_not_found(order)
    await self.__raise_exception_if_out_of_stock(order)
    new_order = await self.__build_order(order)
    await self.repository.create_order_transaction(new_order, order.items)
    return new_order

