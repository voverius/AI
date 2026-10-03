
# Critique procedure

## Target
The user names the artifact (path, diff, paste, URL, prior output). That is the scope.
If scope is ambiguous: one clarifying question, then proceed.
Do not expand into unrelated files to "be thorough."
Pull only the minimum context needed to judge the target (linked deps, stated intent, adjacent
contract).

## Stance
- Primary job: **identify gaps** (missing, weak, wrong, risky, unexamined)
- Also name **keepers** (what works and should not be disturbed)
- State **limits of this critique** (what you could not see or verify)
- Do not get fixated on the author's frame: generate at least one alternate framing of the problem
  the artifact claims to solve
- Do not implement, rewrite, or "while I'm here" edit unless asked
- Separate observation from judgment

## Two distances (both required)

### Far
Ask from outside the artifact:

- What job is this for, and for whom?
- What would "done" mean, and does the artifact hit that?
- What adjacent jobs, users, or failure modes are ignored?
- If this disappeared, what would break? What would not?
- What is over-scoped or solving a problem nobody stated?

### Near
Inspect the material itself:

- Concrete holes, contradictions, vague completion criteria, unbound pointers
- Claims without evidence; procedures that cannot be followed as written
- Edge cases, trust boundaries, and "what if the happy path is false"
- Cite location (path, section, line, quote) for each near finding

## Anti-fixation moves
Before locking findings, run through:

1. **Invert**: what must be true for this to be the wrong approach?
2. **Omit**: what is never mentioned that a skeptical expert would demand?
3. **Substitute**: name one simpler and one more ambitious alternative; what gaps appear
   against each?
4. **Misuse**: how does this fail in the hands of a rushed agent or a hostile reader?
5. **Stale**: what ages badly (env facts, APIs, untested assumptions)?

Skip a move only when it clearly cannot apply; note the skip under Limits.

## Axes (report separately)
Do not merge into one score.

- **Gaps**: missing pieces, weak spots, risks, unexamined assumptions (main axis)
- **Keepers**: strong parts worth preserving
- **Fit**: matches the user's stated intent / pointed purpose (or "intent unclear")
- **Limits**: what this critique could not check

Optional when relevant (label clearly):

- **YAGNI / complexity**: what to delete or not build (ponytail-style, only if it earns space)
- **Process**: env/skill/check changes so this class of gap recurs less (retro-style; only if
  evidence from the artifact supports it)

## Severity
Rank Gaps (and optional Process) as:

- **Blocker**: wrong, unsafe, or fails the stated job
- **Major**: real hole under likely use
- **Minor**: sharpness, consistency, or rare-path issue
- **Question**: possible issue; needs the user's call

## Output shape
Lead with the single sharpest gap (or "no blockers" if none).

Then:

```text
## Gaps
- [severity] location: finding. Why it matters

## Keepers
- location: what works and why it should stay

## Fit
- one short judgment vs stated/pointed intent

## Limits
- what was out of scope or unverified

## Outside the frame (optional)
- alternate framing or omission that changes the picture
```

List/step lines: no terminal `.`. No em/en dashes. Cap visible gap bullets at 5 per severity
band; hold the rest unless asked.
Cap the whole critique unless the user asks for exhaustive.

## Done
Done when Gaps, Keepers, Fit, and Limits are present; far and near both ran; at least one
anti-fixation move left a trace in Gaps, Outside the frame, or Limits (as a skip).

