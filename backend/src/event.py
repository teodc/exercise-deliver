from enum import Enum
from redis_om import JsonModel, Field


class Event(JsonModel):
    type: str = Field(index=True)
    delivery_id: str = Field(index=True)
    data: str = Field()


class Type(Enum):
    DELIVERY_CREATED = "DELIVERY_CREATED"
    DELIVERY_STARTED = "DELIVERY_STARTED"
    PRODUCTS_PICKED_UP = "PRODUCTS_PICKED_UP"
    PRODUCTS_DELIVERED = "PRODUCTS_DELIVERED"
    BUDGET_INCREASED = "BUDGET_INCREASED"
