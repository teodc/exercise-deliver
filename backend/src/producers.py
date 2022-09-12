from event import Event


def produce(event_type: str, delivery_id: str, data: str) -> Event:
    return Event(
        type=event_type,
        delivery_id=delivery_id,
        data=data,
    ).save()
