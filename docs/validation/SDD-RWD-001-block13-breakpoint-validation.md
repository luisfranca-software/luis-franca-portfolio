# SDD-RWD-001 — Block 13 Breakpoint Finalization Evidence

Status: COMPLETE / PENDING HUMAN REVIEW

## Authority and method

Block 12's immutable measurement history remains the intrinsic-fit authority:
`artifacts/responsive-fit/block12-fit-measurements.json`. Block 13 applied its
more demanding EN/PT-BR constraints, then repeated the integer-width Chromium
sweep from 360 through 1440 CSS px. The post-implementation record is
`artifacts/responsive-fit/block13-fit-validation.json`; its 26 boundary images
are under `artifacts/responsive-fit/block13-screenshots/`.

Environment: Chromium 151.0.7922.108 (snap), headless, DPR 1, zoom 100%, 900px
viewport height, Linux x86_64. Every final boundary was probed at N-1/N/N+1 in
English and Brazilian Portuguese with computed mode, geometry, overflow,
collision, and destructive-word-break checks.

## Final inventory and decisions

| FIT | Block 12 measured | Final production threshold | Consolidation | Post-implementation result | State |
| --- | ---: | ---: | --- | --- | --- |
| FIT-HDR-001 | 848px | 848px | Independent | 847 Compact; 848/849 Full | FIT-VALIDATED |
| FIT-HERO-001 | 967px | 967px | Independent | 966 Stacked; 967/968 Split | FIT-VALIDATED |
| FIT-ENG-001 | 640px | 640px / 40rem | 640 family | 639 1-col; 640/641 2-col | FIT-VALIDATED |
| FIT-ENG-002 | 1200px | 1200px / 75rem | 1200 family | 1199 2-col; 1200/1201 4-col | FIT-VALIDATED |
| FIT-PRJ-001 | 896px | 896px / 56rem | 896 family | 895 1-col; 896/897 2-col | FIT-VALIDATED |
| FIT-PRJ-002 | 1200px | 1200px / 75rem | 1200 family | 1199 2-col; 1200/1201 3-col | FIT-VALIDATED |
| FIT-PRC-001 | 640px | 640px / 40rem | 640 family | 639 Vertical; 640/641 Grid2 | FIT-VALIDATED |
| FIT-PRC-002 | 896px | 896px / 56rem | 896 family | 895 Grid2; 896/897 Grid3 | FIT-VALIDATED |
| FIT-PRC-003 | 1200px | 1200px / 75rem | 1200 family | 1199 Grid3; 1200/1201 Horizontal | FIT-VALIDATED |
| FIT-EVD-001 | 640px | 640px / 40rem | 640 family | 639 1-col; 640/641 2-col | FIT-VALIDATED |
| FIT-EVD-002 | 1200px | 1200px / 75rem | 1200 family | 1199 2-col; 1200/1201 4-col | FIT-VALIDATED |
| FIT-EVD-003 | 1200px | 1200px / 75rem | 1200 family | 1199 Stacked; 1200/1201 Side | FIT-VALIDATED |
| FIT-FTR-001 | 640px | 640px / 40rem | 640 family | 639 Stacked; 640/641 Horizontal | FIT-VALIDATED |

The rem values use the unchanged 16px root size and therefore preserve exact
CSS-pixel boundaries. Selector ownership remains component-local; equivalent
thresholds are conceptually consolidated without coupling unrelated rules.
Header uses `max-width: 847px` so Full begins at 848px. Hero uses the exact
`60.4375rem` equivalent of 967px. Neither was rounded into the 896px family.

## Browser and regression observations

- Both locale sweeps report zero page-level horizontal-overflow widths.
- All 78 boundary probes (13 FITs × 2 locales × 3 widths) are healthy.
- Reference widths 360, 768, 1024, and 1440 and interpolation widths 390, 480,
  640, 820, 900, 1100, and 1280 contain all required sections without overflow
  or destructive text breaks.
- The first finalized sweep exposed PT-BR `Engenheiro` breaking at 1024 because
  an existing 64rem Hero rule reintroduced a 32rem visual-column minimum. The
  redundant grid override was removed; the final sweep is clean. The 64rem
  Explorer sizing remains unchanged.
- Existing semantic, keyboard, disclosure, focus, destination, target-size,
  reduced-motion, and noninteractive AI/RAG contracts pass the automated
  accessibility and Homepage regression suites.

## Preserved Block 14 inputs

HERO-BG-001 remains open and unchanged: the approved background asset is still
authoritative, while its crop/gradient fidelity awaits Block 14. The fixed,
noninteractive AI/RAG visual still overlaps Footer professional/social links at
the diagnostic widths recorded in the machine evidence. It has no FIT and was
not altered in Block 13.

## State boundary

All 13 entries are promoted from FIT-TESTED to FIT-VALIDATED. Breakpoint
finalization is complete. Final visual regression/interpolation acceptance and
final human acceptance remain pending Block 14; Block 14 has not started.
