# SDD-RWD-001 — Isolated Portrait Effect Diagnosis and Removal

Date: 2026-08-23<br>
Final state: **PASS — pending human visual review**

## 1. Preflight

Repository `/home/luis/projects/luis-franca-portfolio`, branch `main`, HEAD `10ce72cc9c6cf1481a174c68c3cdfbc41c8f435f`. The cumulative dirty worktree was preserved. No stage, commit, push, reset, clean, restore, checkout, or stash operation was performed.

## 2. Authority inspected

Live Figma file `7XIYTbKZrLk77biI0UhRIb`; reference frames 360 `316:615`, 768 `297:373`, 1024 `270:1357`, and 1440 `153:2`; persisted traceability matrix and integrated-remediation evidence; current Django template, portrait include, Homepage CSS, image bytes, tests, and Chromium harnesses.

## 3. Human-reported symptom

A large blue/translucent rounded luminous geometry appeared behind and above IMG-00 across reference widths.

## 4. Suspected causes

HERO-09A, `.home-hero__depth`, IMG-00 pixels, the portrait wrapper, image `drop-shadow`, Hero container, Code, Explorer, backgrounds, gradients, shadows, filters, pseudo-elements, transforms, and viewport rules were inspected.

## 5–10. Root cause and deterministic mapping

Classification: **B — HERO-09A exists in Figma but the browser implementation rendered the wrong geometry/effect**.

Figma HERO-09A is node `316:704` at 360 and `222:373` at 1440. It contains two localized screen-blended SVG rim lights (cyan-left 420×435 and warm-right 330×410). It is not a single rounded backdrop.

DOM mapping: `[data-trace-id="HERO-09A"].home-hero__portrait-rim`, a noninteractive absolute child of `.home-hero__visual`. CSS mapping: `frontend/static/css/home.css`, `.home-hero__portrait-rim`. The rule created a large empty rounded rectangle using `inset:14% 12% 0 16%`, `border-radius:45% 45% 18% 18%`, `z-index:3`, and `box-shadow:0 0 2rem rgba(0,170,255,.38)`.

This is factual browser evidence, not inference. IMG-00 had transparent background, no box shadow, and the approved responsive asset URLs. Its only filter is a downward black drop shadow. Code and Explorer occupy independent z-index 1/2 rectangles and do not produce the cyan rounded geometry. Portrait master SHA-256 remains `1c2a24c2d8e9fa5b46fb29cf9907d0998166bf419ae9e6b8941d0d846aadbebc`.

## 11. Before evidence

Screenshots and computed evidence: `artifacts/responsive-visual/portrait-effect/before/`. Before HERO-09A rectangles were:

| Width | X | Y | Width | Height | Computed effect |
|---:|---:|---:|---:|---:|---|
| 360 | 68.80 | 676.59 | 219.61 | 430.00 | rounded cyan 32px shadow |
| 768 | 142.23 | 592.89 | 496.09 | 516.00 | rounded cyan 32px shadow |
| 1024 | 572.80 | 240.88 | 345.61 | 467.84 | rounded cyan 32px shadow |
| 1440 | 865.52 | 186.58 | 438.42 | 330.25 | rounded cyan 32px shadow |

## 12. Correction

The smallest safe correction adds `display:none` to `.home-hero__portrait-rim`. The DOM node and `HERO-09A` traceability remain. No structural wrapper or other property was changed.

## 13–17. After evidence and exact-width comparison

Screenshots and computed evidence: `artifacts/responsive-visual/portrait-effect/after/`.

| Width | BEFORE → AFTER | Protected geometry |
|---:|---|---|
| 360 | 219.61×430 shadow rectangle → `display:none`, 0×0 | portrait, image, visual, Code, Explorer exact rectangles unchanged |
| 768 | 496.09×516 shadow rectangle → `display:none`, 0×0 | exact rectangles unchanged |
| 1024 | 345.61×467.84 shadow rectangle → `display:none`, 0×0 | exact rectangles unchanged |
| 1440 | 438.42×330.25 shadow rectangle → `display:none`, 0×0 | exact rectangles unchanged |

At every width the selected portrait asset URL is unchanged and page overflow remains false. Header, background, downstream sections, and AIR-00 were not mutated.

## 18. Interpolation and FIT safety

The Chromium harness passed 390, 480, 640, 820, 900, 1100, and 1280 for EN and PT-BR with no new page overflow, missing portrait/Code/Explorer, or collision. `after/full-width-sweep.json` validates 360–1440 and preserves all 13 FIT-VALIDATED states and thresholds.

## 19–21. Tests and quality gates

- Focused Hero/responsive/Homepage/FIT regression: **39 passed**.
- Full pytest with PostgreSQL settings: **299 passed**.
- Ruff: **passed**.
- mypy application: **passed, 87 source files**.
- mypy tests: **passed, 44 source files**.
- Django system check: **passed, 0 issues**.
- Structure, documentation, naming, and secrets checks: **passed**.
- `git diff --check`: **passed**.

## 22. Protected-baseline audit

No Hero redesign; no portrait asset/srcset/intrinsic/crop/position mutation; no Code or Explorer mutation; no breakpoint/FIT change; no global overflow mask; no fixed height; no Header/background/downstream/AIR/non-Homepage/JavaScript/backend/Figma/dependency mutation.

## 23. Files changed by this task

- `frontend/static/css/home.css` — one `display:none` declaration.
- `tests/integration/test_home_hero.py` — focused regression.
- this report.
- before/after screenshots and machine-readable browser evidence under `artifacts/responsive-visual/portrait-effect/`.

All other dirty-worktree changes pre-existed this isolated task.

## 24. Remaining risks

The rejected browser approximation is disabled rather than replaced with Figma's two SVG rim lights, because this task authorizes removal only and explicitly excludes a new Hero technological-background design cycle. Human visual review remains required.

## 25. Acceptance matrix

| Criteria | Result | Criteria | Result |
|---|---|---|---|
| PE-AC-001 | PASS | PE-AC-020 | PASS |
| PE-AC-002 | PASS | PE-AC-021 | PASS |
| PE-AC-003 | PASS | PE-AC-022 | PASS |
| PE-AC-004 | PASS | PE-AC-023 | PASS |
| PE-AC-005 | PASS | PE-AC-024 | PASS |
| PE-AC-006 | PASS | PE-AC-025 | PASS |
| PE-AC-007 | PASS | PE-AC-026 | PASS |
| PE-AC-008 | PASS | PE-AC-027 | PASS |
| PE-AC-009 | PASS | PE-AC-028 | PASS |
| PE-AC-010 | PASS | PE-AC-029 | PASS |
| PE-AC-011 | PASS | PE-AC-030 | PASS |
| PE-AC-012 | PASS | PE-AC-031 | PASS |
| PE-AC-013 | PASS | PE-AC-032 | PASS |
| PE-AC-014 | PASS | PE-AC-033 | PASS |
| PE-AC-015 | PASS | PE-AC-034 | PASS |
| PE-AC-016 | PASS | PE-AC-035 | PASS |
| PE-AC-017 | PASS | PE-AC-036 | PASS |
| PE-AC-018 | PASS | PE-AC-037 | PASS |
| PE-AC-019 | PASS | PE-AC-038 | PASS |

## 26. Final gate

**PORTRAIT-EFFECT-ISOLATION — PASS — READY FOR HUMAN VISUAL REVIEW**
