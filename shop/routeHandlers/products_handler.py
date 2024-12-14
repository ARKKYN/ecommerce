from fastapi import APIRouter, Depends
from shop.requestForms.create_product_request import CreateProductRequest
from shop.services.product_service import ProductService
from shop.models.product import Product
from typing import List
from shop.utilities.response import ok_response

router = APIRouter()



@router.get("/products", response_model=List[Product])
async def getProducts(product_service: ProductService = Depends()):
  """
  parameters:
    request: {}
  returns:
    List of Products as JSON
  """
  products = await product_service.get_all_products()
  return ok_response(data=products)

@router.post("/products", response_model=Product)
async def createProduct(request: CreateProductRequest, product_service: ProductService = Depends()):
  """
  parameters:
    request: CreateProductRequest
  returns:
    Product as JSON
  """
  product = await product_service.create_product(request)
  return ok_response(data=product)
