import pytest
from unittest.mock import AsyncMock
from uuid import UUID, uuid4
from shop.services.order_service import OrderService
from shop.models.orders import  Order
from shop.models.product import Product
from shop.requestForms.create_order_request import CreateOrderRequest
from shop.exceptions.product_not_found_exception import ProductNotFoundException
from shop.exceptions.outofstock_exception import OutOfStockException

class TestOrderService:
    def setup_method(self):
        self.order_repository = AsyncMock()
        self.product_repository = AsyncMock()
        self.order_service = OrderService(
            order_repository=self.order_repository,
            product_repository=self.product_repository
        )

    @pytest.mark.asyncio
    async def test_create_order_with_non_existent_products(self):

        product_id = str(uuid4())
        order_items = [{"product_id": product_id, "quantity": 1}]
        order_request = CreateOrderRequest(items=order_items)
        self.product_repository.get_all_by_id.return_value = []

        with pytest.raises(ProductNotFoundException) as exc_info:
            await self.order_service.create_order(order_request)
        assert str(product_id) in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_order_with_insufficient_stock(self):

        product_id = str(uuid4())
        quantity = 10
        order_items = [{"product_id": product_id, "quantity": quantity}]
        order_request = CreateOrderRequest(items=order_items)

        mock_product = Product(name="Test Product", price=10.0, description="Test", stock=5)
        mock_product.id = UUID(product_id)
        self.product_repository.get_all_by_id.return_value = [mock_product]

        with pytest.raises(OutOfStockException) as exc_info:
            await self.order_service.create_order(order_request)
        assert product_id in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_order_success(self):

        product_id = str(uuid4())
        quantity = 2
        price = 10.0
        order_items = [{"product_id": product_id, "quantity": quantity}]
        order_request = CreateOrderRequest(items=order_items)

        mock_product = Product(name="Test Product", price=price, description="Test", stock=5)
        mock_product.id = UUID(product_id)
        self.product_repository.get_all_by_id.return_value = [mock_product]

        result = await self.order_service.create_order(order_request)

        assert isinstance(result, Order)
        assert result.total_price == price * quantity
        assert result.status == "success"
        assert len(result.get_items_as_list()) == 1
        assert result.get_items_as_list()[0].product_id == product_id
        assert result.get_items_as_list()[0].quantity == quantity
        self.order_repository.create_order_transaction.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_with_multiple_items(self):

        product1_id = str(uuid4())
        product2_id = str(uuid4())
        order_items = [
            {"product_id": product1_id, "quantity": 2},
            {"product_id": product2_id, "quantity": 3}
        ]
        order_request = CreateOrderRequest(items=order_items)

        mock_product1 = Product(name="Product 1", price=10.0, description="Test 1", stock=5)
        mock_product1.id = UUID(product1_id)
        mock_product2 = Product(name="Product 2", price=20.0, description="Test 2", stock=5)
        mock_product2.id = UUID(product2_id)

        self.product_repository.get_all_by_id.return_value = [mock_product1, mock_product2]

        result = await self.order_service.create_order(order_request)

        assert result.total_price == (2 * 10.0) + (3 * 20.0)
        assert len(result.get_items_as_list()) == 2
        self.order_repository.create_order_transaction.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_with_partial_product_not_found(self):

        existing_product_id = str(uuid4())
        non_existing_product_id = str(uuid4())
        order_items = [
            {"product_id": existing_product_id, "quantity": 1},
            {"product_id": non_existing_product_id, "quantity": 1}
        ]
        order_request = CreateOrderRequest(items=order_items)

        mock_product = Product(name="Test Product", price=10.0, description="Test", stock=5)
        mock_product.id = UUID(existing_product_id)
        self.product_repository.get_all_by_id.return_value = [mock_product]


        with pytest.raises(ProductNotFoundException) as exc_info:
            await self.order_service.create_order(order_request)
        assert non_existing_product_id in str(exc_info.value)
