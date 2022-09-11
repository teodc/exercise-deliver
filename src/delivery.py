from redis_om import JsonModel, Field


class Delivery(JsonModel):
    budget: int = Field(default=0, index=True)
    notes: str = Field(default="")
