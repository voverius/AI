
# Design rules
## Scope and ownership
Define one coherent capability and the requests that should activate it. A description must
distinguish it from nearby skills, including an exclusion only when confusion is plausible. A skill
can govern several related operations. Split into separate skills when they have independent
triggers or permissions, not merely because files are long.

Keep each rule in one authoritative place. Shared voice and global policy stay with their existing
owners. Reference them only when needed. Domain facts belong in the user's project or authoritative
system. Portable procedures must not inherit incidental machine paths, product names or test
answers. Genuine domain requirements remain explicit.

## Context and navigation
The description is paid for during discovery. The entry body is loaded on activation. Keep the
common decisions there and link substantial branch-specific guidance with a clear loading condition.
Use one routing layer. In `SKILL.md`, give each reference a linked name, a short description of
what it covers and when to read it. Put these descriptions in the routing list rather than adding
a duplicate index. A reader must be able to choose a file without opening it. During review, check
that each description matches its contents. References contain guidance, not another menu.

Group related constraints together. Split when readers can avoid irrelevant material. Merge tiny
references that are always loaded together. Optimize the ordinary task's actual reads, not a target
file count or word count. A skill that is all one short workflow may need no references.

In long sessions, continue applying relevant guidance without ritual reinvocation. After context
loss, recover the active task and necessary instructions through the host's persistent entry
mechanism. Do not promise that loaded context survives compaction.

## Task coverage and dependencies
When the user accepts an artifact as the expected result, extract its general quality criteria and
the corrections that established them. Put reusable requirements in their workflow owner. Do not
hardcode the artifact's topic, filename, phrasing or incidental environment into the skill. Use a
small template for stable structure and reserve the accepted artifact for evaluator calibration.

Trace each supported user outcome from request to route, required context, permitted actions and
completion evidence. Include outcomes implied by declared outputs and responsibilities. A folder
or artifact definition does not provide a procedure for producing it. When removing or merging a
branch, account for every job it owned: preserve, replace or explicitly retire it.

Check each route as a fresh entry, without context from another branch. Load the rules it relies on
before use, including shared locations, ownership and evidence rules. Resolve the intended target
before reads as well as writes when several projects or workspaces are available. Give read-only
routes their own completion criteria, without requiring artifacts or changes.

## Instructions that change behaviour
Use concrete actions, decision conditions and observable completion criteria. Replace "be thorough"
with the particular check that prevents a demonstrated mistake. Prefer a default with a reason over
an unranked menu. Use a small template when omissions recur. Use executable validation for
mechanical invariants when it earns its maintenance cost.

State when an operation reads, writes, publishes or deletes. A request for explanation or review
must not silently become implementation. A successful subprocess or self-reported completion is not
evidence that the user's intended result exists.

Make exception paths explicit where they affect correctness: missing dependencies, conflicting
evidence, partial input and unavailable capabilities. Resolve contradictions between branches
instead of adding another competing rule. Avoid universal gates and approval rituals for
hypothetical risks.

## Pruning
Keep material that changes decisions or prevents relevant errors. Remove repeated rules, ceremonial
status text, invented terminology, framework name-dropping and explanations of familiar concepts.
Preserve necessary evidence and caveats. Brevity is not a reason to erase a constraint.

Do not generate logs, reports, scaffolding or handovers merely to show that the skill ran. Every
persistent artifact needs a user or workflow purpose. Repeated execution with no new information
should leave state unchanged when the task permits it.

These are authoring conventions, not additional requirements of the Agent Skills format. They
synthesize the writing-for-agents approach and observed failures in our own skill work. The
installed third-party skill is not a runtime dependency.

