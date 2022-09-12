import json
from fastapi import HTTPException
from state import State, Status
from event import Event, Type


def _delivery_created(state: State, event: Event) -> State:
    data = json.loads(event.data)

    state.status = Status.READY.value
    state.budget = int(data["budget"])
    state.notes = data["notes"]

    return state


def _delivery_started(state: State) -> State:
    if state.status != Status.READY.value:
        raise HTTPException(status_code=400, detail="Delivery has already started")

    state.status = Status.IN_PROGRESS.value

    return state


def _products_picked_up(state: State, event: Event) -> State:
    data = json.loads(event.data)

    purchase_price = int(data["purchase_price"])
    quantity = int(data["quantity"])

    new_budget = state.budget - purchase_price * quantity

    if new_budget < 0:
        raise HTTPException(status_code=400, detail="Not enough budget")

    state.budget = new_budget
    state.purchase_price = purchase_price
    state.quantity = quantity
    state.status = Status.COLLECTED.value

    return state


def _products_delivered(state: State, event: Event) -> State:
    data = json.loads(event.data)

    sell_price = int(data["sell_price"])
    delivered_quantity = int(data["quantity"])

    new_budget = state.budget + sell_price * delivered_quantity
    new_quantity = state.quantity - delivered_quantity

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Not enough quantity")

    state.budget = new_budget
    state.sell_price = sell_price
    state.quantity = new_quantity
    state.status = Status.COMPLETED.value

    return state


def _budget_increased(state: State, event: Event) -> State:
    data = json.loads(event.data)

    state.budget = state.budget + int(data["amount"])

    return state


def consume(current_state: State, event: Event) -> State:
    match event.type:
        case Type.DELIVERY_CREATED.value:
            updated_state = _delivery_created(current_state, event)
        case Type.DELIVERY_STARTED.value:
            updated_state = _delivery_started(current_state)
        case Type.PRODUCTS_PICKED_UP.value:
            updated_state = _products_picked_up(current_state, event)
        case Type.PRODUCTS_DELIVERED.value:
            updated_state = _products_delivered(current_state, event)
        case Type.BUDGET_INCREASED.value:
            updated_state = _budget_increased(current_state, event)

    updated_state.save()

    return updated_state
