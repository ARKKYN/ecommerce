from sqlmodel import Session, select
from shop.models.product import Product
from shop.core.inititalize_database import get_engine
from uuid import UUID
from fastapi import Depends
from shop.core.inititalize_database import get_session

class ProductRepository:
  def __init__(self, session: Session = Depends(get_session)):
    self.session = session

  async def get_all(self):
    data = self.session.exec(select(Product)).all()
    return data
  async def createProduct(self, product: Product):
    self.session.add(product)
    self.session.commit()
    self.session.refresh(product)
    return product

  async def get_all_by_id(self, ids: list[str]):
    uuid_ids = [UUID(id_str) for id_str in ids]
    data = self.session.exec(select(Product).where(Product.id.in_(uuid_ids))).all()
    return data

  async def get_by_id(self, id: UUID):
    data = self.session.exec(select(Product).where(Product.id == id)).one_or_none()
    return data

  async def get_by_name_and_id(self, name: str, id: UUID):
    data = self.session.exec(select(Product).where(Product.name == name, Product.id == id)).one_or_none()
    return data

  async def __lock_and_get_by_id(self, id: UUID):
    data = self.session.exec(
      select(Product)
      .where(Product.id == id)
      .with_for_update()
    ).first()
    return data

  async def deduct_stock(self, id: UUID, quantity: int):
    product = await self.__lock_and_get_by_id(id)
    if not product:
        raise ValueError("Product not found")

    if product.stock < quantity:
        raise ValueError(f"Insufficient stock. Available: {product.stock}, Requested: {quantity}")

    product.stock -= quantity
    self.session.commit()
    self.session.refresh(product)
    return product
