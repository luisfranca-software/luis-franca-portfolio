# SDD-RWD-001 — Hero Technology Composition Refactor

## 1. Preflight

Gate A passed: current live Figma deterministically exposed IMG-02 and the complete composition at 360, 768, 1024, and 1440. Work remained strictly scoped to the Hero technology composition and its evidence/tests.

## 2. Authorities read

EGS-001, technical specification, architecture, SDD-RWD-001, current geometry, geometry remediation, integrated remediation, findings, traceability, portrait isolation, templates, CSS, tests, and live Figma were inspected before mutation.

## 3. Repository state

Branch `main`, preflight HEAD `10ce72...`, cumulative dirty worktree preserved. Nothing was staged, reset, cleaned, restored, committed, or pushed.

## 4. Live Figma authority

File `7XIYTbKZrLk77biI0UhRIb`; HERO-07 nodes `316:626`, `297:384`, `270:1368`, `153:1199`. Live design context and read-only Plugin API inspection were used; Figma was not mutated.

## 5. Terminology confirmation for IMG-02

IMG-02 means only the approved Homepage Technology Background asset/layer. It is distinct from generic page and section background colors.

## 6. Current Hero technology diagnosis

The prior DOM had a generic depth layer, combined gutter/code presentation, Explorer labels without separate structure ownership, and IMG-02 on `.homepage` with a later stretched `100%`-height override.

## 7. Existing coupling identified

Late media rules independently rewrote the same child properties, portrait dimensions were capped by inherited global image rules, Explorer used right offsets while other states used left offsets, and the atmospheric asset doubled as generic Homepage styling.

## 8. Figma geometry — 360

Composition 320×500; gutter `[0,21,16,336]`; IDE `[13,21,186,448]`; Explorer `[172,21,148,310]`; portrait `[0,220,320,262.58]`.

## 9. Figma geometry — 768

Composition 704×600; gutter `[32,0,19,336]`; IDE `[57,0,295,384]`; Explorer `[410,0,294,384]`; portrait `[72,97,561,522]`.

## 10. Figma geometry — 1024

Composition 480×544; gutter `[0,36,22,336]`; IDE `[28,36,332,336]`; Explorer `[306,36,174,324]`; portrait `[-16,122,531,427]`.

## 11. Figma geometry — 1440

Composition 608×384; gutter `[0,12,22,336]`; IDE `[28,12,332,336]`; Explorer `[360,20,248,324]`; portrait `[-24,75.87,600,492.13]`.

## 12. IMG-02 Figma authority by viewport

Nodes `316:616`, `297:374`, `270:1358`, `199:1358`; frames 360×6960, 768×5416, 1024×4428, 1440×2604. All use the same 933×1686 image hash, FILL, centered identity transform, opacity 1, stack 0.

## 13. Rebuild architecture

One relative, isolated `.home-hero__visual` owns atmosphere, gutter, IDE, Explorer, disabled rim trace, and portrait. Each geometry-bearing responsibility has its own variables and stacking level.

## 14. DOM changes

Added one decorative IMG-02 layer, explicit atmosphere and gutter siblings, Explorer structure/label children, and authoritative code/tree rows. No duplicate breakpoint DOM or semantic copy change was introduced.

## 15. CSS changes

Removed competing technology declarations and the stretched Homepage background. Anchor variables define measured states; local absolute positioning expresses intentional overlap without margin compensation or JavaScript.

## 16. Professional Portrait implementation

IMG-00 retains its canonical responsive `<picture>` and accessible alt text. Local geometry is independent, and `aspect-ratio: 1385 / 1136` neutralizes an inherited incorrect ratio without changing the asset.

## 17. IDE implementation

HERO-07A owns code bounds, 14px line-height, Roboto Mono typography, `.84` opacity, clipping, and z-index 2. HERO-07B independently owns the 24-line gutter at z-index 1.

## 18. Explorer implementation

HERO-08 owns panel bounds, 12px radius, cyan `.28` stroke, clipping, and z-index 3. HERO-08A labels and HERO-08B structure are independently positioned children.

## 19. Layering model

Live-Figma order is atmosphere (0), gutter (1), IDE (2), Explorer (3), disabled rim trace, portrait (4). HERO-09A remains `display:none`.

## 20. Homepage Technology Background implementation

IMG-02 is a dedicated absolute decorative child of `.homepage`, behind normal Homepage content. The generic `#020b1f` base remains separate and protected.

## 21. IMG-02 responsive art-direction strategy

The live Figma FILL evidence maps to `center center / cover no-repeat`. The layer follows content height without fixed screenshot heights; computed rendered dimensions and centered crop are recorded per viewport.

## 22. 360 browser result

EN/PT-BR render without page overflow or Hero text breakage. Chromium scrollbar content width yields a 305px visual box; local anchor positions otherwise reproduce the compact state and canonical portrait ratio.

## 23. 768 browser result

The 689px content box reproduces the tablet state with measured IDE 295×384, gutter 19×336, Explorer 294×384, and portrait 561×460.14 at its canonical ratio.

