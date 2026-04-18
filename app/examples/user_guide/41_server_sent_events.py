from collections.abc import AsyncIterable, Iterable
from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None


items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]


@app.get('/items/stream', response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item


# no-async
@app.get('/items/stream-no-async', response_class=EventSourceResponse)
def sse_items_no_async() -> Iterable[Item]:
    for item in items:
        yield item


# no return type
@app.get('/items/stream-no-annotation', response_class=EventSourceResponse)
async def sse_items_no_annotation():
    for item in items:
        yield item


# ServerSentEvent
class Item(BaseModel):
    name: str
    price: float


items = [
    Item(name="Plumbus", price=32.99),
    Item(name="Portal Gun", price=999.99),
    Item(name="Meeseeks Box", price=49.99),
]


@app.get('/items/stream', response_class=EventSourceResponse)
async def stream_items() -> AsyncIterable[ServerSentEvent]:
    yield ServerSentEvent(comment='stream of item updates')
    for i, item in enumerate(items):
        yield ServerSentEvent(
            data=item, event='item_update', id=str(i + 1), retry=5000
        )


# raw data
@app.get('/logs/stream', response_class=EventSourceResponse)
async def stream_logs() -> AsyncIterable[ServerSentEvent]:
    logs = [
        "2025-01-01 INFO  Application started",
        "2025-01-01 DEBUG Connected to database",
        "2025-01-01 WARN  High memory usage detected",
    ]

    for log_line in logs:
        yield ServerSentEvent(raw_data=log_line)


# last-event-id
@app.get('/items/stream', response_class=EventSourceResponse)
async def stream_items(
    last_event_id: Annotated[int | None, Header()] = None
) -> AsyncIterable[ServerSentEvent]:
    start = last_event_id + 1 if last_event_id is not None else 0
    for i, item in enumerate(items):
        if i < start:
            continue
        yield ServerSentEvent(data=item, id=str(i))


class Prompt(BaseModel):
    text: str


# SSE with Post
@app.post('/chat/stream', response_class=EventSourceResponse)
async def stream_chat(prompt: Prompt) -> AsyncIterable[ServerSentEvent]:
    words = prompt.text.split()
    for word in words:
        yield ServerSentEvent(data=word, event='token')
    yield ServerSentEvent(raw_data='[DONE]', event='done')
