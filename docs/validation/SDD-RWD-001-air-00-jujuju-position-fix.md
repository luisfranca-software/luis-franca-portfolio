# SDD-RWD-001 — AIR-00 Jujuju AI Position Fix

## 1. Preflight

Branch `main`, HEAD `10ce72...`; the cumulative dirty worktree was recorded and preserved. Scope was limited to AIR-00, its direct positioning conflict, focused tests/evidence, and the already-established Footer-safe clearance.

## 2. AIR-00 current implementation

AIR-00 is one direct child of `.homepage`, rendered before the closing Homepage wrapper and before the shared Footer. `.home-ai-rag` declares fixed positioning, z-index 20, right/bottom safe-area-aware offsets, 210×48 final size, no transform, and pointer-events none.

## 3. Position-regression root cause

The Hero technology refactor introduced `.homepage > :not(.homepage__technology-background) { position:relative; z-index:1; }`. Its higher specificity overrode AIR-00's single-class `position:fixed`, returning AIR to normal flow near the Footer. No ancestor transform, filter, perspective, or containment caused the defect.

## 4. Figma authority

Live file `7XIYTbKZrLk77biI0UhRIb`; instances `316:751`, `297:509`, `270:1493`, and `154:1374`, each 210×48. Existing geometry, opacity, component identity, styling, and native IDs were preserved.

## 5. Figma text update

All four existing instance component properties were updated to Label=`Jujuju AI`, Supporting text=``, after loading their current Inter fonts. Read-back and screenshot validation confirmed the change; no unrelated Figma node was mutated.

## 6. Content change to Jujuju AI

The Homepage template now renders exactly one invariant `Jujuju AI` label. `Ask AI / RAG`, `Explore engineering context`, and their PT-BR translations are no longer rendered by AIR-00.

## 7. Positioning correction

The direct-child normal-flow selector now explicitly excludes `.home-ai-rag`, allowing AIR's existing fixed declaration to win. No JavaScript positioning or new breakpoint was introduced.

## 8. CSS changes

One selector exclusion restores fixed ownership; obsolete supporting-text styling was removed. Footer bottom padding is 104px, matching the existing desktop safe-clearance intent and preventing real target intersections at maximum Footer scroll.

## 9. Template changes

Only AIR-00 child copy changed. `data-trace-id="AIR-00"`, `aria-hidden="true"`, the decorative icon element, and the noninteractive div structure remain intact.

## 10. Translation changes

No translation infrastructure or catalog was changed. The product name is deliberately literal and invariant; historical catalog strings remain for safe history preservation but are not rendered.

## 11. 360 result

EN/PT-BR: fixed 210×48 at x=115, y=832 in Chromium's 345px content viewport; CSS right/bottom=20px, measured physical edges 35/20 due the scrollbar. No overflow or required-target collision.

## 12. 768 result

EN/PT-BR: fixed 210×48 at x=511, y=820; CSS right/bottom=32px, stable at every scroll probe, without text overflow or required-target collision.

## 13. 1024 result

EN/PT-BR: fixed 210×48 at x=751, y=804; CSS right/bottom=48px. The 104px Footer clearance resolves the prior sub-pixel target intersection at maximum scroll.

## 14. 1440 result

EN/PT-BR: fixed 210×48 at x=1167, y=804; CSS right/bottom=48px. Component remains right-side, compact, and viewport-relative.

## 15. EN/PT-BR result

All 88 observations (11 widths × 4 scroll states × 2 locales) render exactly `Jujuju AI`; no locale-specific secondary copy or text overflow remains.

## 16. Scroll-position validation

At top, middle, Contact-centered, and maximum Footer scroll, each width has one unique AIR rectangle and one unique right/bottom edge pair. Scroll movement does not alter AIR geometry.

## 17. Contact/Footer collision validation

Contact CTA intersection is false at the Contact probe. Actual Footer navigation/social anchors are clear at maximum Footer scroll. LinkedIn/GitHub intersections are false at the top probe. All raw rectangles remain persisted for audit.

## 18. Interpolation smoke

390, 480, 640, 820, 900, 1100, and 1280 pass fixed/right/bottom/content/overflow/stability checks without a new breakpoint.

## 19. Accessibility

AIR remains a decorative DIV with `aria-hidden=true`, no role, no tabindex, zero links/buttons, and pointer-events none. No runtime behavior exists.

## 20. Protected-baseline regression

Header, Hero copy and technology composition, IMG-02, portrait, downstream sections, Footer structure, responsive images, reduced motion, and non-Homepage routes remain protected. Full-width evidence records all 13 existing FIT states as validated.

## 21. Files changed

Task-owned code changes are `frontend/templates/home/home.html`, `frontend/static/css/home.css`, `tests/integration/test_home_ai_rag_reserved.py`, the dedicated capture script, this report, findings closure, and `artifacts/responsive-visual/air-00-jujuju/`. Cumulative unrelated changes were preserved.

## 22. Tests

Focused AIR/Footer/Block 14 tests passed 18/18. Homepage, responsive, Hero, Footer, route, accessibility, and evidence regression passed 182/182.

## 23. Full pytest

271 tests passed; 30 database-backed cases could not set up because the established PostgreSQL service is unavailable. This is separately classified environmental failure; no SQLite fallback or database-architecture change was made.

## 24. Ruff

PASS: `uv run ruff check .`.

## 25. mypy

PASS: application 87 files; tests 44 files.

## 26. Django check

PASS: zero issues, zero silenced.

## 27. Repository gates

Structure, canonical documentation, naming, and tracked-secret gates pass. `git diff --check` passes. Nothing was staged, reset, cleaned, restored, committed, or pushed.

## 28. Evidence generated

`artifacts/responsive-visual/air-00-jujuju/` contains live-Figma authority, eight reference Footer screenshots, 88 scroll observations with computed styles/semantics/targets, interpolation evidence, full integer-width sweep, and FIT screenshots.

## 29. AIR-AC-001–040 matrix

PASS: AIR-AC-001–033 and AIR-AC-035–040. CONDITIONALLY SATISFIED: AIR-AC-034—full pytest was run, 271 passed, and only 30 PostgreSQL-unavailable setup errors remain. All 13 FIT states are `FIT-VALIDATED` with zero page-overflow widths.

## 30. Remaining risks

Human visual review remains required. PostgreSQL-backed tests must be rerun when the established native service is available. Raw evidence also records incidental geometric crossings at intermediate scroll moments; AIR is pointer-inert, while the mandated Contact and maximum-Footer target probes are clear.

## 31. Final gate

AIR-00-JUJUJU — PASS — READY FOR HUMAN VISUAL REVIEW
