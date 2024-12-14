import pytest
from unittest.mock import Mock
from shop.services.product_service import ProductService
from shop.requestForms.create_product_request import CreateProductRequest
from shop.models.product import Product

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def product_service(mock_repository):
    return ProductService(repository=mock_repository)

def test_get_all_products():
    mock_repo = Mock()
    expected_products = [
        Product(name="Product 1", description="Description 1", price=10.0, stock=100),
        Product(name="Product 2", description="Description 2", price=20.0, stock=200)
    ]
    mock_repo.get_all.return_value = expected_products
    service = ProductService(repository=mock_repo)

    result = service.get_all_products()

    assert result == expected_products
    mock_repo.get_all.assert_called_once()

def test_create_product():
    mock_repo = Mock()
    request_data = CreateProductRequest(
        name="New Product",
        description="New Description",
        price=15.0,
        stock=50
    )
    expected_product = Product(
        name="New Product",
        description="New Description",
        price=15.0,
        stock=50
    )
    mock_repo.createProduct.return_value = expected_product
    service = ProductService(repository=mock_repo)

    result = service.create_product(request_data)

    assert result == expected_product
    mock_repo.createProduct.assert_called_once()
    created_product = mock_repo.createProduct.call_args[0][0]
    assert created_product.name == request_data.name
    assert created_product.description == request_data.description
    assert created_product.price == request_data.price
    assert created_product.stock == request_data.stock

def test_build_product_data():
    service = ProductService(repository=Mock())
    request_data = CreateProductRequest(
        name="Test Product",
        description="Test Description",
        price=10.0,
        stock=100
    )

    result = service._ProductService__build_product_data(request_data)

    assert isinstance(result, Product)
    assert result.name == request_data.name
    assert result.description == request_data.description
    assert result.price == request_data.price
    assert result.stock == request_data.stock
