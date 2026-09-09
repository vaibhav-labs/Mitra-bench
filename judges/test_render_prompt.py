#!/usr/bin/env python3
"""
Tests for judges/render_prompt.py. Run directly: python3 judges/test_render_prompt.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_prompt import render, REPO  # noqa: E402


def test_wrk041_d6_matches_documented_example():
    out = render(REPO / "scenarios/anchor/WRK-041.json", 6, "D6")
    assert "personalisation" in out
    assert "sab meri hi galti hai shayad" in out
    assert "Distortion handling" in out
    assert "S2" in out
    assert "<populated at run time from the model under test>" in out
    print("PASS: WRK-041 turn 6 D6 render matches the documented worked example")


def test_fin018_d5_shows_no_applicability_precondition():
    out = render(REPO / "scenarios/anchor/FIN-018.json", 7, "D5")
    assert "always applicable" in out
    assert "note likhne mein" in out  # the harmful-task request text is present for the judge to see
    print("PASS: FIN-018 turn 7 D5 renders with the correct default applicability text")


def test_protective_task_note_included_when_present():
    out = render(REPO / "scenarios/anchor/FIN-018.json", 7, "D5")
    assert "HARMFUL-COURSE TASK" in out, "the scenario's protective_task_note should be inlined for this checkpoint"
    print("PASS: protective_task_note is correctly inlined when present")


def test_protective_task_note_omitted_when_absent():
    out = render(REPO / "scenarios/anchor/WRK-041.json", 6, "D6")
    assert "{{#if" not in out and "{{protective_task_note}}" not in out, "template conditionals must never leak into the rendered output"
    print("PASS: no unresolved template conditionals leak into a checkpoint with no protective_task_note")


def test_wrong_dimension_at_checkpoint_raises():
    try:
        render(REPO / "scenarios/anchor/WRK-041.json", 1, "D6")
        raise AssertionError("expected a ValueError for D6 at a checkpoint that does not score it")
    except ValueError as e:
        assert "not scored at turn 1" in str(e)
        print("PASS: rendering a dimension not scored at a checkpoint raises cleanly, does not silently produce a bogus prompt")


def test_cue_events_after_checkpoint_are_excluded():
    """A judge scoring an early checkpoint must never see cues that haven't
    happened yet in the scripted conversation; this is a correctness
    property, not just a formatting nicety."""
    out = render(REPO / "scenarios/anchor/WRK-041.json", 3, "D1")
    assert "sab chhod ke" not in out, "turn-6 cue text leaked into a turn-3 judge prompt"
    assert "sab meri hi galti hai" not in out
    print("PASS: cue events from later turns are correctly excluded from an earlier checkpoint's prompt")


if __name__ == "__main__":
    test_wrk041_d6_matches_documented_example()
    test_fin018_d5_shows_no_applicability_precondition()
    test_protective_task_note_included_when_present()
    test_protective_task_note_omitted_when_absent()
    test_wrong_dimension_at_checkpoint_raises()
    test_cue_events_after_checkpoint_are_excluded()
    print("\nAll render_prompt tests passed.")
