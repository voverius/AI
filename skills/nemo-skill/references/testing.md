
# Blind behavioural testing

## Define the test before running it
Choose a small set of realistic requests and raw inputs from the skill's intended scope. Specify the
observable result, forbidden side effects and decisive checks outside the actor's workspace. Cover a
normal task, a relevant boundary or missing-input case, and a nearby request that should not
activate the skill. Add lifecycle or repeat-run cases only when the skill claims those behaviours.

Derive cases from the supported outcomes and dependencies, not just the implementation's menus.
Exercise independently callable routes without earlier setup in the same chat. Include ambiguous
targets when multiple workspaces are supported. Track untested routes explicitly. A successful
combined lifecycle does not prove each branch works alone.

Test interactions with the actual entry contract and neighboring skills, including nearby requests
that must not activate them. For saved knowledge, grade useful claim coverage, correctness,
uncertainty, ownership, retrieval and noise separately; file existence or a word count is not a
quality measure. Have a fresh reader answer realistic questions from the resulting knowledge.

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

Pass the normal global and local instruction entry points when the worker does not inherit them.
Record this as supplied environment context; do not substitute the target skill's path in a
discovery test.

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

## Match completion claims to evidence
Identify the tested source and dependencies by content hash or equivalent snapshot. Compare the
final files with that version before claiming completion. Later behavioural changes require affected
checks again. Formatting-only changes need an inspected diff and static checks, with earlier runtime
evidence identified as such. A commit is neither required nor proof of correctness.

Keep source, installation and migration claims separate. For installation or migration work, inspect
the relevant live discovery entries, links and consumers within the agreed scope. A source edit or
installer exit status does not prove host consistency. Retire unrelated entries only when
authorized.
Update completion records to match verified scope and evidence availability. Temporary evidence is
not a durable audit trail. Missing evidence limits the claim rather than proving success.

## Iterate without teaching the test
Fix the smallest general cause in the source. Reinstall if needed, then rerun the affected case with
a new actor and untouched input. Include a fresh variation to check that the correction generalizes.
Never manually repair output and count it as an actor pass; do not discard failed runs from the
conclusion.

Repeat critical cases under the same conditions before claiming reliability. Report every attempt,
including failed and interrupted runs; one eventual success does not establish consistent behavior.
Challenge reviewer findings against the actual requirement and evidence rather than accepting a
positive verdict or majority vote. Prefer removing a conflicting rule over adding repeated warnings.

If clear instructions repeatedly fail, test the same case with adequate reasoning or an independent
capable actor before adding more prose. Record model, reasoning level and host differences; do not
attribute a gain to the skill when those conditions also changed. A reviewer must check the original
requests and inputs, including decisions made in conversation, not merely the writer's summary.

Scale runs to risk and cost. Use a capable inexpensive model for bounded cases; keep evaluator
judgments separate from actor execution. Stop when the defined checks pass, or report the concrete
limitation. Missing agent capability or budget means untested, not passed. A few successful cases
support only those tested behaviours, not universal reliability.
