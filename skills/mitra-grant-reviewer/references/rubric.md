# Rubric: what wins this grant

Distilled from the RFP, Anthropic's guidance on building wellbeing evaluations, the December 2025 safeguards report, the June 2025 affective-use study, and Transluce's August 2026 Mental Health Behavior Report. The board scores against this, not against taste.

## The five stated criteria (RFP)

1. **Scientific rigor.** Defined construct; validation against expert human judgment; consistent results; usable by any developer.
2. **Feasibility.** Can this team deliver this scope in this time for this money. Named people. Realistic effort. Recruitment risk priced.
3. **Team capabilities.** The RFP's pairing test in its own words: subject-matter expertise (mental health or the impact of technology on wellbeing) paired with deep technical understanding of how AI systems behave and how to measure them. Demonstrated, not promised.
4. **Open-source release plan.** All funded evaluations must be released as open-source resources any developer can use. Licence, maintenance, contamination handling, first-hour usability.
5. **Likely contribution to the field.** Fills a gap the portfolio needs. Generalises. Does not duplicate what ships.

## What the guidance requires an evaluation to have

- One clearly defined construct.
- Both failure modes measured: harmful compliance and overrefusal.
- Multiple severity levels with a rubric per level.
- Decomposed pass or fail dimensions, never one collapsed score.
- Realistic multi-turn scenarios where risk escalates and context shifts.
- External validity: test the surface the claim is about (consumer chat, not bare API alone).
- Graders validated against human experts; a different model family as judge; hand inspection.
- Honesty about simulated versus real behaviour.
- Built with domain experts.
- Reproducible: open code, data, taxonomy.
- Sample size: 100+ multi-turn items, 1,000+ single-turn.
- Regional and linguistic variation where risk presents differently.
- Named failure modes to avoid: no human validation, underspecified grading, circular judge, single-turn only, trivially gameable, ambiguous items, saturation.

## The bar Transluce raised (August 2026)

- Descriptive evaluations at scale now exist for crisis presentations in US English. A new evaluation must state what it adds: language, sub-acute range, or a normative answer key.
- Applicability criteria per dimension, judge chaining, three-judge majority vote across developer families, tough-call flags.
- Evaluation awareness is measured and matters: human-authored scenarios are the defence; synthetic users must be checked with a detector.
- Harmful and helpful behaviours co-occur in one reply; scoring must catch task facilitation alongside referral.
- Expert clinicians disagree; a normative benchmark must publish agreement statistics and anchor its window to protocol, not opinion.

## What the December 2025 safeguards report tells the board

- Single-turn crisis response is near ceiling (98.6 to 99.3% appropriate; benign refusals near zero). A new single-turn eval is born saturated.
- Multi-turn scores 78 to 86%; prefill course-correction as low as 10% on sycophancy. Headroom is multi-turn and recovery.
- Anthropic runs its evals without the production system prompt to expose underlying tendencies; the bare arm has precedent.
- Claude.ai requires users to be 18+; every persona must be adult.

## House rules for this project (hard gates)

- No em dashes. No comma before "and" joining two clauses. No comparative "rather" constructions. No "not X but Y" antithesis. Flowing sentences. British spelling.
- Employer unnamed in the proposal by the author's byline rule; the CV names it. One convention across the package, decided by the author and then enforced.
- The private practice is never named in a submission-grade artifact.
- Every helpline number carries a verification date; superseded or merged numbers are never cited as live.
- Brackets are placeholders. A submission-grade artifact with a bracket is not submission-grade.
- The author writes the substance of anything competitive. The board recommends; it does not draft.

## Numbers the board holds in memory

Ask: $395,000 over 12 months (proposal v9, plan v4). PI 0.4 FTE. Lead research fellow 1.0 FTE. Six raters plus two bench. Clinician co-investigator with sign-off. 260 scenarios across Indian English, Hinglish and Hindi. 2,000-item screen. Three-judge majority vote. Compute $41,000. Dates: EOI September 21, 2026; invitations October 5; full proposal November 5.

Any artifact that states a different number without a changelog entry explaining why is a consistency failure.
