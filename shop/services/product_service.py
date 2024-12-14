
from fastapi import Depends
from shop.requestForms.create_product_request import CreateProductRequest
from shop.repository.product_repository import ProductRepository
from shop.models.product import Product
from typing import List

class ProductService:
  def __init__(self, repository: ProductRepository = Depends()):
    self.repository = repository

  def get_all_products(self) -> List[Product]:
    return self.repository.get_all()

  def __build_product_data(self, product: CreateProductRequest):
    return Product(name=product.name, description=product.description, price=product.price, stock=product.stock)

  def create_product(self, requestData: CreateProductRequest):
    new_product = self.__build_product_data(product=requestData)
    return self.repository.createProduct(new_product)
