import pytest
from httpx import AsyncClient
from shop.app import app
from shop.models.product import Product
from shop.core.inititalize_database import get_session
from sqlalchemy import text, delete
from shop.models.orders import Order
from sqlmodel import  select
from uuid import uuid4
from sqlalchemy import text, delete
from shop.models.orders import Order
import pytest_asyncio
from httpx import ASGITransport

test_product_data = {
    "name": "Test Product",
    "price": 10.0,
    "description": "Test Description",
    "stock": 10
}

@pytest.mark.asyncio
class TestProductAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):
        self.session = get_session()
        self.client = AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )
        yield
        await self.cleanup_db()

    async def cleanup_db(self):
        self.session.exec(delete(Product).where(Product.id != 100))
        self.session.commit()

    async def test_create_product_api(self):
        response = await self.client.post("/api/v1/products", json=test_product_data)
        data = response.json()["data"]
        assert response.status_code == 200
        assert data["name"] == test_product_data["name"]
        assert data["price"] == test_product_data["price"]
        assert data["stock"] == test_product_data["stock"]
        assert data["description"] == test_product_data["description"]

    async def test_get_products_validation_api(self):
        response = await self.client.post("/api/v1/products")
        data = response.json()
        assert response.status_code == 400
        assert len(data["errors"]) > 0

    async def test_get_products_api(self):
        await self.client.post("/api/v1/products", json=test_product_data)
        response = await self.client.get("/api/v1/products")
        data = response.json()
        assert response.status_code == 200
        assert len(data["data"]) == 1
