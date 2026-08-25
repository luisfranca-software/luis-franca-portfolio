# SDD-RWD-001 — IMG-02 Continuous Responsive Background

Date: 2026-08-24<br>
Technical status: PASS — ready for mandatory human visual review

## Requirement and authority

IMG-02 must use one canonical Homepage Technology Background, scale continuously from viewport width, retain the canonical 1440:2604 presentation ratio, repeat complete modules vertically, and remain decorative and out of flow. The authority is Figma file `7XIYTbKZrLk77biI0UhRIb`, page `02 — Homepage`, frame `Homepage / Desktop v1`, node `199:1358`, geometry 1440×2604, image hash `b06fb16c56279829bc6adb74058b8d60081e5854`.

The repository authority is `frontend/static/images/background/homepage-background-desktop-02.png`. Its SHA-1 is exactly `b06fb16c56279829bc6adb74058b8d60081e5854`; no image was created or changed. The stored Figma export is 933×1686 because it is a downsampled raster representation; browser geometry is governed by the canonical Figma presentation dimensions.

## Previous defect and technical decision

`.homepage__technology-background` previously used `center center / cover no-repeat`. Since the absolute owner spans the complete Homepage document, `cover` scaled/cropped the artwork against page height, produced a document-dependent crop, and stopped after one image.

The dedicated existing decorative DOM owner remains unchanged. Its CSS now uses the same canonical image with `background-position:center top`, `background-size:100vw auto`, and `background-repeat:repeat-y`. `100vw` is intentional: Chromium's classic scrollbar makes the containing block 15 CSS pixels narrower than the requested viewport, while the requirement defines module width from viewport width. Background painting does not create layout overflow. No breakpoint-specific IMG-02 rule, overlay, filter, JavaScript listener, duplicate asset, fixed page height, or tile count exists.

The formula is:

`scale = viewport_width / 1440`

`module_width = viewport_width`

`module_height = 2604 × viewport_width / 1440`

## Checkpoints, interpolation, and growth

Chromium 151 at DPR 1 and 100% zoom computed the following values. Module heights use the canonical Figma ratio; subpixel values remain fractional until painting.

| Viewport | Scale | Computed background-size | Expected module | Overflow |
|---:|---:|---:|---:|---|
| 360 | 0.25 | 360px | 360×651 | no |
| 390 | 0.2708333 | 390px | 390×705.25 | no |
| 480 | 0.3333333 | 480px | 480×868 | no |
| 600 | 0.4166667 | 600px | 600×1085 | no |
| 768 | 0.5333333 | 768px | 768×1388.8 | no |
| 900 | 0.625 | 900px | 900×1627.5 | no |
| 1024 | 0.7111111 | 1024px | 1024×1851.7333 | no |
| 1280 | 0.8888889 | 1280px | 1280×2314.6667 | no |
| 1440 | 1 | 1440px | 1440×2604 | no |
| 1600 | 1.1111111 | 1600px | 1600×2893.3333 | no |
| 1920 | 1.3333333 | 1920px | 1920×3472 | no |

Edge probes 767→768, 1023→1024, and 1439→1440 each increase the module width by exactly 1 CSS pixel and height by 1.8083333 CSS pixels. There is no IMG-02 media query or geometry step. The existing responsive harness swept every integer width from 360 through 1440 in EN and PT-BR; neither locale produced a horizontal-overflow width. Unclamped 1600 and 1920 probes prove growth above 1440.

## Ownership and content invariants

Traceability is deterministic: Figma `199:1358` → canonical repository asset → `home.html` `.homepage__technology-background[data-trace-id="IMG-02"]` → `home.css` `.homepage__technology-background` → computed browser evidence.

The owner remains `position:absolute`, `inset:0`, `z-index:0`, `pointer-events:none`, and `aria-hidden="true"`. It therefore adds no document box to normal flow, does not intercept input, and does not alter accessibility semantics. Pre/post browser rectangles were compared for Header, Hero, Engineering, Selected Engineering Work, Process, Evidence/Contact, Footer, and Jujuju AI at all shared evidence widths in both locales: `contentShiftCount = 0`.

## Files and evidence

Affected implementation/test files:

- `frontend/static/css/home.css`
- `tests/integration/test_home_block14.py`
- `scripts/validate-img02-background.py`

Traceability/report files:

- `docs/validation/SDD-RWD-001-visual-traceability-matrix.md`
- this report

Machine-readable evidence and screenshots:

- `artifacts/responsive-visual/img02-continuous/img02-geometry.json`
- `artifacts/responsive-visual/img02-continuous/interpolation-sweep.json`
- `artifacts/responsive-visual/img02-continuous/content-shift-comparison.json`
- `artifacts/responsive-visual/img02-continuous/before/` and `after/`
- full-page EN/PT-BR screenshots at 360, 768, 1024, and 1440; EN screenshots at 1600 and 1920

## Regression results and review gate

Focused Homepage/background/responsive tests: 43 passed. Ruff, mypy application (87 files), mypy tests (44 files), Django system check, repository structure, canonical documentation, naming, secret scan, and `git diff --check` passed. Full pytest completed collection/execution with 271 passed and 30 setup errors; every error was isolated to the unavailable local PostgreSQL connection. No SQLite fallback or database architecture change was introduced.

Automated geometry verifies implementation behavior, not artistic perception. A human must review tile boundaries, the complete repeated artwork, and visual continuity in the supplied full-page screenshots before final visual acceptance.
