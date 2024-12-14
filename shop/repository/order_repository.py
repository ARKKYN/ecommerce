from sqlmodel import Session, select
from uuid import UUID
from shop.core.inititalize_database import get_engine
from shop.models.orders import Order
from sqlalchemy.orm import Session
from fastapi import Depends
from shop.models.orders import OrderItem
from shop.repository.product_repository import ProductRepository
from shop.core.inititalize_database import get_session

class OrderRepository:
  db: Session
  product_repository: ProductRepository

  def __init__(self, db: Session = Depends(get_session), product_repository: ProductRepository = Depends()):
    self.db = db
    self.product_repository = product_repository

  def get_all(self):
    return self.session.exec(select(Order)).all()

  def get_by_id(self, id: UUID):
    return self.session.exec(select(Order).where(Order.id == id)).first()

  def create_order(self, order: Order):
    self.db.add(order)
    self.db.commit()
    self.db.refresh(order)
    return order

  async def create_order_transaction(self, order: Order, items: list[OrderItem]):
    try:
        for item in items:
            await self.product_repository.deduct_stock(UUID(item.product_id), item.quantity)
        self.create_order(order)
        return order
    except Exception as e:
      self.db.rollback()
      raise e
