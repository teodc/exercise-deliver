import enums
from redis_om import JsonModel, Field


class Delivery(JsonModel):
    budget: int = Field(default=0, index=True)
    notes: str = Field(default="")


class Event(JsonModel):
    type: enums.Type = Field(index=True)
    delivery_id: str = Field(index=True)
    data: str = Field()


class State(JsonModel):
    delivery_id: str = Field(default="", index=True)
    status: enums.Status = Field(default="", index=True)
