from pydantic import BaseModel, field_validator, Field
from typing import Dict
from uuid import UUID

class OrderItem(BaseModel):
    product_id: str
    quantity: int

    model_config = {
        "json_encoders": {
            UUID: lambda v: str(v)
        },
        "extra": "forbid"
    }

class CreateOrderRequest(BaseModel):
    items: list[OrderItem]

    model_config = {
        "json_encoders": {
            UUID: lambda v: str(v)
        },
        "extra": "forbid"
    }

    @field_validator('items')
    def items_must_not_be_none_or_empty(cls, v):
        if v is None or len(v) == 0:
            raise ValueError('items list must not be None or empty')
        return v

    def to_order_item_map(self) -> Dict[UUID, OrderItem]:
        return {item.product_id: item for item in self.items}

    def to_order_ids_list(self) -> list[str]:
        return [item.product_id for item in self.items]

