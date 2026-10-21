"""drcode-bench: harness for benchmarking the full drcode agent loop.

See `drcode-bench.md` for the plan. Implemented so far:

- stage 1 (§12.1 skeleton): CLI stubs (`bench.__main__`), matrix parsing
  (`bench.matrix`), run-environment preparation (`bench.env_setup`);
- stage 2 (§4, §7 S1): one run = one subprocess (`bench.run_one`),
  settle detection + failure diagnostics (`bench.settle`),
  scenario loading (`bench.scenario`), the s1_happy scenario.
"""

__version__ = "0.1.0"
