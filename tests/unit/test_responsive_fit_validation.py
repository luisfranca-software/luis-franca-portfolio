"""Audit contracts for SDD-RWD-001 Block 13 breakpoint finalization."""

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = REPO_ROOT / "artifacts/responsive-fit/block13-fit-validation.json"
FINAL_THRESHOLDS = {
    "FIT-HDR-001": 848,
    "FIT-HERO-001": 967,
    "FIT-ENG-001": 640,
    "FIT-ENG-002": 1200,
    "FIT-PRJ-001": 896,
    "FIT-PRJ-002": 1200,
    "FIT-PRC-001": 640,
    "FIT-PRC-002": 896,
    "FIT-PRC-003": 1200,
    "FIT-EVD-001": 640,
    "FIT-EVD-002": 1200,
    "FIT-EVD-003": 1200,
    "FIT-FTR-001": 640,
}


def _evidence() -> dict[str, Any]:
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def test_every_final_threshold_switches_at_the_validated_boundary() -> None:
    evidence = _evidence()

    assert {locale["locale"] for locale in evidence["locales"]} == {"en-US", "pt-BR"}
    for locale in evidence["locales"]:
        assert locale["sweep"]["page_overflow_widths"] == []
        assert set(locale["transitions"]) == set(FINAL_THRESHOLDS)
        for fit_id, threshold in FINAL_THRESHOLDS.items():
            transition = locale["transitions"][fit_id]
            assert transition["implemented_threshold"] == threshold
            assert transition["mode_switch"] == threshold
            assert transition["measured_transition"] == threshold
            assert transition["state"] == "FIT-VALIDATED"
            assert set(transition["probes"]) == {
                str(threshold - 1),
                str(threshold),
                str(threshold + 1),
            }
            assert all(probe["healthy"] for probe in transition["probes"].values())


def test_final_css_uses_exact_evidence_backed_boundaries() -> None:
    site_css = (REPO_ROOT / "frontend/static/css/site.css").read_text(encoding="utf-8")
    home_css = (REPO_ROOT / "frontend/static/css/home.css").read_text(encoding="utf-8")

    assert "@media (max-width: 847px)" in site_css
    assert "@media (min-width: 60.4375rem)" in home_css
    assert 'window.matchMedia("(min-width: 53rem)")' in (
        REPO_ROOT / "frontend/static/js/site.js"
    ).read_text(encoding="utf-8")
    for shared in ("40rem", "56rem", "75rem"):
        assert f"@media (min-width: {shared})" in home_css
    assert "PROVISIONAL IMPLEMENTATION THRESHOLD" not in site_css + home_css


def test_block12_measurement_history_remains_tested() -> None:
    history = json.loads(
        (REPO_ROOT / "artifacts/responsive-fit/block12-fit-measurements.json").read_text(
            encoding="utf-8"
        )
    )

    assert all(
        transition["state"] == "FIT-TESTED"
        for locale in history["locales"]
        for transition in locale["transitions"].values()
    )