## 24. 1024 browser result

The visual is 480×544; IDE/gutter/Explorer exactly match Figma bounds. The responsive global max-width caps the portrait to 480×393.70 while retaining its required position and undistorted ratio.

## 25. 1440 browser result

The visual is 600.97×384 after scrollbar allocation; IDE and gutter match, Explorer remains right-anchored at 248×324, and portrait is 600×492.13, matching Figma size and ratio.

## 26. Absolute geometry comparison

The exact Figma/browser rectangles and deltas are persisted in `live-figma-authority.json` and `hero-tech-refactor-visual-validation.json`. Differences are limited to browser scrollbar allocation and the protected global image max-width at 360/1024; no distortion occurs.

## 27. Relational geometry comparison

Evidence records gutter→IDE, IDE→Explorer, portrait→IDE, and portrait→Explorer overlap areas at every tested width. Positioning is composition-local; Engineering remains in normal flow below the Hero.

## 28. IMG-02 perceptual comparison

Automated and screenshot review confirms the same cyan/blue arcs, gold field, particles, and depth remain visible around portrait/code/explorer. Final perceptual acceptance is explicitly reserved for a human.

## 29. Hero-to-Engineering spacing

IMG-02 is absolute and cannot establish flow height. Hero state heights remain 500/600/544/384 anchors; Engineering was not artificially moved.

## 30. Interpolation

390, 480, 640, 820, 900, 1100, and 1280 have zero page overflow and no Hero broken words in both locales. Wide Explorer right anchoring prevents intermediate overflow.

## 31. Full-width sweep

The 360–1440 integer sweep completed for EN/PT-BR with zero page-overflow widths and all 13 transitions `FIT-VALIDATED`; no threshold declaration changed.

## 32. EN/PT-BR

Both locales were captured at all reference and interpolation widths. Hero content remains localized and its technology layers remain decorative.

## 33. Accessibility

One H1, heading order, keyboard/focus contracts, portrait alt text, and `aria-hidden` decoration remain intact. Focused regression passed.

## 34. Responsive images

The canonical PNG and 480/768/1024 WebP sources, intrinsic attributes, fetch priority, and `sizes` contract remain present.

## 35. Reduced motion

No motion or animation was introduced; existing reduced-motion behavior is unchanged.

## 36. Protected Homepage regression

Header, Hero copy/actions, Engineering, Projects, Process, Evidence, Contact, Footer, and AIR were not redesigned. Changes outside technology selectors are limited to IMG-02 ownership.

## 37. Non-Homepage regression

`home.css` remains Homepage-only; `/about/` does not load it or render `.homepage`. Focused route contract passed.

## 38. Tests

Hero structural tests: 22 passed. Broader Homepage/responsive/accessibility regression: 181 passed. Architecture tests now assert independent traces and correct component scope.

## 39. Full pytest

Result after the refactor audit: 268 passed, 2 stale assertions found and corrected, 30 PostgreSQL setup errors. The errors are environmental connection failures; no SQLite fallback was used. Focused rerun after corrections passed 181/181.

## 40. Ruff

PASS: `uv run ruff check .`.

## 41. mypy

PASS: application 87 source files; tests 44 source files.

## 42. Django check

PASS: zero issues, zero silenced.

## 43. Repository gates

Structure, documentation, naming, and tracked-secret gates all pass.

## 44. Files changed

Refactor-owned files: `frontend/templates/home/home.html`, `frontend/static/css/home.css`, capture script, four focused test modules, findings register, this report, and the dedicated evidence namespace. Cumulative unrelated changes were preserved.

## 45. Evidence generated

`artifacts/responsive-visual/hero-tech-refactor/` contains live authority JSON, two-locale geometry/computed-style JSON, eight full-page shots, eight Hero shots, full sweep JSON, and FIT screenshots.

## 46. Acceptance matrix HTR-AC-001–051

PASS: 001–042 and 044–051. ENVIRONMENT-BLOCKED: 043 because local PostgreSQL is unavailable; all non-DB and focused tests pass. AC-027–030 remain technically supported but require human perceptual confirmation before human acceptance.

## 47. Cumulative diff audit

No duplicate composition, duplicate IMG-02, competing obsolete IMG-02 rule, dead experiment, generic background replacement, restored rim, margin compensation, fixed page height, global overflow mask, JS positioning, screenshot hack, new effect, or unrelated Homepage redesign was found.

## 48. Remaining risks

Human perception of IMG-02 focal crop and atmospheric strength remains the explicit review risk. Browser scrollbar allocation differs from Figma frame math. Full database-backed pytest awaits PostgreSQL availability.

## 49. Human visual-review checklist

Compare EN/PT-BR full and Hero shots at 360/768/1024/1440; inspect arc/particle/gold visibility, code/tree legibility, intentional portrait overlap, absence of rim rectangle, and Hero-to-Engineering rhythm.

## 50. Final gate

HERO-TECH-REFACTOR — PASS — READY FOR HUMAN VISUAL REVIEW
