
# Debugging
Inspect the symptom, relevant code and available evidence before choosing a fix. Redact secrets
from tool output and retained evidence.

1. Reproduce the failure at a public boundary with a focused test, CLI fixture or other repeatable
   check. Confirm it exercises the intended workspace and fails for the reported reason. Reduce
   the case until unrelated setup is removed; measure a baseline for performance problems
2. Test a specific explanation against that reproduction, changing one variable at a time. Use
   the debugger or a small probe before adding logs. For ambiguous failures, compare plausible
   causes with discriminating checks; do not invent a quota of hypotheses for an obvious defect
3. Apply the smallest supported fix, add regression coverage and rerun the original reproduction.
   Remove temporary instrumentation and artifacts created by the investigation. Report the actual
   result and remaining limits

If execution is unavailable, continue useful read-only diagnosis and distinguish suspected causes
from confirmed ones. Request only the missing access or redacted evidence needed to advance. Do not
claim reproduction, a tested fix or a successful regression check without running it.
