"""User endpoints of the demo API."""

from __future__ import annotations

from .router import route


@route("GET /users")
def handle_list_users():
    return [{"id": 7, "login": "ada"}]


@route("DELETE /users/{user_id}")
def handle_delete_user(user_id: int):
    return {"deleted": user_id}
