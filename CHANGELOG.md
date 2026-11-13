# Changelog

## 0.1.0 - 2026-11-13

First public release.

- Two modes, chosen by what is being reviewed: change review (a diff, PR, commit range or sub-agent delivery) and codebase audit (a project, directory, module or file with no change baseline).
- Change review: deterministic risk tiers L0–L3; pre-review steps (deterministic checks, file filtering, size check, review brief, implementation report); reviewer count and tracks per tier, including the contract-tracing track for high-risk changes; follow-up and re-review rules R1–R6.
- Codebase audit: project map, module ranking by high-risk surface, change frequency and incident records, batched review with explicit coverage status, remediation order instead of an approve/reject verdict.
- Shared by both modes: eight review dimensions with an admission bar (a reachable failure scenario or a measurable cost), a fixed finding format, independent verification that tries to falsify each finding, and token accounting from transcripts.
- Verdicts for change review: `APPROVE`, `REQUEST_CHANGES`, `INCOMPLETE`.
- `templates.md`: briefs for review, codebase audit, re-review and verification, plus a record table for comparison rounds.
- `evidence.md`: source and evidence strength for every rule, rejected practices with reasons, and the list of thresholds still to be calibrated.
