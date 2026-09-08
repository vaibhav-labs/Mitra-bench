# Board review: proposal v9, 2026-09-07

The board's first full review, on the day it was created. Kept as the calibration example: this is the pitch new reviews should match.

## 1. Verdict

**BLOCK.** The construct would survive the panel; the document would not, because it asserts commitments the record cannot show and cites a helpline that no longer exists as a separate line.

## 2. Hard gates triggered

- `proposal.md` Part A "The team" and section 10: seven unfilled brackets (`[name, credentials, insert before submission]`, `[update status]` twice, `[confirm year]` twice, `[to be obtained and cited]`, `[name, credentials, to be confirmed before submission]`).
- `proposal.md` Part A "The team": "a soft commitment is in place for the clinician co-investigator" in the same sentence as an empty name bracket. Asserted, unbacked.
- `proposal.md` section 6, checkpoint at turn 9: KIRAN 1800-599-0019 listed as a correct D3 resource. `resources/india_resources.md` (verified 2026-09-02) records that line as merged into Tele-MANAS. The answer key would have graded a merged number as India-correct.

## 3. Seat findings

**S1 Program Officer.** (1) Part A "The team": the fellow recruited from the BlueDot community is fine as a post-award hire; the co-investigator is not, because the sentence claims a commitment and shows no name. Wins: a name and one-line credential by September 18, or the sentence changes to "a clinician co-investigator will be contracted at G1a" and the ask is defended without the claim. (2) Section 12: the $395,000 figure matches the plan; the mechanical gate confirms the lines sum. No finding. (3) The proposal anonymises the employer while the CV names it; the package needs one convention before both leave.

**S2 Safeguards Methodologist.** (1) Section 7 describes two judges from non-Anthropic families with disagreements escalated to humans. `taxonomy/taxonomy_v0.md` section 12 now specifies a three-judge majority vote across developer families with tough-call flags. The repo and the proposal describe different graders. Wins: the proposal adopts the three-judge design, since it is the one Transluce validated at scale and the one the code implements. (2) Section 3 and section 5 pass: both failure modes, cue-indexed windows, decomposed dimensions, the protective-task rule. (3) Contamination handling in section 9 passes.

**S3 Clinical Reviewer.** (1) Section 2 cites Tele-MANAS operational guidelines with a bracket saying they are yet to be obtained. Do not cite what has not been read. Wins: obtain them by September 18 or anchor the window to mhGAP decision rules and the ICF referral competency alone, with the Tele-MANAS guidelines a month-1 deliverable in the plan, which it already is. (2) Clinical authority is structurally present in section 10 and missing a name. Same fix as S1. (3) No method detail found in any item, including FIN-018 at S3.

**S4 Frontline Counsellor.** (1) The KIRAN gate above. Wins: cite Tele-MANAS on 14416 or 1-800-891-4416 and iCall on 9152987821 with hours, and state that naming KIRAN's former number as a separate line fails D3. (2) Section 6 turn 6 at 01:58 with three messages in four minutes reads true. (3) "Log kya kahenge" as the stigma mechanism in section 1 is the right frame.

**S5 Open-Source Maintainer.** (1) Section 8 promises Petri seeds and SimMH-Chat interop; the repo README records the choice as a G2 decision. Consistent. (2) The first-hour path exists in the repo today and is a G5 gate in the plan. No finding.

**S6 Epistemics Skeptic.** (1) Record check: the $395,000 ask, the 0.4 FTE, the six-plus-two panel, the 260 scenarios and the three registers all match `docs/grant/development-plan.md`. (2) The Transluce figures in section 1 and section 9 trace to `docs/sources/sources.md` rows dated 2026-09-02 and 2026-09-07. (3) The two-judge sentence in section 7 does not trace to the current taxonomy. That is the S2 finding, restated as a record failure.

**S7 State-of-the-Art Reviewer.** (1) Section 1 fact four positions against Transluce's three stated boundaries accurately. (2) The crosswalk to Transluce's 14 behaviours is a plan deliverable (WS2, month 3) and is not yet named in the proposal's section 13 deliverables list. Wins: one clause in section 13.

## 4. What would actually win

1. Names for the co-investigator and two raters by September 18, entered in Part A and section 10, or the commitment sentences rewritten as gates. Serves criterion 3, team capabilities.
2. Section 6 resource list corrected to the verified numbers with the KIRAN merger stated. Serves criterion 1, scientific rigor, since D3 is only as good as its answer key.
3. Section 7 rewritten to the three-judge majority vote, judge chaining and tough-call flags, matching `taxonomy_v0.md` section 12 and `judges/`. Serves criteria 1 and 4.
4. Section 2 either cites obtained Tele-MANAS guidelines or drops the bracket and leans on mhGAP and ICF. Serves criterion 1.
5. Section 13 names the crosswalk. Serves criterion 5.
6. One employer convention across proposal and CV. Serves criterion 2, since inconsistency reads as carelessness.

## 5. Strongest objection

The objection: every gate after G0 depends on eight signatures that do not yet exist, while the proposal asserts that some of them do. The early signal: brackets beside commitment language. What the artifact does about it: the funds-release gate means no money moves without the clinicians. What it should do: stop asserting until the names exist, because a reviewer who emails the co-investigator and finds air ends the application on integrity, which no methodology survives.

## 6. Record check

Verified against the repo or the sources ledger: the ask, the effort structure, the panel size, the scenario counts, the register list, every Transluce figure, every safeguards-report figure, the affective-use figures, the Tele-MANAS and iCall numbers. Not verifiable: the co-investigator's identity, the rater commitments, the Ashgro countersignature, the FLI contest year, the FLF result. All five are brackets or bare assertions; all five are hard gates in a submission-grade artifact.

## 7. Style and consistency

Mechanical gate: 11 hard gates (7 brackets, 3 unbacked commitments, 1 superseded number); 3 warnings, all three-item lists, cleared by hand; budget lines sum to the total; headline ask consistent across the package.

## 8. Ship decision

Nothing leaves. Items 2 and 3 of section 4 are editorial and were applied in v10 the same day. Items 1, 4 and 6 are the author's, by the no-ghostwriting rule and because only the author can produce a name. The document is resubmitted to the board once the brackets are gone.
