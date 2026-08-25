"""Audit contracts for SDD-RWD-001 Block 12 browser evidence."""

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = REPO_ROOT / "artifacts/responsive-fit/block12-fit-measurements.json"
EXPECTED_FITS = {
    "FIT-HDR-001",
    "FIT-HERO-001",
    "FIT-ENG-001",
    "FIT-ENG-002",
    "FIT-PRJ-001",
    "FIT-PRJ-002",
    "FIT-PRC-001",
    "FIT-PRC-002",
    "FIT-PRC-003",
    "FIT-EVD-001",
    "FIT-EVD-002",
    "FIT-EVD-003",
    "FIT-FTR-001",
}


def _evidence() -> dict[str, Any]:
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def test_fit_evidence_records_real_browser_environment_and_inventory() -> None:
    evidence = _evidence()

    assert evidence["environment"]["browser"].startswith("Chromium ")
    assert evidence["environment"]["headless"] is True
    assert evidence["environment"]["css_pixels_authoritative"] is True
    assert set(evidence["fit_inventory"]) == EXPECTED_FITS


def test_every_fit_has_two_locale_boundary_evidence_and_tested_state() -> None:
    evidence = _evidence()

    assert {entry["locale"] for entry in evidence["locales"]} == {"en-US", "pt-BR"}
    for locale in evidence["locales"]:
        assert set(locale["transitions"]) == EXPECTED_FITS
        assert locale["sweep"] == {
            "from": 360,
            "through": 1440,
            "step_css_px": 1,
            "page_overflow_widths": [],
        }
        for transition in locale["transitions"].values():
            boundary = transition["first_healthy_larger_mode_width"]
            assert transition["state"] == "FIT-TESTED"
            assert "FIT-VALIDATED" not in json.dumps(transition)
            assert set(transition["probes"]) == {
                str(boundary - 1),
                str(boundary),
                str(boundary + 1),
            }
            screenshot = REPO_ROOT / "artifacts" / transition["screenshot"]
            assert screenshot.is_file()


def test_reference_widths_are_complete_and_collision_observations_are_recorded() -> None:
    for locale in _evidence()["locales"]:
        for width in (360, 768, 1024, 1440):
            diagnostic = locale["diagnostics"][str(width)]
            assert diagnostic["content"]["h1"] == 1
            assert diagnostic["content"]["sections"] is True
            assert diagnostic["overflow"]["page"] is False
        assert locale["ai_rag_collision_observations"]
