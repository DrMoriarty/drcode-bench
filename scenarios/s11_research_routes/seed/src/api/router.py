"""Route registry for the demo API.

Every endpoint is declared as a PAIR: a ``@route("METHOD /path")``
decorator directly above its handler function. The decorator stamps the
spec onto the handler and registers the handler name — it does NOT
duplicate the spec anywhere else, so each "METHOD /path" string occurs
exactly once in the source tree (in its decorator).
"""

from __future__ import annotations

REGISTERED: list[str] = []


def route(spec: str):
    """Stamp the "METHOD /path" spec onto the decorated handler."""

    def register(handler):
        REGISTERED.append(handler.__name__)
        handler.route_spec = spec
        return handler

    return register
