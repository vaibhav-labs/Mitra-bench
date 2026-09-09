# Changelog

## [0.6.1] - 2026-09-09 - Outreach role briefs

### Added
- `docs/outreach/role_brief_clinician_co-investigator.md` and `docs/outreach/role_brief_calibration_rater.md`: one-page briefs to send to candidates directly, explicitly not contracts and not legal documents. Each states scope, time commitment, compensation basis and what saying yes actually commits to right now (a name in the expression of interest, nothing binding until Ashgro's agreement is signed post-award). Built to shorten the path from a candidate saying yes to that yes being usable in the application, since named collaborators remain the single largest gap in every board review to date.

### Note
- No repo-content changes this entry; the GitHub repository was renamed to match the name already used throughout this package, which the author has confirmed directly.

## [0.6.0] - 2026-09-08 - The single-turn screen, and two content bugs the pipeline caught

### Added
- `screen/screen_item.schema.json`, `screen/generate_screen.py`, `screen/validate_screen.py`: the single-turn screen, empty since the first commit despite being named in the proposal repeatedly. The generator templates every screen-eligible lexicon entry into a single-turn item; the validator cross-references every item back against its source lexicon entry (register and severity must match, D2 and D5 can never appear since neither is testable in one turn). 23 seed items generated from the 24-entry lexicon.
- `lexicon/lexicon.schema.json`: two new optional fields, `screen_eligible` and `screen_ineligible_reason`, so an entry that is a discourse connector, not a standalone distress signal, can be excluded from screen generation with a logged reason, instead of silently producing a meaningless test item.

### Fixed, both caught by building the screen, not by review of the lexicon alone
- `LEX-0023` was tagged register `indian_english` but its phrase was written in Hinglish. Rewritten as genuine Indian English. This is the same class of error the stale-number and null-field bugs were: a label asserted without checking it against the content it was supposed to describe.
- `LEX-0024` ("waise ek unrelated cheez", the context-shift framing device from FAM-114) was templated into a standalone screen item that tested nothing meaningful, since the phrase only means anything as a lead-in to what follows it in a multi-turn conversation. Marked `screen_eligible: false` with the reason logged, not deleted, since it remains a correct and useful lexicon entry for its actual purpose.

### Changed
- CI and the local pre-push gate both now generate and validate the screen on every run.

### Verified
- 23/23 screen items pass, cross-referenced against 24 lexicon entries with 1 correctly excluded. Full regression (scenarios, judge votes, lexicon, prompt renderer, screen, harness) clean.

## [0.5.0] - 2026-09-08 - Lexicon and judge prompts: two empty directories closed
### Added
- `lexicon/lexicon.schema.json` and `lexicon/seed_lexicon.json`: the idiom-of-distress lexicon, empty since the repo's first commit, now has 24 entries. Drawn from the ten existing scenarios plus new material to round out coverage: every severity level represented (S0 through S3), every cue channel represented (somatic idiom, direct verbal, cognitive distortion, behavioural report, third-party framing), and the first entry in the hindi_romanised register, closing the last register gap noted in earlier versions. `lexicon/validate_lexicon.py` checks schema conformance, duplicate detection and the WS2 acceptance criterion (every entry needs a register, a severity association and a source type) explicitly, not just via schema "required".
- `judges/prompts/chained_applicability_behavior.md`: the actual judge prompt template implementing the three-judge chained design from taxonomy Section 12, previously specified only as schemas with no prompt behind them. Documents a worked example against WRK-041 turn 6 D6.
- `judges/render_prompt.py`: assembles a real, complete judge prompt from a scenario file, a checkpoint and a dimension, with dimension definitions pulled from a single table so a taxonomy revision propagates automatically. Proves the full pipeline (taxonomy definitions plus scenario annotations plus cue-event filtering) end to end without any API call.
- `judges/test_render_prompt.py`: six tests, including a correctness property, not just a formatting check: cue events from turns after the checkpoint must never leak into a judge's prompt, since a judge scoring an early checkpoint must not see distress cues that haven't happened yet in the scripted conversation.
### Fixed
- `lexicon/lexicon.schema.json`: `region_notes` was typed as required-string, rejecting the many entries that legitimately have no regional restriction. Same class of bug as the stale-number allowlist fix in 0.4.2: a schema that assumed a field always has content, checked against real data with nulls, failed immediately. Fixed to allow null.
- `CHANGELOG.md`: the 0.4.2 entry describing the removal of a banned comparative phrase from the proposal contained that exact same banned phrase. Caught by the mechanical gate on this session's first run over the updated repo_checks (which now also runs the lexicon validator and prompt-renderer tests), not by manual review.
### Changed
- `review/pre_push_review.py` `repo_checks`: now also runs the lexicon validator, the prompt-renderer test suite, and the Hindi-register scenario validator (previously only checked in CI, never in the local gate).
- `.github/workflows/validate.yml`: same two additions, so CI and the local pre-push gate check identically again.
### Verified
- 24/24 lexicon entries pass. 6/6 prompt-renderer tests pass, including the cue-leakage correctness test. All ten scenarios and the judge vote unit tests still pass after the schema and gate changes.

## [0.4.2] - 2026-09-08 - Board review of the Torous-lab addition and a gate bug it exposed
### Fixed
- `review/pre_push_review.py`: `check_stale_numbers` only recognised the superseded/merged allowlist inside `india_resources.md` by filename. Running the gate against `docs/sources/sources.md` for the first time exposed this: the ledger's own correct historical notes on iCall's former number and KIRAN's merger were flagged as live citations. Fixed to recognise the allowlist in any file. A reviewer that misreports its own findings is worse than the gap it exists to catch.
### Changed
- `docs/grant/proposal.md` (v12): fact six's closing sentences, per the board's S7 finding, now state the supply-side argument from the Torous-lab audit explicitly, that the shortfall tracks what has been published and indexed in Hindi and not any property of the language, framed as an independent argument for why this project's lexicon and resources file are themselves a field contribution. Two style violations introduced while writing that sentence (one banned comparative phrase, one genuine two-clause comma-and) were caught by the same gate that flagged the fix and corrected before ship.
### Board verdict at this version
- Submission-mode gate on the full package: BLOCK, ten items, unchanged from v11 and all the author's (seven brackets, three commitment claims without names). The new paragraph itself: no new gates.

## [0.4.1] - 2026-09-08 - Third-field converging evidence
### Added
- `docs/sources/sources.md`: new row for Nguyen, Torous et al. (Harvard Medical School Division of Digital Psychiatry), "Sources of Truth" (arXiv:2609.00319, Aug 31 2026), which found Google AI Overview returns zero citations for 30% of Hindi-language mental-health queries. Audits ChatGPT, Perplexity and Google AI Overview; does not include Claude; measures citation/retrieval grounding, not conversational escalation, so it is cited as converging field context, never as a claim about this benchmark's subject model.
- `docs/grant/proposal.md` (v11): new seventh fact in Section 1 noting that clinical informatics researchers, not only AI-safety researchers, have independently measured a related piece of the Hindi-language gap, positioned as a third research community converging on the same underserved language via a third method.
### Not done, and why
- The jackknife sensitivity technique from this paper (leave-one-annotator-out, recomputed across all raters) is a candidate addition to WS8's reliability analysis but was not added to the development plan this round, to avoid a full plan version bump for one technique. Flagged for the author's decision.

## [0.4.0] - 2026-09-07 - Ten sketch scenarios: the pre-award milestone, properly covered
### Added
- Six new scenarios, bringing the sketch set to ten (the number the pre-award timeline names): `WRK-041-B` (closes the branch stub left dangling in WRK-041), `ACD-005` and `ACD-091` (first academic-context coverage, a matched pair), `FAM-027` (first family-context scenario, first Devanagari-script scenario, a clean S3 disclosure without a task-facilitation subplot, correctly placed in `scenarios/hindi/`), `FIN-052` (first dedicated cadence-only scenario: content stays mild throughout, timing alone carries the signal), `FAM-114` (first context-shift class scenario, operationalising the exact worked example in Anthropic's own grant announcement: an early bereavement disclosure that must modulate a later, self-described-as-unrelated medication-safety question).
- `docs/crosswalk_transluce.md`: the crosswalk stub that `taxonomy_v0.md` Section 13 already referenced but that did not exist until now. States plainly what does not map before attempting what does.
### Coverage after this batch
- All five scenario classes now have at least one live example (context_shift and the closed branch were previously at zero).
- All four contexts covered (workplace 3, financial 3, academic 2, family 2).
- Three of four language registers represented (Indian English, Hinglish, Hindi Devanagari); Hindi romanised remains the honest gap, deferred to post-award authoring with native-speaker annotators.
### Verified
- All 10 scenarios pass `harness/validate_scenarios.py` on first run across both `scenarios/anchor/` and `scenarios/hindi/`.
- Harness smoke-tested on the two most structurally novel additions (FAM-114's context-shift logic, FAM-027's Devanagari text) with no encoding or pipeline issues.
- Judge vote unit tests unaffected, still 7/7.

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
