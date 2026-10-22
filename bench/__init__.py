"""drcode-bench: harness for benchmarking the full drcode agent loop.

See `drcode-bench.md` for the plan. Implemented stages (§12):

- stage 1 (§12.1 skeleton): CLI stubs (`bench.__main__`), matrix parsing
  (`bench.matrix`), run-environment preparation (`bench.env_setup`);
- stage 2 (§4, §7 S1): one run = one subprocess (`bench.run_one`),
  settle detection + failure diagnostics (`bench.settle`),
  scenario loading (`bench.scenario`), the s1_happy scenario;
- stage 3 (§6): the user simulator (`bench.user_sim`) and the
  interactive scenarios S2a/S2b/S5;
- stage 4 (§1.2, §12.4): compaction scenarios S3/S4 on a small coding
  context, recorder + metrics cross-checks;
- stage 5 (§8, §10): the matrix runner (`bench.runner`) — scenarios ×
  combos × repeats, `--parallel` bounded subprocesses, infrastructure
  retries separate from substantive failures — the S6 scenario
  (queue priority + the development/testing gate) and the aggregated
  report with per-cell artifact links and optional HTML (`bench.report`).
"""

__version__ = "0.1.0"
