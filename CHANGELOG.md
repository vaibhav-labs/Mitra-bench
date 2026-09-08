# Changelog

## [0.3.0] - 2026-09-07 - Review gate and grant-reviewer board
### Added
- `skills/mitra-grant-reviewer/`: a standing seven-seat review board (program officer, safeguards methodologist, clinical reviewer, frontline counsellor, open-source maintainer, epistemics skeptic, state-of-the-art reviewer) with hard gates, an output contract, per-seat kill questions, a rubric distilled from the RFP, the guidance PDF and the 2025-2026 sources, the project's own failure log, and a calibration review of proposal v9.
- `review/pre_push_review.py`: the mechanical half of the board. Style bans, unfilled brackets, unbacked commitment language, superseded helpline numbers, practice name, budget arithmetic, cross-document headline numbers, employer convention, deadline dates, plus the validator, judge tests and harness smoke test. Writes dated reports to `review/reports/` and assembles `latest_prompt.md` for the full board. BLOCK exits 1.
- `.githooks/pre-push`: runs the gate in repo mode; enable with `git config core.hooksPath .githooks`.
- `docs/grant/`: the proposal (v10) and development plan (v5) inside the repo so the package is checked as a package.
- `docs/sources/sources.md`: the ledger of external claims with locators and verification dates. The board may not cite a fact absent from this ledger. No source text is stored, only locators.
### Changed
- Proposal v10: section 6 no longer lists KIRAN's former number as a correct D3 resource (merged into Tele-MANAS; caught by the gate on its first run); section 7 and Part A now describe the three-judge majority vote, judge chaining and tough-call flags that `taxonomy_v0.md` section 12 and `judges/` implement.
- Plan v5: WS5 and the compute model updated for three judges; net cost roughly neutral since the third judge replaces most human escalation.
- `resources/india_resources.md`: the historical iCall mention now uses the word "superseded" so the gate's allowlist recognises it, a fix to the artifact, not the rule.
### Gate status at release
- Repo mode: REVISE (three warnings, all verified three-item lists). Pushes proceed.
- Submission mode on the grant package: BLOCK on ten items, all the author's: seven brackets and three commitment claims without names. It stays blocked until they exist.

## [0.2.0] - 2026-09-07 - Judge architecture from Transluce's methodology appendix
### Added
- `taxonomy/taxonomy_v0.md` Section 12: adopted three-judge majority-vote design (one judge per developer family, always fixed, ties scored 0.5 and routed to human review at this project's scale), applicability criteria as a first-class concept with judge chaining, the tough-call flag, and a rubric-validity check used only during calibration. All adapted from Transluce's Mental Health Behavior Report methodology appendix (Appendix D/E), which validated this design at over 50,000 conversations.
- `scenarios/scenario.schema.json`: added `applicability_criteria` to checkpoint objects; populated on the three existing scenarios with a D6 or D4 precondition.
- `judges/judge_output.schema.json` and `judges/grade.schema.json`: new schemas for the per-judge record and the aggregated majority-vote grade.
- `judges/aggregate_votes.py`: working majority-vote aggregation logic with 7 unit tests, all passing. Caught and fixed a real polarity bug during test-writing: whether `occurred=True` means "pass" or means "the labelled behavior happened" was left implicit and had it shipped unresolved, every D6 grade would have inverted. The schema now states the convention explicitly.
- Refusal-handling threshold (development plan risk R29) tightened from an arbitrary 2% to 0.5%, anchored to Transluce's empirical rate of under 0.06% refused transcripts.
- CI now runs the judge unit tests on every push.

## [0.1.0] - 2026-09-02 - Pre-award scaffold
### Added
- Repository structure (taxonomy, lexicon, resources, scenarios, harness, judges, analysis, reports, docs, petri_seeds)
- `taxonomy/taxonomy_v0.md` - severity levels, escalation ladder, six dimensions, cue channels, distortion cues, cadence cues, scenario classes, and the protective-versus-harmful task rule (added in response to Transluce's Mental Health Behavior Report, Aug 31 2026). **Status: draft, pending co-investigator sign-off at G2.**
- `resources/india_resources.md` - verified helpline numbers as of 2026-09-02. Caught and corrected two stale-data risks before any scenario referenced them: iCall's pre-2023 number still circulating online and KIRAN's merger into the Tele-MANAS line.
- `scenarios/scenario.schema.json` - formal JSON Schema for scenario records.
- Four sketch scenarios (`scenarios/anchor/`): WRK-041 (canonical worked example, branched + cadence), WRK-104 (counter-case pair), FIN-018 (protective-vs-harmful task rule, S3), FIN-018-R (recovery-class prefill variant). All `status: sketch_pending_clinical_review`.
- `harness/validate_scenarios.py` - schema + cross-field checklist validator (WS3 rules). All four sketches pass.
- `harness/run_scenario.py` - minimal runner skeleton with a mock backend; proves the scenario → conversation → run-record pipeline end to end.
- CI workflow running the validator and a scenario-schema lint on every push.

### Explicitly deferred (see development plan for gates)
- Real model API backends (post-award, WS6)
- Grading and judge integration (post-award, gated at G3 rubric freeze, WS5)
- Lexicon content beyond the schema stub (needs annotator pool, WS2/WS3)
- Adaptive arm / SimMH-Chat integration (G2 decision, WS6)
- Calibration, panel ratings, alpha computation (needs contracted panel, WS4)
- Anything touching real human subjects (gated on IRB, WS1)
