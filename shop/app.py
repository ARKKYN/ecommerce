import logging
import time
from fastapi import FastAPI, Request
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .core.inititalize_database import initialize_database
from .routeHandlers import products_handler, orders_handler
from .exceptions.outofstock_exception import OutOfStockException
from .exceptions.product_not_found_exception import ProductNotFoundException
from .utilities.response import error_response

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Ecommerce")

initialize_database()
app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_host = request.client.host if request.client else "Unknown"
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Completed {request.method} {request.url.path} "
            f"[{response.status_code}] "
            f"from {client_host} "
            f"took {process_time:.2f}ms"
        )
        return response

    except Exception as e:
        logger.error(
            f"Request failed {request.method} {request.url.path} "
            f"from {client_host}: {str(e)}"
        )
        raise

@app.exception_handler(OutOfStockException)
async def handle_out_of_stock_exception(request, e: OutOfStockException):
  return error_response(e.message, status_code=HTTP_409_CONFLICT)

@app.exception_handler(ProductNotFoundException)
async def handle_product_not_found_exception(request, e: ProductNotFoundException):
  return error_response(e.message, status_code=HTTP_400_BAD_REQUEST)

@app.exception_handler(RequestValidationError)
async def handle_product_not_found_exception(request, e: RequestValidationError):
  return error_response("Validation error", errors=e.errors(), status_code=HTTP_400_BAD_REQUEST)

@app.exception_handler(Exception)
async def handle_product_not_found_exception(request, e: Exception):
  logger.error(f"Internal server error: {e}")
  return error_response("Internal server error", status_code=HTTP_500_INTERNAL_SERVER_ERROR)

@app.exception_handler(StarletteHTTPException)
async def handle_http_exception(request, e: StarletteHTTPException):
  logger.error(f"HTTP exception: {e}")
  return error_response(message=e.detail, status_code=e.status_code)

@app.get("/")
async def ok():
  return {"status": "ok"}

app.include_router(router=products_handler.router, prefix="/api/v1")
app.include_router(router=orders_handler.router, prefix="/api/v1")

