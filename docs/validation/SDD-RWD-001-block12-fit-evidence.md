# SDD-RWD-001 — Block 12 Intrinsic-Fit Browser Evidence

Status: COMPLETE / PENDING HUMAN REVIEW

## Environment and method

- Chromium 151.0.7922.108 (snap), headless, Linux x86_64.
- CSS viewport pixels are authoritative; device pixel ratio 1; zoom 100%.
- Viewport height: 900 CSS px.
- Locales: English (`en-US`) and Brazilian Portuguese (`pt-BR`).
- Progressive sweep: every integer width from 360 through 1440 CSS px.
- Boundary probes: N-1, N, and N+1 with rendered mode, geometry, overflow,
  collision, and destructive intra-word-break evidence.
- Machine-readable authority: `artifacts/responsive-fit/block12-fit-measurements.json`.
- Boundary screenshots: `artifacts/responsive-fit/screenshots/`.

Reference widths are validation states, not automatically final breakpoints.
Block 13 owns final threshold selection and consolidation.

## FIT evidence

| FIT | SDD interval | Provisional switch | EN first healthy larger mode | PT-BR first healthy larger mode | Effective measured constraint | Limiting evidence | State |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| FIT-HDR-001 | >768–1024 | 769 | 839 | 848 | 848 | Full Header remains multi-row through 847 in PT-BR; 848/849 are single-row and collision-free. | FIT-TESTED |
| FIT-HERO-001 | >768–1024 | 769 | 885 | 967 | 967 | Split Hero destructively breaks title words through 966 in PT-BR; 967/968 preserve whole words and containment. | FIT-TESTED |
| FIT-ENG-001 | >360–768 | 640 | 640 | 640 | 640 | 639 is healthy one-column; 640/641 are healthy two-column with readable intrinsic cards. | FIT-TESTED |
| FIT-ENG-002 | >1024–1440 | 1200 | 1200 | 1200 | 1200 | 1199 is healthy two-column; 1200/1201 are healthy four-column without card overflow. | FIT-TESTED |
| FIT-PRJ-001 | >768–1024 | 896 | 896 | 896 | 896 | 895 is healthy one-column; 896/897 are healthy two-column with the final card centered. | FIT-TESTED |
| FIT-PRJ-002 | >1024–1440 | 1200 | 1200 | 1200 | 1200 | 1199 is healthy two-column; 1200/1201 are healthy three-column with intact tags and actions. | FIT-TESTED |
| FIT-PRC-001 | >360–768 | 640 | 640 | 640 | 640 | 639 is healthy Vertical; 640/641 are healthy Grid2 with intact connectors and order. | FIT-TESTED |
| FIT-PRC-002 | >768–1024 | 896 | 896 | 896 | 896 | 895 is healthy Grid2; 896/897 are healthy Grid3 with centered Validation. | FIT-TESTED |
| FIT-PRC-003 | >1024–1440 | 1200 | 1200 | 1200 | 1200 | 1199 is healthy Grid3; 1200/1201 are readable Horizontal mode with intact connectors. | FIT-TESTED |
| FIT-EVD-001 | >360–768 | 640 | 640 | 640 | 640 | 639 is healthy one-column; 640/641 are healthy two-column evidence grids. | FIT-TESTED |
| FIT-EVD-002 | >1024–1440 | 1200 | 1200 | 1200 | 1200 | 1199 is healthy two-column; 1200/1201 are healthy four-column evidence grids. | FIT-TESTED |
| FIT-EVD-003 | >1024–1440 | 1200 | 1200 | 1200 | 1200 | 1199 is healthy stacked; 1200/1201 preserve useful Evidence and CTA widths side-by-side. | FIT-TESTED |
| FIT-FTR-001 | >360–768 | 640 | 640 | 640 | 640 | 639 is healthy stacked; 640/641 are readable horizontal layouts in both locales. | FIT-TESTED |

The effective measured constraint uses the more demanding locale. These are
Block 12 measurements, not final CSS decisions.

## Reference and interpolation observations

- English and PT-BR render complete required content at 360, 768, 1024, and
  1440 CSS px.
- Diagnostic probes at 390, 480, 640, 820, 900, 1100, and 1280 show no
  page-level horizontal overflow after the isolated Hero correction.
- No required component collision was detected in Header or Hero geometry.
- Source order and DOM semantics remain unchanged across every mode.

## AI/RAG collision observation

The fixed AI/RAG reserved visual overlaps the Footer professional-link region
when the Footer is brought to the viewport at most diagnostic widths, including
360, 390, 640, 768, 820, 900, 1024, 1100, 1200, 1280, and 1440 in both locales.
It does not obscure the Contact CTA in the recorded probes. AI/RAG has no FIT
ID, so this observation is recorded separately and remains an acceptance input
for later collision/visual validation; no new FIT or Block 13 change is created.

## HERO-BG-001

HERO-BG-001 remains open. Chromium confirms the approved
`homepage-background-desktop-02.png` authority at every diagnostic width, with
the current centered-top `max(100%, 933px) auto` treatment. The rendered crop
and gradient continue to suppress portions of the approved luminous
arc/particle continuity relative to the Figma authority. The deviation is
visible across stacked and split widths and is preserved for Block 14; no
visual redesign was authorized in Block 12.

## Measurement-enabling correction

At 1024–1070 CSS px, the split Hero's 64rem rule previously forced 29rem and
32rem minimum columns plus the gap into a 928px reference container. Chromium
measured a 1072px document width at the 1024px reference. The redundant first
column minimum was changed from `minmax(29rem, 0.9fr)` to
`minmax(0, 0.9fr)`. No media-query threshold changed. The final sweep records
zero page-overflow widths in both locales from 360 through 1440.

## State boundary

All 13 candidates transition from FIT-CANDIDATE to FIT-TESTED. None is
FIT-VALIDATED. Breakpoint finalization and consolidation remain pending Block
13. Final interpolation and visual-regression acceptance remain pending Block
14.
