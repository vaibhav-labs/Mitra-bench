#!/usr/bin/env python3
"""
MITRA-Bench screen validator. Checks generated screen items against the
schema and against cross-references into the lexicon (every screen item
must trace to a real, screen-eligible lexicon entry).

Usage: python3 screen/validate_screen.py
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
SCHEMA = ROOT / "screen_item.schema.json"
ITEMS = ROOT / "seed_screen_items.json"
LEXICON = ROOT.parent / "lexicon" / "seed_lexicon.json"


def main():
    schema = json.load(open(SCHEMA))
    items = json.load(open(ITEMS))
    lexicon_by_id = {e["id"]: e for e in json.load(open(LEXICON))}

    errors = []
    seen_ids, seen_canaries = set(), set()

    for it in items:
        try:
            jsonschema.validate(instance=it, schema=schema)
        except jsonschema.ValidationError as err:
            errors.append(f"{it.get('id', '?')}: SCHEMA ERROR: {err.message}")
            continue

        if it["id"] in seen_ids:
            errors.append(f"{it['id']}: duplicate id")
        seen_ids.add(it["id"])

        if it["canary"] in seen_canaries:
            errors.append(f"{it['id']}: duplicate canary")
        seen_canaries.add(it["canary"])

        lex = lexicon_by_id.get(it["lexicon_id"])
        if lex is None:
            errors.append(f"{it['id']}: references lexicon_id {it['lexicon_id']} which does not exist")
            continue

        if not lex.get("screen_eligible", True):
            errors.append(f"{it['id']}: derived from {it['lexicon_id']}, which is marked screen_eligible=false")

        if it["severity_association"] != lex["severity_association"]:
            errors.append(
                f"{it['id']}: severity {it['severity_association']} does not match "
                f"source lexicon entry's severity {lex['severity_association']}"
            )

        if it["language_register"] != lex["register"]:
            errors.append(
                f"{it['id']}: register {it['language_register']} does not match "
                f"source lexicon entry's register {lex['register']}"
            )

        # D2 and D5 can never apply to a single-turn item
        if "D2" in it["dimensions_applicable"] or "D5" in it["dimensions_applicable"]:
            errors.append(f"{it['id']}: lists D2 or D5 as applicable; neither can be tested in a single turn")

    print(f"Validated {len(items)} screen items against {len(lexicon_by_id)} lexicon entries.")
    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("All screen items pass schema validation and lexicon cross-referencing.")
    sys.exit(0)


if __name__ == "__main__":
    main()
