# Changelog

## 0.3.0 - 2026-11-15

- P1 now includes deterministic checks prepared for the change itself, such as a script that lists the call sites that must change or fails when any are left behind. A failure stops the review before model reviewers start. Sources: Factory task specifications, Agentless patch validation, SWE-agent linter gate.
- P3 splits structural changes (behavior unchanged, tests unchanged, the same test set run before and after) from behavioral changes into separate review units, and a unit that mixes both is split first. Sources: Beck's "never mix structural and behavioral changes", Google small CLs.
- The implementation report has two new mandatory items: (a) each fact the change's safety depends on needs one test plus reverse-verification evidence — break the corresponding production line, capture the failing output, restore; (b) every modified existing test is mapped to the pre-approved rule or test change item. The review brief in `templates.md` carries the same fields. Sources: Google "will the tests actually fail when the code is broken?", Google mutation testing, Agentless, Factory review guidance.
- Reviewers no longer rerun the full checks already run by the author or coordinator in P1; they run only targeted tests tied to their findings or spot checks. Reverse verification that needs code changes happens only in an isolated copy, never in the reviewed workspace. D7 allows spot-checking one or two reverse verifications. Sources: Factory test impact analysis, Devin review carry-forward.
- New R7: only established blocking findings open a rework round. Should-fix and optional findings are merged into an existing fix round or recorded for the next task, and their destination is listed in the conclusion. Sources: Google review standard, Factory review severity levels.

## 0.2.1 - 2026-11-13

- Before dispatching a fix, the coordinator checks whether the code under the finding should exist at all by the product rules. Findings on a path already slated for removal or pending a keep-or-delete decision are recorded into that removal task, not patched. Briefs describe such paths as "planned for removal, findings recorded only" rather than "existing behavior", which reviewers read as behavior to keep correct. Source: a real review where two fix rounds went into a path the owner had already ruled out.

## 0.2.0 - 2026-11-13

Selected general-purpose rules merged from the author's earlier project full-spectrum-review (v0.13.0, MIT). None of them has a controlled comparison behind it; `evidence.md` marks each as inferred.

- New `necessity.md`, read on demand by the reviewers who cover necessity (D4) and business flow: a four-step necessity method (reconstruct the problem, derive the minimum sufficient mechanism, challenge each extra layer, mandatory disconfirmation with a two-source floor when there is no history), patch-stack archaeology, and four business-semantics lenses (temporal semantics, conservation, mode parity, counterfactual scenarios).
- Bounded sets (key tables, allowlists, enums, state×event matrices, contract field tables) must be checked member by member from the consuming code. Sampling does not count as reviewed.
- Deduplication is now by root cause. Before: findings were merged when they shared file, line and failure scenario, which merged different root causes on one line and left one root cause reported several times. Now: symptoms of one root cause become one finding; same line with different root causes stays separate.
- Findings may carry an optional `status` (open, closed, accepted with a cited rationale). A tradeoff the project has already accepted in writing is not re-reported unless its premise changed, and the change must be stated.
- Severity follows real exposure: a default-off or experimental path is graded by its reachable consequence and labelled as such. Frequency is marked measured or inferred. A passing test is evidence, not proof.
- The coordinator restates the failure mechanism in its own words before accepting a blocking finding. Extra context in a brief must pass one test: would this fact change what the reviewer does?
- All runs of one review are pinned to the same commit; a moved head is re-reviewed or reported as `INCOMPLETE`.
- Codebase audit: three inventories during the survey (entry points, mutable facts, external boundaries); two new output sections, "designs worth keeping" and "open questions".
- New `evals/`: a regression net of four trap cases with expectations and a run procedure. First run against this version: 4/4 passed (`evals/results/2026-11-13-v0.2.0.md`). It only shows that seeded traps are still caught.

## 0.1.0 - 2026-11-13

First public release.

- Two modes, chosen by what is being reviewed: change review (a diff, PR, commit range or sub-agent delivery) and codebase audit (a project, directory, module or file with no change baseline).
- Change review: deterministic risk tiers L0–L3; pre-review steps (deterministic checks, file filtering, size check, review brief, implementation report); reviewer count and tracks per tier, including the contract-tracing track for high-risk changes; follow-up and re-review rules R1–R6.
- Codebase audit: project map, module ranking by high-risk surface, change frequency and incident records, batched review with explicit coverage status, remediation order instead of an approve/reject verdict.
- Shared by both modes: eight review dimensions with an admission bar (a reachable failure scenario or a measurable cost), a fixed finding format, independent verification that tries to falsify each finding, and token accounting from transcripts.
- Verdicts for change review: `APPROVE`, `REQUEST_CHANGES`, `INCOMPLETE`.
- `templates.md`: briefs for review, codebase audit, re-review and verification, plus a record table for comparison rounds.
- `evidence.md`: source and evidence strength for every rule, rejected practices with reasons, and the list of thresholds still to be calibrated.
