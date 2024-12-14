from .base_model import BaseModel

class Product(BaseModel, table=True):
  name: str
  price: float
  description: str
  stock: int

  def __init__(self, name, price, description, stock):
    self.name = name
    self.price = price
    self.description = description
    self.stock = stock

  def get_id(self):
    return self.id

  def get_id_as_str(self):
    return str(self.id)

  def get_name(self):
    return self.name

  def get_price(self):
    return self.price

  def get_description(self):
    return self.description

  def get_stock(self):
    return self.stock

