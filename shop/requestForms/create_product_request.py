
from pydantic import BaseModel

class CreateProductRequest(BaseModel):
  name: str
  price: float
  description: str
  stock: int


