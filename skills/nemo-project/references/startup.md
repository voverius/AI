# Global skills and project entry

Skills live in the global installation. Project contracts use skill names; the host resolves
names to paths. Hosts without discovery need that mapping in global config. Keep
package-development paths out of projects.

## Contract template

Create `AGENTS.md` from this contract. Adapt local locations; preserve unrelated instructions:

> Start with the globally installed **nemo-project** skill (it owns root location and the
> access check). Then read [README](README.md), the knowledge index when present, and only
> the relevant subjects or handover.
>
> - `docs/` is the LLM wiki (compounding facts, decisions, procedures); handovers own
>   unfinished work; inbox holds arrivals; sources hold retained raw originals; outputs
>   hold deliverables; work is temporary. Keep code and authoritative external resources
>   in place

> - Shared facts have one subject owner; dependent procedures link to it. Preserve evidence,
>   uncertainty, and decision rationale
> - Use **nemo-project** init for structure, distill for knowledge and filing, capture at
>   substantive task boundaries
> - The changing agent updates affected index entries and incoming links. One integrator
>   reconciles parallel writes
> - If a required global skill is unavailable, report the missing installation before changing
>   project state; do not substitute a local development copy

README: purpose and links to existing roles. Topic navigation belongs in the knowledge index.
Setup alone creates no knowledge or handover.

## Verify

- Each contract responsibility appears in the generated file, including missing-skill handling
- Host loads entry automatically or via persistent global guidance
- Test a fresh ordinary request with no supplied workflow path and no project-local skill package
- Report unsupported discovery instead of claiming readiness

Use the existing skill installer for authorized installs. After moves or updates: check global
discovery and fresh startup. Project contracts keep the same skill names.
