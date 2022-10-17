import json
import uvicorn
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import Migrator
from redis_om.model import NotFoundError

import constants
from models import Delivery, Event, State
from enums import Type
from consumers import consume
from producers import produce


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[constants.FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

Migrator().run()


class CreateDeliveryRequest(BaseModel):
    budget: int
    notes: str


class StartDeliveryRequest(BaseModel):
    delivery_id: str


class PickupProductsRequest(BaseModel):
    delivery_id: str
    purchase_price: int
    quantity: int


class DeliverProductsRequest(BaseModel):
    delivery_id: str
    sell_price: int
    quantity: int


class IncreaseBudgetRequest(BaseModel):
    delivery_id: str
    amount: int


@app.get("/")
async def root() -> str:
    return "I'm alive!"


@app.post("/create-delivery")
async def create_delivery(request: CreateDeliveryRequest) -> State:
    delivery = Delivery(budget=request.budget, notes=request.notes).save()
    state = State(delivery_id=delivery.pk)
    event = produce(
        event_type=Type.DELIVERY_CREATED.value,
        delivery_id=delivery.pk,
        data=json.dumps(request.__dict__),
    )

    return consume(state, event)


@app.post("/start-delivery")
async def start_delivery(request: StartDeliveryRequest) -> State:
    delivery_id = request.delivery_id
    state = await _get_state(delivery_id)
    event = produce(
        event_type=Type.DELIVERY_STARTED.value,
        delivery_id=delivery_id,
        data=json.dumps(None),
    )

    return consume(state, event)


@app.post("/pickup-products")
async def pickup_products(request: PickupProductsRequest) -> State:
    delivery_id = request.delivery_id
    state = await _get_state(delivery_id)
    event = produce(
        event_type=Type.PRODUCTS_PICKED_UP.value,
        delivery_id=delivery_id,
        data=json.dumps(request.__dict__),
    )

    return consume(state, event)


@app.post("/deliver-products")
async def deliver_products(request: DeliverProductsRequest) -> State:
    delivery_id = request.delivery_id
    state = await _get_state(delivery_id)
    event = produce(
        event_type=Type.PRODUCTS_DELIVERED.value,
        delivery_id=delivery_id,
        data=json.dumps(request.__dict__),
    )

    return consume(state, event)


@app.post("/increase-budget")
async def increase_budget(request: IncreaseBudgetRequest) -> State:
    delivery_id = request.delivery_id
    state = await _get_state(delivery_id)
    event = produce(
        event_type=Type.BUDGET_INCREASED.value,
        delivery_id=delivery_id,
        data=json.dumps(request.__dict__),
    )

    return consume(state, event)


@app.get("/get-status/{delivery_id}")
async def get_status(delivery_id: str) -> State:
    return await _get_state(delivery_id)


async def _get_state(delivery_id: str) -> State:
    try:
        delivery = Delivery.get(delivery_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Delivery not found")

    try:
        return State.find((State.delivery_id == delivery.pk)).first()
    except NotFoundError:
        return _build_state(delivery.pk)


def _build_state(delivery_id: str) -> State:
    delivery_events = Event.find((Event.delivery_id == delivery_id)).all()
    state = State(delivery_id=delivery_id)
    for event in delivery_events:
        state = consume(event, state)

    return state.save()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=constants.APP_HOST,
        port=constants.APP_PORT,
        reload=constants.APP_ENV == "local",
        reload_dirs=["./src"],
    )
