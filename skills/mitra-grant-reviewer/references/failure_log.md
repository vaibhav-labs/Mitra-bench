# Failure log

The board's memory. Every entry is something that actually went wrong in this project or was caught just before it did. The board reads this before any submission-grade review so it looks for these patterns first and never repeats them.

## Fabricated premises from outside reviewers

- **2026-09-01.** An outside review asserted the ask had "previously been restructured to $425,000." No such restructuring existed; every document carried $385,000. Rule: the board quotes the record before asserting a decision. If the record is silent, the board says so.
- **2026-09-02.** An outside review asserted the author had "decided to drop the clinician co-investigator" and recommended replacing clinical sign-off with the PI's coaching credential. No such decision existed; the author's own instruction was to keep the co-investigator with soft commitments. The proposed fix would have reopened the panel's second-strongest objection. Rule: a fix that removes clinical authority from severity governance is a hard gate, whatever premise it rides in on.

## Feasibility failures caught by review

- The first budget asked $100,000 against a program whose typical grants run $500,000 to $1.5M. Read as a pilot, not a program. Fixed by scaling scope honestly, then by leaning the team and stating why the number sits where it does.
- PI effort stated at 0.8 FTE alongside a senior day job. Not credible. Moved to 0.5, then to a sabbatical at 1.0, then to 0.4 with a full-time fellow owning execution. The sabbatical version carried a promise the author could not yet verify; the fellow version replaced it with a structure that survives any one calendar.
- Eleven hypothetical people in v3. The objection was never headcount; it was that nobody was named. Rule: a lean named team beats a large imaginary one on every criterion.
- Month-1 traffic jam: thirteen contracts and an IRB acknowledgment scheduled in thirty days. Fixed by splitting G1 into G1a (clinical signatures release authoring funds) and G1b (fellow, engineer, IRB on parallel tracks).
- Kill criterion 7 let the PI drop to 0 FTE if outside-activity clearance was withdrawn. Read as accountability with an escape hatch. Removed; clearance is now a G0 precondition.

## Rigor failures caught by review

- Tamil was in scope while the calibration panel was Mumbai-based; a Mumbai clinician cannot rate Tamil transcripts. Internal contradiction. Descoped to three registers with the line "this team validates natively only what it can rate natively."
- The 10% flat hand-inspection rate could miss systematic judge bias on Hinglish. Fixed with per-register judge qualification at 85%, risk-weighted inspection, dual grading of all S3 checkpoints, batch-level drift monitoring.
- Scripted users ignore good early intervention. Fixed with forty branched scenarios and a recovery class.
- The escalation ladder rewarded continuity credit for any help, including drafting a farewell note beside a referral. Transluce documented the co-occurrence pattern. Fixed with the protective-versus-harmful task rule governing D5 and D2.
- Adaptive-arm personas prompt-steered from assistants carry stylistic tells; Transluce measured near-100% AI-detection for that approach against 34.6% for a base-model-plus-pilot design. Fixed: human-authored scenarios primary, detection rates published, base-model design for the adaptive arm.
- The judge output field `occurred` had no stated polarity. Transluce's behaviours are harm-labelled (true is bad); this benchmark's dimensions are pass conditions (true is good). Left implicit, every D6 grade would have inverted. Caught by writing the unit test. Rule: conventions that could be read two ways are stated in the schema.

## Data failures caught by review

- iCall's helpline number changed in 2023; pages online still carry the old one. KIRAN merged into the Tele-MANAS line. Both would have been graded "correct" under D3 had they entered the answer key from memory. Caught in the first verification pass. Rule: every resource line carries a verification date; the refresh runbook runs at G2, G4 and annually.

## Positioning failures caught by review

- The proposal's first versions did not cite Anthropic's own affective-use study, which names coaching as a category and describes the author's caseload almost verbatim. An applicant who has not read the funder's research reads as an applicant who has not read the field.
- The proposal did not cite Transluce for two days after publication. Every serious applicant will. Fixed with a sixth fact in section 1 and positioning against Transluce's three stated boundaries.
- Early drafts said "nearly every proposal this program receives will miss this." Presumptuous. The gap now argues itself from sources.

## Style failures caught by review

- Em dashes, comma-before-and joining clauses and the banned comparative phrase recurred in every new block of prose, including the board's own files. The mechanical gate now catches all three on every push. Three-item Oxford-comma lists are legitimate and are left alone.

## What the board has not yet seen fail, and watches for

- A scenario with method detail slipping past two-person review.
- A judge refusing to classify Hinglish distress content at a rate above 0.5%.
- Transluce announcing an Indian-language extension.
- A co-maintainer MOU not signing by month 10.
- A number changed in one document and not the others.
