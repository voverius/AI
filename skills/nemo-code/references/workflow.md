# Code workflow glue

Session mode for software development, debugging, and code review. Voice stays in `nemo-general`.

Load by task:

| Task | Read |
| --- | --- |
| Init only | [init](init.md) |
| Implement / behavior change | [orientation](orientation.md) → [tdd](tdd.md) → [implement](implement.md) → [verify](verify.md) |
| Debug / diagnose | [orientation](orientation.md) → [debug](debug.md) → [tdd](tdd.md) when locking a regression → [verify](verify.md) |
| Review only | [review](review.md) |

Always: follow global and repository instructions; preserve existing user changes; never claim a check passed unless it was run.
