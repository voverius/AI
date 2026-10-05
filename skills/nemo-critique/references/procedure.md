
# Critical review
Review the requested artifact and the context necessary to judge it. Follow relevant dependencies
and authority; do not expand into unrelated work. Ask only when scope cannot be resolved from the
request. Implement fixes only when authorized.

## Judge the outcome
First identify the user's intended result and what evidence would prove it. Check whether the
artifact solves that problem, not merely whether it follows its own design. Consider a simpler
approach when the present structure creates cost without supporting a requirement.

Inspect concrete behavior and content for missing outcomes, contradictions, unsupported claims,
stale assumptions, unclear ownership and instructions a fresh agent cannot follow. Trace relevant
routes through their actual dependencies. For each material concern, cite its location and explain
its practical consequence. Label untested concerns; do not report them as observed failures.

Challenge your own verdict: could the artifact pass the stated checks while failing the user's
job? Could a claimed defect be an intentional boundary or an unnecessary preference? Recheck the
source before deciding. A plausible completion message or another reviewer's agreement is not proof.

## Report proportionately
Lead with the most consequential finding, or state that no material defects were found. Keep useful
parts, fit to the user's goal and inspection limits visible without repeating the artifact.

Rank findings by consequence:
- **Blocker:** fails the intended job or permits an unacceptable action
- **Major:** likely use produces wrong, missing or misleading results
- **Minor:** localized clarity or maintenance defect
- **Question:** a consequential choice only the user can settle

For a substantial review, group findings under Gaps, Keepers, Fit and Limits. A short review can
cover those points in prose. Report only actionable findings; no quota of objections, alternatives
or praise. Match the user's requested detail and communication preferences.

Done means the scoped artifact was inspected against its intended outcome, findings are supported,
and unverified requirements or limits are explicit. Reviewing alone does not establish that fixes
were made or that untested behavior works.
