# Demo API (research seed for S11)

A miniature HTTP router in `src/api/`:

- `router.py` — the `route` decorator factory and the handler registry;
- `items.py`, `users.py` — endpoint modules: each endpoint is a pair
  «`@route("METHOD /path")` decorator directly above its `def handle_*`
  function».

There is no server here and nothing to run: the package exists so the
route table can be extracted from the source mechanically. Five routes
are declared in total; every (method, path, handler) triple is unique
and every decorator string occurs exactly once in the tree, so a
`@route\("...\)` grep yields no false matches.
