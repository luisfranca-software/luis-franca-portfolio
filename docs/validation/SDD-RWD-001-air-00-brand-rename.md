# SDD-RWD-001 — AIR-00 Brand Rename to Juju IA

## 1. Preflight

Branch `main`, HEAD `10ce72...`; cumulative work was preserved. This micro-remediation changed only the AIR-00 brand authority, its focused tests, current findings annotation, and proportionate evidence/reporting.

## 2. Existing AIR-00 authority

The production authority was the single literal `Jujuju AI` inside the one Homepage `.home-ai-rag[data-trace-id="AIR-00"]`. Earlier reports and evidence were classified as historical and not rewritten.

## 3. Figma Node/Traceability identity

File `7XIYTbKZrLk77biI0UhRIb`; AIR-00 instances remain `316:751`, `297:509`, `270:1493`, and `154:1374` in the 360, 768, 1024, and Desktop frames. All remain 210×48 at their prior X/Y coordinates.

## 4. Figma rename

After loading the instances' current Inter fonts, only `Label#115:3` changed from `Jujuju AI` to `Juju IA`. Supporting text remains empty. Read-back and screenshot validation confirmed unchanged IDs and geometry.

## 5. Application content authority

`frontend/templates/home/home.html` is the sole current production name authority. The name remains a locale-invariant literal, avoiding duplicate translation messages.

## 6. Application rename

The authoritative literal changed from `Jujuju AI` to `Juju IA`. No DOM, CSS, positioning, Footer clearance, JavaScript, breakpoint, or runtime behavior changed.

## 7. EN/PT-BR result

All 88 Chromium observations across EN/PT-BR render exactly `Juju IA`. Neither `Jujuju AI` nor `Juju AI` is rendered by current AIR-00.

## 8. Position-regression protection

Before/after comparison at both locales and four reference widths reports identical X/Y/W/H and right/bottom edges. Fixed positioning, 210×48 size, z-index, safe-area offsets, and containing-block exclusion are unchanged.

## 9. 360 result

Juju IA fits on one line without clipping or overflow. Browser rectangle remains x=115, y=832, w=210, h=48; CSS offsets remain right=20px and bottom=20px.

## 10. 768 result

Juju IA fits without clipping or overflow. Browser rectangle remains x=511, y=820, w=210, h=48; CSS offsets remain right=32px and bottom=32px.

## 11. 1024 result

Juju IA fits without clipping or overflow. Browser rectangle remains x=751, y=804, w=210, h=48; CSS offsets remain right=48px and bottom=48px.

## 12. 1440 result

Juju IA fits without clipping or overflow. Browser rectangle remains x=1167, y=804, w=210, h=48; CSS offsets remain right=48px and bottom=48px.

## 13. Interpolation result

390, 480, 640, 820, 900, 1100, and 1280 retain fixed right-side geometry, one-line content, no text/page overflow, stable scroll geometry, and the previously approved collision probes.

## 14. Accessibility/noninteractive contract

AIR-00 remains `aria-hidden=true`, pointer-events none, outside tab order, and a DIV with no role, link, button, or JavaScript behavior.

## 15. Protected-baseline audit

No CSS changed during this rename. Header, Hero/IMG-02/IDE/Explorer/portrait, downstream Homepage sections, Footer, all breakpoints, responsive images, reduced motion, and unrelated routes are untouched. The existing full-width sweep remains authoritative for all 13 FIT decisions.

## 16. Files changed

Rename-owned application changes are `frontend/templates/home/home.html` and `tests/integration/test_home_ai_rag_reserved.py`; additionally this current report, findings annotation, and `artifacts/responsive-visual/air-00-brand-rename/` were added. Historical AIR evidence/report content was preserved.

## 17. Tests

Focused AIR/Footer/visual tests passed 18/18. Broader Homepage, responsive, Hero, Footer, route, accessibility, and evidence regression passed 182/182.

## 18. Full pytest

271 tests passed. Thirty database-backed cases could not initialize because the established PostgreSQL runtime is unavailable; no SQLite fallback or database change was introduced.

## 19. Ruff/mypy/Django checks

Ruff passed. mypy passed for 87 application files and 44 test files. Django system check passed with zero issues.

## 20. Repository gates

Structure, canonical documentation, naming, tracked-secret checks, and `git diff --check` pass. No Git staging, reset, clean, restore, commit, or push occurred.

## 21. Acceptance matrix AIR-BRAND-AC-001–036

PASS: 001–029 and 031–036. CONDITIONALLY SATISFIED: 030—the full suite ran with 271 passes; only 30 PostgreSQL-unavailable setup errors remain. Current Figma/application identity is deterministic and geometry is unchanged.

## 22. Remaining risks

Human visual review remains required. PostgreSQL-backed tests should be rerun when the established service is available. No rename-specific geometry, collision, clipping, or traceability risk remains in automated evidence.

## 23. Final gate

AIR-00-BRAND-RENAME — PASS — READY FOR HUMAN VISUAL REVIEW
