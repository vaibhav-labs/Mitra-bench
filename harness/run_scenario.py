#!/usr/bin/env python3
"""
MITRA-Bench minimal harness runner (skeleton).

Drives one scenario turn-by-turn against a pluggable model backend and
records a run record. This is intentionally a skeleton: it proves the data
flow (scenario -> conversation -> transcript -> run record) end to end on a
mocked backend, so that plugging in a real API client later is a small,
well-defined change rather than a redesign.

What this file does NOT yet do (all deferred to post-award, gated as noted):
  - Call a real model API (needs API keys, arm configs -> post-award)
  - Grade the transcript against the answer key (needs frozen rubric -> G3)
  - Run the consumer-approximating arm with a snapshotted system prompt
  - Run five repeats / compute the noise budget (needs the report-card stage)

Usage:
    python3 run_scenario.py --scenario scenarios/anchor/WRK-041.json --backend mock
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class MockBackend:
    """Stand-in model backend. Returns a fixed, clearly-labelled placeholder
    reply so the pipeline can be exercised before any API integration exists.
    Replace with a real backend class implementing the same .reply() signature."""

    name = "mock-backend-v0"

    def reply(self, conversation_history, arm="bare_api"):
        last_user_turn = conversation_history[-1]["text"]
        return (
            f"[MOCK REPLY — backend={self.name}, arm={arm}] "
            f"Placeholder response to: {last_user_turn[:60]}..."
        )


def load_scenario(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def build_conversation(scenario: dict, backend, arm: str) -> list:
    """Interleave scripted user turns with model-generated assistant turns,
    in scripted-turn order. This is the bare skeleton of multi-turn context
    accumulation the real harness will do with actual API calls."""
    conversation = []
    for user_turn in scenario["turns"]:
        conversation.append({"turn": user_turn["turn"], "role": "user", "text": user_turn["text"]})
        assistant_text = backend.reply(conversation, arm=arm)
        conversation.append({"turn": user_turn["turn"], "role": "assistant", "text": assistant_text})
    return conversation


def make_run_record(scenario: dict, conversation: list, backend, arm: str) -> dict:
    return {
        "run_id": f"{scenario['id']}__{backend.name}__{arm}__{int(time.time())}",
        "scenario_id": scenario["id"],
        "scenario_canary": scenario["canary"],
        "model": backend.name,
        "arm": arm,
        "seed": None,
        "temperature": None,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "cost_usd": None,
        "wall_clock_seconds": None,
        "transcript": conversation,
        "note": "SKELETON RUN — mock backend, not a real model. For pipeline validation only.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, help="Path to a scenario JSON file")
    parser.add_argument("--backend", default="mock", choices=["mock"], help="Model backend to use")
    parser.add_argument("--arm", default="bare_api", choices=["bare_api", "consumer_approximating"])
    parser.add_argument("--out", default=None, help="Output path for the run record (default: prints to stdout)")
    args = parser.parse_args()

    scenario_path = Path(args.scenario)
    if not scenario_path.is_absolute():
        scenario_path = REPO_ROOT / scenario_path

    scenario = load_scenario(scenario_path)
    backend = MockBackend()
    conversation = build_conversation(scenario, backend, args.arm)
    run_record = make_run_record(scenario, conversation, backend, args.arm)

    output = json.dumps(run_record, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Run record written to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
