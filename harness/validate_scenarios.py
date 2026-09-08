#!/usr/bin/env python3
"""
MITRA-Bench scenario validator.

Checks every scenario JSON file against scenario.schema.json, then applies
the WS3 authoring checklist rules that a JSON Schema can't express on its own
(cross-field logic: window references a real cue, checkpoints reference real
dimensions for the taxonomy version in use, canaries are unique, etc.).

Usage:
    python3 validate_scenarios.py [--dir scenarios/anchor]

Exit code 0 = all scenarios pass. Non-zero = at least one failure, printed
with the scenario id and the specific rule violated.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Missing dependency: pip install jsonschema --break-system-packages")
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "scenarios" / "scenario.schema.json"


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def checklist_rules(scenario, path):
    """WS3 checklist items not expressible purely in JSON Schema."""
    errors = []
    sid = scenario.get("id", "UNKNOWN")

    # Adult persona (belt-and-braces on top of the schema const)
    if not scenario.get("persona", {}).get("adult", False):
        errors.append(f"{sid}: persona.adult must be true (adult-persona rule)")

    # Window's opening cue must exist among cue_events
    cue_ids = {c["cue_id"] for c in scenario.get("cue_events", [])}
    opening = scenario.get("window", {}).get("opening_cue_id")
    if opening not in cue_ids:
        errors.append(f"{sid}: window.opening_cue_id '{opening}' not found in cue_events")

    # Every checkpoint turn must exist among turns
    turn_numbers = {t["turn"] for t in scenario.get("turns", [])}
    for cp in scenario.get("checkpoints", []):
        if cp["turn"] not in turn_numbers:
            errors.append(f"{sid}: checkpoint at turn {cp['turn']} has no matching turn entry")

    # Pass band must be consistent with the taxonomy's severity->band table
    expected_bands = {
        "S0": {"L0", "L1"},
        "S1": {"L1", "L2"},
        "S2": {"L2", "L3"},
        "S3": {"L3"},
    }
    for cp in scenario.get("checkpoints", []):
        sev = cp["severity"]
        band = set(cp["pass_band"])
        if not band.issubset(expected_bands.get(sev, set())) or not band:
            errors.append(
                f"{sid}: checkpoint at turn {cp['turn']} (severity {sev}) has pass_band "
                f"{cp['pass_band']}, expected a non-empty subset of {sorted(expected_bands[sev])}"
            )

    # D5-scoring checkpoints should carry a protective_task_note (WS2 Section 5 rule)
    for cp in scenario.get("checkpoints", []):
        if "D5" in cp.get("dimensions_to_score", []) and not cp.get("protective_task_note"):
            errors.append(
                f"{sid}: checkpoint at turn {cp['turn']} scores D5 but has no "
                f"protective_task_note (required by the protective-vs-harmful task rule)"
            )

    # Content notice must be set if peak severity is S2 or S3
    if scenario.get("peak_severity") in ("S2", "S3") and scenario.get("content_notice_level") == "none":
        errors.append(f"{sid}: peak_severity {scenario['peak_severity']} requires a content_notice_level")

    # Canary must be present and look like a canary
    canary = scenario.get("canary", "")
    if "MITRA-BENCH-CANARY" not in canary:
        errors.append(f"{sid}: canary string missing or malformed")

    # Recovery-class scenarios must carry a prefill
    if scenario.get("class_flags", {}).get("recovery") and not scenario.get("prefill"):
        errors.append(f"{sid}: class_flags.recovery is true but prefill is null")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="scenarios/anchor", help="Directory of scenario JSON files to validate")
    args = parser.parse_args()

    scenario_dir = REPO_ROOT / args.dir
    schema = load_schema()

    files = sorted(scenario_dir.glob("*.json"))
    if not files:
        print(f"No scenario files found in {scenario_dir}")
        sys.exit(1)

    all_errors = []
    canaries_seen = {}

    for path in files:
        with open(path) as f:
            scenario = json.load(f)

        # JSON Schema validation
        try:
            jsonschema.validate(instance=scenario, schema=schema)
        except jsonschema.ValidationError as e:
            all_errors.append(f"{path.name}: SCHEMA ERROR: {e.message} (at {'/'.join(str(p) for p in e.path)})")
            continue  # cross-field checks assume schema validity

        # Cross-field checklist rules
        errors = checklist_rules(scenario, path)
        all_errors.extend(errors)

        # Canary uniqueness across the whole set
        canary = scenario.get("canary")
        if canary in canaries_seen:
            all_errors.append(f"{path.name}: canary duplicates {canaries_seen[canary]}")
        else:
            canaries_seen[canary] = path.name

    print(f"Validated {len(files)} scenario(s) in {scenario_dir}")
    if all_errors:
        print(f"\n{len(all_errors)} error(s):\n")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("All scenarios pass schema validation and the WS3 checklist rules.")
        sys.exit(0)


if __name__ == "__main__":
    main()
