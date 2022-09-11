from enum import Enum
from redis_om import JsonModel, Field


class State(JsonModel):
    delivery_id: str = Field(default="", index=True)
    status: str = Field(default="", index=True)


class Status(Enum):
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COLLECTED = "collected"
    COMPLETED = "completed"
