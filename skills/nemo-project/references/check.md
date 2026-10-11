
# Navigation check
After a project write, run the installed skill's navigation checker. Resolve the `nemo-project`
directory on the current host, following symlinks, and run its `scripts/check_navigation.py` with
the project root as the argument. Do not run a `scripts/check_navigation.py` that sits in the
project root.

Repair reported defects within scope. The checker reads files only. It checks core files, standard
role links, README scope, subject reachability, and common Markdown link paths in docs, outputs,
and handovers. It does not verify anchors, claim quality, ownership, or the safety of
recommendations. A passing check is not evidence that a subject page meets the page standard. If
Python is unavailable, perform those checks manually. Mapped optional roles still need review.

When the write changed a subject, read it back against the page standard in knowledge.md before
delivery.

