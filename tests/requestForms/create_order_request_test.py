import unittest
from shop.requestForms.create_order_request import CreateOrderRequest, OrderItem
from pydantic import ValidationError

class TestCreateOrderRequest(unittest.TestCase):
    def test_to_order_item_map(self):
        items = [
            {"product_id": "prod1", "quantity": 2},
            {"product_id": "prod2", "quantity": 5},
            {"product_id": "prod3", "quantity": 1}
        ]
        order_request = CreateOrderRequest(items=items)

        order_item_map = order_request.to_order_item_map()

        self.assertEqual(len(order_item_map), 3)
        self.assertIn("prod1", order_item_map)
        self.assertIn("prod2", order_item_map)
        self.assertIn("prod3", order_item_map)
        self.assertEqual(order_item_map["prod1"].quantity, 2)
        self.assertEqual(order_item_map["prod2"].quantity, 5)
        self.assertEqual(order_item_map["prod3"].quantity, 1)

    def test_validation_success(self):
        items = [
            {"product_id": "prod1", "quantity": 2},
            {"product_id": "prod2", "quantity": 5},
            {"product_id": "prod3", "quantity": 1}
        ]
        try:
            CreateOrderRequest(items=items)
        except Exception as e:
            self.fail(f"Test Validation failed: {e}")


    def test_validation_failure(self):
        with self.assertRaises(ValidationError):
            CreateOrderRequest(items=[])

    def test_to_order_ids_list(self):
        items = [
            {"product_id": "prod1", "quantity": 2},
            {"product_id": "prod2", "quantity": 5},
            {"product_id": "prod3", "quantity": 1}
        ]
        order_request = CreateOrderRequest(items=items)
        self.assertEqual(order_request.to_order_ids_list(), ["prod1", "prod2", "prod3"])
