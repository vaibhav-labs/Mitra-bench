#!/usr/bin/env python3
"""
MITRA-Bench pre-push review gate: the mechanical half of the grant-reviewer board.

Runs the checks a machine can run reliably, writes a report, and assembles the
prompt for the full seven-seat review. It can BLOCK on its own. It cannot PASS
a submission-grade artifact on its own; only the full board does that.

Modes:
  --mode repo        Repo hygiene: style bans on project prose, validator, judge
                     tests, harness smoke test, stale numbers, practice name.
                     Used by the git pre-push hook.
  --mode submission  Everything in repo mode plus the submission-grade gates:
                     unfilled brackets, unbacked commitment language, budget
                     arithmetic, cross-document numbers, employer convention.
                     Requires --artifact (one or more files).

Exit codes: 0 = no BLOCK (warnings may exist). 1 = BLOCK. 2 = misuse.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORTS = REPO / "review" / "reports"
SKILL = REPO / "skills" / "mitra-grant-reviewer"

PROSE_FILES = [
    "README.md", "CHANGELOG.md", "taxonomy/taxonomy_v0.md", "resources/india_resources.md",
]
STALE_NUMBERS = ["022-25521111", "1800-599-0019"]
PRACTICE_NAME = re.compile(r"clearhead", re.IGNORECASE)
EM_DASH = "\u2014"
RATHER_THAN = re.compile(r"\brather than\b")
# Two-clause join heuristic: ", and" followed by a subject-like word. Three-item
# lists ("A, B, and C") are legitimate and this heuristic tries to skip them by
# requiring a clause opener after "and".
CLAUSE_AND = re.compile(
    r",\s+and\s+(?:the|it|this|that|these|those|every|no|a|an|I|we|they|he|she|there|what|which|nothing|everything|any)\b"
)
BRACKET = re.compile(r"\[(?!x\]|\s\])[^\[\]\n]{3,}\]")
MD_LINK = re.compile(r"\]\(")
COMMITMENT_WORDS = re.compile(
    r"\b(soft commitment|confirmed|finali[sz]ed|is in place|are in place|contracted|countersigned|named)\b",
    re.IGNORECASE,
)
MONEY = re.compile(r"\$?\b(\d{3}),000\b")
BUDGET_ROW = re.compile(r"^\|[^|]+\|\s*([\d,]+)\s*\|\s*$")
TOTAL_ROW = re.compile(r"^\|\s*\*\*Total\*\*\s*\|\s*\*\*([\d,]+)\*\*\s*\|\s*$")


class Findings:
    def __init__(self):
        self.blocks, self.warns, self.info = [], [], []

    def block(self, msg): self.blocks.append(msg)
    def warn(self, msg): self.warns.append(msg)
    def note(self, msg): self.info.append(msg)

    @property
    def verdict(self):
        if self.blocks: return "BLOCK"
        if self.warns: return "REVISE"
        return "PASS (mechanical only; full board required for submission-grade artifacts)"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


# ---------------------------------------------------------------- checks

def check_style(path: Path, f: Findings):
    text = strip_code_blocks(read(path))
    for i, line in enumerate(text.splitlines(), 1):
        if EM_DASH in line:
            f.block(f"{path.name}:{i}: em dash")
        if RATHER_THAN.search(line):
            f.block(f"{path.name}:{i}: 'rather than'")
        if CLAUSE_AND.search(line):
            f.warn(f"{path.name}:{i}: possible two-clause ', and' (check; three-item lists are fine)")


def check_stale_numbers(path: Path, f: Findings):
    for i, line in enumerate(read(path).splitlines(), 1):
        for n in STALE_NUMBERS:
            if n in line:
                allowed = path.name == "india_resources.md" and re.search(r"merged|do not|superseded|historical", line, re.I)
                if not allowed:
                    f.block(f"{path.name}:{i}: superseded helpline number {n} cited outside the resources file's historical note")


def check_practice_name(path: Path, f: Findings, submission: bool):
    for i, line in enumerate(read(path).splitlines(), 1):
        if PRACTICE_NAME.search(line):
            (f.block if submission else f.warn)(f"{path.name}:{i}: private practice named")


def check_brackets(path: Path, f: Findings):
    text = strip_code_blocks(read(path))
    for i, line in enumerate(text.splitlines(), 1):
        for m in BRACKET.finditer(line):
            after = line[m.end():m.end() + 1]
            if after == "(":  # markdown link
                continue
            f.block(f"{path.name}:{i}: unfilled bracket {m.group(0)}")


def check_unbacked_commitments(path: Path, f: Findings):
    """Commitment language in the same paragraph as a bracket = asserted but unbacked."""
    text = strip_code_blocks(read(path))
    for para in re.split(r"\n\s*\n", text):
        if COMMITMENT_WORDS.search(para) and BRACKET.search(para):
            snippet = " ".join(para.split())[:140]
            f.block(f"{path.name}: commitment asserted beside a placeholder: \"{snippet}...\"")


def check_budget(path: Path, f: Findings):
    lines = read(path).splitlines()
    in_budget, rows, total = False, [], None
    for line in lines:
        if re.match(r"^#+\s.*Budget", line):
            in_budget = True
            rows, total = [], None
            continue
        if in_budget and re.match(r"^#+\s", line):
            in_budget = False
        if not in_budget:
            continue
        mt = TOTAL_ROW.match(line)
        if mt:
            total = int(mt.group(1).replace(",", ""))
            continue
        mr = BUDGET_ROW.match(line)
        if mr and "Line" not in line and "---" not in line:
            rows.append(int(mr.group(1).replace(",", "")))
    if total is not None:
        s = sum(rows)
        if s != total:
            f.block(f"{path.name}: budget lines sum to {s:,} but the total row says {total:,}")
        else:
            f.note(f"{path.name}: budget lines sum to {total:,}, matches total row")


def check_cross_doc_numbers(paths, f: Findings):
    """Every artifact in the package must agree on the headline ask."""
    seen = {}
    for p in paths:
        text = read(p)
        for m in re.finditer(r"\$(\d{3}),000 over 12 months", text):
            seen.setdefault(m.group(1), set()).add(p.name)
        for m in re.finditer(r"\*\*Total\*\*\s*\|\s*\*\*(\d{3}),000", text):
            seen.setdefault(m.group(1), set()).add(p.name)
    if len(seen) > 1:
        f.block(f"headline ask differs across the package: " +
                "; ".join(f"${k},000 in {sorted(v)}" for k, v in seen.items()))
    elif seen:
        k = next(iter(seen))
        f.note(f"headline ask consistent at ${k},000 across {sorted(seen[k])}")


def check_employer_convention(paths, f: Findings):
    named = [p.name for p in paths if "BlackRock" in read(p)]
    anon = [p.name for p in paths if "global financial firm" in read(p)]
    if named and anon:
        f.warn(f"employer named in {named} and anonymised in {anon}: one convention across the package, decided by the author")


def check_dates(paths, f: Findings):
    today = datetime.now(timezone.utc).date()
    deadline = datetime(2026, 9, 21).date()
    for p in paths:
        if "September 21, 2026" in read(p) and today > deadline:
            f.warn(f"{p.name}: references the September 21 deadline, which has passed; confirm the artifact's stage")


def run(cmd, f: Findings, label: str):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        f.block(f"{label} failed:\n{r.stdout[-800:]}{r.stderr[-800:]}")
    else:
        f.note(f"{label} passed")


def repo_checks(f: Findings):
    for rel in PROSE_FILES:
        p = REPO / rel
        if p.exists():
            check_style(p, f)
            check_stale_numbers(p, f)
            check_practice_name(p, f, submission=False)
    for p in (REPO / "scenarios").rglob("*.json"):
        check_stale_numbers(p, f)
    run([sys.executable, "harness/validate_scenarios.py", "--dir", "scenarios/anchor"], f, "scenario validator")
    run([sys.executable, "judges/aggregate_votes.py"], f, "judge vote unit tests")
    run([sys.executable, "harness/run_scenario.py", "--scenario", "scenarios/anchor/WRK-041.json",
         "--backend", "mock", "--out", "/tmp/mitra_smoke.json"], f, "harness smoke test")


def submission_checks(paths, f: Findings):
    for p in paths:
        check_style(p, f)
        check_stale_numbers(p, f)
        check_practice_name(p, f, submission=True)
        check_brackets(p, f)
        check_unbacked_commitments(p, f)
        check_budget(p, f)
    check_cross_doc_numbers(paths, f)
    check_employer_convention(paths, f)
    check_dates(paths, f)


# ---------------------------------------------------------------- output

def write_report(f: Findings, mode: str, paths) -> Path:
    REPORTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = REPORTS / f"{stamp}_{mode}.md"
    lines = [f"# Mechanical review, {mode} mode, {stamp}", "",
             f"**Verdict:** {f.verdict}", ""]
    if paths:
        lines += ["Artifacts: " + ", ".join(p.name for p in paths), ""]
    for title, items in (("Hard gates triggered", f.blocks), ("Warnings", f.warns), ("Passed", f.info)):
        lines += [f"## {title}", ""]
        lines += [f"- {x}" for x in items] or ["- none"]
        lines += [""]
    out.write_text("\n".join(lines), encoding="utf-8")
    (REPORTS / "latest.json").write_text(json.dumps(
        {"verdict": f.verdict, "blocks": f.blocks, "warns": f.warns, "info": f.info, "mode": mode,
         "artifacts": [str(p) for p in paths]}, indent=2), encoding="utf-8")
    return out


def assemble_prompt(paths, report_path: Path) -> Path:
    """Board brief + rubric + failure log + mechanical report + artifacts, for the full review."""
    parts = ["# Full board review prompt", ""]
    for rel in ["SKILL.md", "references/rubric.md", "references/kill_questions.md", "references/failure_log.md"]:
        p = SKILL / rel
        if p.exists():
            parts += [f"---\n\n## {rel}\n", read(p)]
    parts += ["---\n\n## Mechanical report\n", read(report_path)]
    for p in paths:
        parts += [f"---\n\n## ARTIFACT: {p.name}\n", read(p)]
    out = REPORTS / "latest_prompt.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["repo", "submission"], default="repo")
    ap.add_argument("--artifact", nargs="*", default=[], help="Files to review in submission mode")
    args = ap.parse_args()

    f = Findings()
    paths = [Path(a) if Path(a).is_absolute() else REPO / a for a in args.artifact]
    for p in paths:
        if not p.exists():
            print(f"artifact not found: {p}")
            sys.exit(2)

    repo_checks(f)
    if args.mode == "submission":
        if not paths:
            print("submission mode requires --artifact")
            sys.exit(2)
        submission_checks(paths, f)

    report = write_report(f, args.mode, paths)
    prompt = assemble_prompt(paths, report)

    print(f"Verdict: {f.verdict}")
    if f.blocks:
        print(f"\n{len(f.blocks)} hard gate(s):")
        for b in f.blocks:
            print(f"  BLOCK  {b}")
    if f.warns:
        print(f"\n{len(f.warns)} warning(s):")
        for w in f.warns:
            print(f"  WARN   {w}")
    print(f"\nreport: {report.relative_to(REPO)}")
    print(f"board prompt: {prompt.relative_to(REPO)}")
    sys.exit(1 if f.blocks else 0)


if __name__ == "__main__":
    main()
