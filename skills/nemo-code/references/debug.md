# Debugging

Hard bugs and performance regressions: build a feedback loop before theorizing.

Redact secrets in any command output you show (`<REDACTED>`).

## Phase 1 — Tight red loop (mandatory)

Do not hypothesize from code reading until you have a **tight, red-capable** loop you have already run once (show invocation + redacted output):

- **Red-capable**: drives the bug path and asserts the user's symptom (not merely "didn't crash").
- **Deterministic** (or high enough repro rate to debug).
- **Fast** (seconds when possible).
- **Agent-runnable**.

Constructors (prefer earlier): failing test → curl/HTTP script → CLI + fixture → headless UI script → replay captured payload → throwaway harness → property/fuzz → bisect/differential harness.

If you cannot build a loop: stop, list what you tried, ask for environment access or a redacted artifact. Do not proceed to Phase 2 without a loop.

## Phase 2 — Reproduce and minimise

Confirm the loop shows the user's failure mode. Shrink the repro until every remaining element is load-bearing.

## Phase 3 — Hypothesise

Generate 3–5 ranked, falsifiable hypotheses ("If X, then probe Y changes the symptom") before testing them. Show the list when cheap; don't block if the user is AFK.

## Phase 4 — Instrument

Change one variable at a time. Prefer debugger/REPL, then targeted logs tagged `[DEBUG-…]` for easy cleanup. For perf: measure baseline first.

## Phase 5 — Fix + regression

If a correct seam exists: failing regression test → fix → green → re-run the original Phase 1 loop. If no correct seam exists, document that as a finding.

## Phase 6 — Cleanup

Original loop green; regression in place (or seam gap noted); all `[DEBUG-…]` removed; throwaways deleted.
