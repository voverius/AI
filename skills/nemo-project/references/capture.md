# Capture

Read [lifecycle](lifecycle.md) if not already loaded.
One `handovers/<task>.md` per workstream; update it rather than one file per conversation.

1. **Diff against the checkpoint.** Compare conversation and artifacts to the existing
   handover. Keep unique useful findings not yet distilled. For material already
   maintained elsewhere: link + continuation implication, not another summary. Memory is
   not proof of current file or system state
2. **Write populated fields only.** Objective and status; authorization boundaries;
   unfinished steps and blockers; exact next action; links to filed decisions, evidence,
   results; unique undistilled findings or hypotheses. Mark completed/cancelled explicitly;
   drop obsolete next actions. Exclude secrets, transcripts, raw tool output, repeated
   topic contents
3. **Cold read.** As a new agent: can you see the objective, facts vs uncertainty, needed
   artifacts, and continue without redoing finished work? Repair local links. Unchanged →
   leave the file untouched

Keep the checkpoint one-pass readable. Distill durable material when it dominates the
checkpoint; keep unresolved useful content. At completion: result pointer + any real
unresolved dependency, or remove the checkpoint if everything is already discoverable and
nothing continues.
