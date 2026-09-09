#!/usr/bin/env python3
"""
MITRA-Bench lexicon validator. Checks the seed lexicon against its schema
and against the WS2 acceptance criterion from the development plan: every
entry must have a register, a severity association and a source type
(enforced structurally by the schema's "required" list, verified here again
explicitly so a future schema relaxation can't silently drop the guarantee).

Usage: python3 lexicon/validate_lexicon.py
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Missing dependency: pip install jsonschema --break-system-packages")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "lexicon.schema.json"
SEED = ROOT / "seed_lexicon.json"


def main():
    schema = json.load(open(SCHEMA))
    entries = json.load(open(SEED))

    errors = []
    seen_ids, seen_phrases = set(), set()
    severity_counts = {"S0": 0, "S1": 0, "S2": 0, "S3": 0}
    register_counts = {}
    channel_counts = {}

    for e in entries:
        try:
            jsonschema.validate(instance=e, schema=schema)
        except jsonschema.ValidationError as err:
            errors.append(f"{e.get('id', '?')}: SCHEMA ERROR: {err.message}")
            continue

        # WS2 acceptance criterion, checked explicitly and not just via schema "required"
        for field in ("register", "severity_association", "source_type"):
            if not e.get(field):
                errors.append(f"{e['id']}: missing required field '{field}' (WS2 acceptance criterion)")

        if e["id"] in seen_ids:
            errors.append(f"{e['id']}: duplicate id")
        seen_ids.add(e["id"])

        phrase_key = e["phrase"].strip().lower()
        if phrase_key in seen_phrases:
            errors.append(f"{e['id']}: duplicate phrase text")
        seen_phrases.add(phrase_key)

        severity_counts[e["severity_association"]] += 1
        register_counts[e["register"]] = register_counts.get(e["register"], 0) + 1
        channel_counts[e["channel"]] = channel_counts.get(e["channel"], 0) + 1

    print(f"Validated {len(entries)} lexicon entries.")
    print(f"Severity coverage: {severity_counts}")
    print(f"Register coverage: {register_counts}")
    print(f"Channel coverage:  {channel_counts}")

    # Coverage warnings (not hard failures for a seed set, but flagged)
    for sev, count in severity_counts.items():
        if count == 0:
            print(f"  WARNING: zero entries at severity {sev}")
    for ch in ("somatic_idiom", "direct_verbal", "cognitive_distortion", "behavioural_report", "third_party_framing"):
        if channel_counts.get(ch, 0) == 0:
            print(f"  WARNING: zero entries for channel {ch}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("\nAll lexicon entries pass schema validation and the WS2 acceptance criterion.")
    sys.exit(0)


if __name__ == "__main__":
    main()
