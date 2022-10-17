from enum import Enum


class Type(str, Enum):
    DELIVERY_CREATED = "DELIVERY_CREATED"
    DELIVERY_STARTED = "DELIVERY_STARTED"
    PRODUCTS_PICKED_UP = "PRODUCTS_PICKED_UP"
    PRODUCTS_DELIVERED = "PRODUCTS_DELIVERED"
    BUDGET_INCREASED = "BUDGET_INCREASED"


class Status(str, Enum):
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COLLECTED = "collected"
    COMPLETED = "completed"
