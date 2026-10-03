
# Blind behavioural testing

## Define the test before running it
Choose a small set of realistic requests and raw inputs from the skill's intended scope. Specify the
observable result, forbidden side effects and decisive checks outside the actor's workspace. Cover a
normal task, a relevant boundary or missing-input case, and a nearby request that should not
activate the skill. Add lifecycle or repeat-run cases only when the skill claims those behaviours.

Freeze the candidate during a run. The skill under test and its real dependencies remain accessible
to the actor. Keep evaluator notes, expected answers, prior outputs and alternative candidates
outside actor access. Fixtures must resemble ordinary user material, not contain hints about the
defect being tested. Never include live credentials or use production writes just to test a workflow

## Start an unpolluted actor
Spawn a new subagent with no inherited conversation (for example, `fork_turns="none"` when
supported). Give it only the natural task, raw inputs, permitted workspace and normal operating
constraints. Use separate writable workspaces for independent runs. Do not send the author's
reasoning, suspected bug, desired implementation, rubric, expected answer or earlier failure
messages.

A new name is not a fresh context. Do not reuse the author's or a previous tester's session. If the
host cannot prevent history inheritance, use a genuinely fresh supported session or mark the test
non-blind. Record unavoidable shared context such as global instructions and skill catalogs; do not
claim isolation that was not verified. Prompt restrictions are not a filesystem sandbox.

Distinguish two tests:
- **Execution:** explicitly supply the candidate skill or its path. This tests following its
  instructions, not discovering it
- **Discovery:** install through the authorized mechanism and give only an ordinary user request
  Verify which skill was selected and read. Also test a nearby non-matching request. Successful
  forced invocation does not prove discovery

The actor performs the task, rather than reviewing its own expected compliance. It must not inspect
evaluator files, other runs or author discussions. A reviewer can separately inspect the result;
do not give its critique back to an actor mid-run.

## Inspect evidence
Await each actor's actual terminal state; a timeout is not completion or failure. Inspect artifacts,
changes and relevant tool reads, not just the final message. Check useful information, uncertainty,
ownership, reference resolution and prohibited actions where applicable. For read-only or unchanged
runs, compare state before and after.

Keep enough evidence to reproduce the claim: exact prompt, raw input identity, candidate identity,
host/model, observed actions and outcomes, and failed or skipped checks. Retain it outside
deliverable/source directories under the task's retention policy; do not create permanent evidence
dumps by default.

Separate findings by cause: discovery, instructions, unavailable environment/tool, or evaluation
setup. If claiming improvement, compare the same inputs and host/model conditions against the prior
skill or no-skill baseline. Report the metric actually measured; fewer loaded words do not prove
lower latency or better answers.

## Iterate without teaching the test
Fix the smallest general cause in the source. Reinstall if needed, then rerun the affected case with
a new actor and untouched input. Include a fresh variation to check that the correction generalizes.
Never manually repair output and count it as an actor pass; do not discard failed runs from the
conclusion.

Scale runs to risk and cost. Use a capable inexpensive model for bounded cases; keep evaluator
judgments separate from actor execution. Stop when the defined checks pass, or report the concrete
limitation. Missing agent capability or budget means untested, not passed. A few successful cases
support only those tested behaviours, not universal reliability.

