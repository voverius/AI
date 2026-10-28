# nemo-general eval
Repeatable evaluation for [nemo-general](../../skills/nemo-general/SKILL.md). Project status and
results live in the AI knowledge project handover, `~/Projects/AI/handovers/nemo-general-rebuild.md`.
Run outputs and sandboxes are gitignored.

- `eval.py` - `run`, `judge`, `report <label> [train|heldout|heldout2|screen]`, `usage`, `selftest`
- `cases.json` - 94 cases with expectations, split train / heldout / heldout2
- `screen.txt` - 30-case subset for cheap screening
- `prefs.json` - the user's choices among variants, with notes
- `user-verdicts.json` - the user's pass/fail ratings and judge disagreements
- `results/`, `sandbox/`, `sb-*/` - local run outputs and test output styles, not versioned

Runs use real `claude -p` sessions with the user's hooks and plugins. `EVAL_SETTINGS` adds settings
and `EVAL_SANDBOX` picks the folder. Runs stop when weekly usage reaches 95%.
