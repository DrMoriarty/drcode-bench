"""Item endpoints of the demo API."""

from __future__ import annotations

from .router import route


@route("GET /items")
def handle_list_items():
    return [{"id": 1, "name": "widget"}]


@route("POST /items")
def handle_create_item():
    return {"id": 2, "name": "sprocket", "created": True}


@route("GET /items/{item_id}")
def handle_get_item(item_id: int):
    return {"id": item_id, "name": "widget"}
