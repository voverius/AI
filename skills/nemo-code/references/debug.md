# Debugging

Hard bugs and perf regressions: feedback loop before theories.

Redact secrets in shown output (`<REDACTED>`).

## 1. Tight red loop (mandatory)

No hypothesizing from code until you have a tight, red-capable loop you have already run once
(show invocation + redacted output):

- **Red-capable**: hits the bug path; asserts the user's symptom (not "didn't crash")
- **Deterministic** (or high enough repro rate)
- **Fast** (seconds when possible)
- **Agent-runnable**

Build one, prefer earlier: failing test, curl/HTTP, CLI + fixture, headless UI, replay payload,
throwaway harness, fuzz, bisect/differential.

If you cannot: stop, list attempts, ask for access or a redacted artifact.
No Phase 2 without a loop.

## 2. Reproduce and minimise

Confirm the user's failure mode. Shrink until every remaining piece is load-bearing.

## 3. Hypothesise

3-5 ranked, falsifiable hypotheses before testing ("If X, then probe Y changes the symptom").
Show the list when cheap; do not block if the user is AFK.

## 4. Instrument

One variable at a time. Debugger/REPL first, then tagged logs `[DEBUG-…]`. Perf: measure baseline
first.

## 5. Fix + regression

Correct seam: failing regression → fix → green → re-run Phase 1 loop on the original scenario.
No correct seam: document that finding.

## 6. Cleanup

Phase 1 loop green; regression in place (or seam gap noted); all `[DEBUG-…]` gone; throwaways
deleted.
