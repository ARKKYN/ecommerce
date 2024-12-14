import pytest
from httpx import AsyncClient
from shop.app import app
from shop.models.product import Product
from shop.core.inititalize_database import get_session
from uuid import uuid4
from sqlmodel import  select
import pytest_asyncio
from httpx import ASGITransport
from sqlalchemy import text, delete
from shop.models.orders import Order

@pytest.mark.asyncio
class TestOrderIntegration:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):
        self.session = get_session()
        self.client = AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )
        yield
        await self.cleanup_db()

    async def cleanup_db(self):
        self.session.exec(delete(Order).where(Order.id != 100))
        self.session.exec(delete(Product).where(Product.id != 100))
        self.session.commit()

    async def create_test_product(self, name="Test Product", price=10.0, stock=10):
        product = Product(
            name=name,
            price=price,
            description="Test Description",
            stock=stock
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    @pytest.mark.asyncio
    async def test_create_order_success(self):
        product = await self.create_test_product()

        order_data = {
            "items": [
                {
                    "product_id": str(product.id),
                    "quantity": 2
                }
            ]
        }

        response = await self.client.post("/api/v1/orders", json=order_data)

        assert response.status_code == 200
        order_response = response.json()
        assert order_response["data"]["total_price"] == 20.0
        assert order_response["data"]["status"] == "success"
        self.session.refresh(instance=product)

        updated_product = self.session.exec(
            select(Product).where(Product.id == product.id)
        ).first()
        assert updated_product.stock == 8

    @pytest.mark.asyncio
    async def test_create_order_product_not_found(self):
        order_data = {
            "items": [
                {
                    "product_id": str(uuid4()),
                    "quantity": 1
                }
            ]
        }

        response = await self.client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 400
        assert "Products not found" in response.json()["message"]

    @pytest.mark.asyncio
    async def test_create_order_insufficient_stock(self):
        product = await self.create_test_product(stock=5)

        order_data = {
            "items": [
                {
                    "product_id": str(product.id),
                    "quantity": 10
                }
            ]
        }

        response = await self.client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 409
        assert "out of stock" in response.json()["message"]
        self.session.refresh(instance=product)
        updated_product = self.session.exec(
            select(Product).where(Product.id == product.id)
        ).first()
        assert updated_product.stock == 5

    @pytest.mark.asyncio
    async def test_create_order_multiple_products(self):
        product1 = await self.create_test_product(name="Product 1", price=10.0)
        product2 = await self.create_test_product(name="Product 2", price=20.0)

        order_data = {
            "items": [
                {
                    "product_id": str(product1.id),
                    "quantity": 2
                },
                {
                    "product_id": str(product2.id),
                    "quantity": 1
                }
            ]
        }

        response = await self.client.post("/api/v1/orders", json=order_data)
        assert response.status_code == 200
        order_response = response.json()
        assert order_response["data"]["total_price"] == 40.0  # (2 * 10) + (1 * 20)

        self.session.refresh(instance=product1)
        self.session.refresh(instance=product2)
        updated_product1 = self.session.exec(
            select(Product).where(Product.id == product1.id)
        ).first()
        updated_product2 = self.session.exec(
            select(Product).where(Product.id == product2.id)
        ).first()

        assert updated_product1.stock == 8
        assert updated_product2.stock == 9

    @pytest.mark.asyncio
    async def test_create_order_invalid_request(self):
        invalid_order_data = {
            "items": [
                {
                    "product_id": "not-a-uuid",
                    "quantity": "invalid"
                }
            ]
        }

        response = await self.client.post("/api/v1/orders", json=invalid_order_data)
        assert response.status_code == 400
        assert "Validation error" in response.json()["message"]
