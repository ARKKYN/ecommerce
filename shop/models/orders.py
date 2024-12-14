import json
from .base_model import BaseModel

class OrderItem:
  product_id : str
  quantity: int

  def __init__(self, product_id, quantity):
    self.product_id = product_id
    self.quantity = quantity

  def to_dict(self):
    return {"product_id": self.product_id, "quantity": self.quantity}

class Order(BaseModel, table=True):
  total_price: float
  status: str
  items: str

  def __init__(self, total_price, status, items: list[OrderItem] | str):
    self.total_price = total_price
    self.status = status
    self.items = self.__convert_items_to_str(items)

  def __convert_items_to_str(self, items: list[OrderItem] | str):
    if isinstance(items, list):
      return json.dumps([item.to_dict() for item in items])
    return items

  def get_id(self):
    return self.id

  def get_total_price(self):
    return self.total_price

  def get_status(self):
    return self.status

  def get_items_as_list(self) -> list[OrderItem]:
    items_data = json.loads(self.items)
    return [OrderItem(**item) for item in items_data]

  def to_dict(self):
    return {
      "id": self.id,
      "total_price": self.total_price,
      "status": self.status,
      "items": json.loads(self.items)
    }
