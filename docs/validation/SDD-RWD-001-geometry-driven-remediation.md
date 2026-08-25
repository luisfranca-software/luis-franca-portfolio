# SDD-RWD-001 — Geometry-Driven Remediation

Date: 2026-08-23<br>
Branch/HEAD: `main` / `10ce72cc9c6cf1481a174c68c3cdfbc41c8f435f`<br>
Technical state: ready for human visual review; automated acceptance is not human acceptance.

## 1–11. Preflight, authority, traceability, and gates

The cumulative dirty worktree was recorded and preserved; nothing was staged, reset, cleaned, restored, committed, or pushed. Governance, SDD-RWD-001, Blocks 12–14, integrated-remediation evidence, findings, portrait isolation, templates, CSS, JS, content, translations, assets, tests, and capture infrastructure were inspected.

The current live Figma authority was queried again, not inferred from historical reports. Frame IDs remain 360 `316:615`, 768 `297:373`, 1024 `270:1357`, and 1440 `153:2`. Exact high-impact geometry is in `SDD-RWD-001-current-figma-geometry.md` and `figma-current-geometry.json`. Current semantic IDs are unambiguous across frames. Gate A: **PASS**.

The mapping `Traceability ID → native node → geometry → data-trace-id DOM → scoped selector → canonical asset → browser evidence` is persisted in `deterministic-traceability.json`. Gate B: **PASS**.

## 12–17. Hero diagnosis and remediation

Historical CSS retained the correct four responsive states but had stale internal geometry. Most notably, 360 IDE type was 10.5px although current Figma is 6px; portrait offsets/scales were percentage-derived; and the 1440 picture used a stale `bottom:-264px` placement.

- Portrait: canonical image preserved; explicit component-local size/offset states now reproduce current Figma relationships without distortion.
- Code: independent bounds/type corrected at 360/768/1024/1440; no dependence on portrait scaling.
- Explorer: independently sized and positioned; clipping retained.
- Titles: 14px greeting and 16/26 body rhythm corrected; 26/34 at 360 and 48/56 at larger references; no destructive intra-word wrapping in EN or PT-BR.
- Background: canonical image preserved, SHA-256 `09eb5be0…`; current continuous full-page authority remains scoped to `.homepage`.
- Portrait rim: rejected rectangle/shadow remains disabled with `display:none`; no invented effect was introduced.

## 18–24. Header and downstream validation

Header logo, PT/EN control, WhatsApp, compact menu, keyboard contracts, and breakpoint behavior were preserved. Engineering, Projects, Process, Evidence/Contact, Footer, and decorative AIR-00 were visually recaptured without unrelated redesign. AIR-00 remains pointer-inert and collision-free. Homepage-only rules did not propagate to `/about/`, `/skills/`, `/experience/`, `/portfolio/`, or `/contact/`.

## 25–33. Reference, locale, interpolation, sweep, and FIT results

Chromium `151.0.7922.108 snap`, DPR 1, zoom 100%, viewport height 900 was used. Full-page EN/PT-BR captures exist for 360, 768, 1024, and 1440. Interpolation measurements cover 390, 480, 640, 820, 900, 1100, and 1280.

The one-CSS-pixel sweep covered every width 360–1440 for both locales: 2,162 viewport measurements, zero page-overflow widths, zero recorded destructive word breaks, and zero Header/Hero/AIR/footer target collisions. All 13 FIT transitions remain healthy. EN project FIT was measured at 898 (historical allowed content-fit variation); PT-BR project FIT remained 896 and its large-card transition remained 1204. No breakpoint CSS threshold was changed.

## 34–38. Accessibility, i18n, images, motion, and route protection

Exactly one H1, landmarks, heading order, skip link, focus behavior, minimum targets, language actions, professional links, decorative semantics, AIR-00 tab exclusion, reduced-motion rules, and responsive-picture semantics remain covered. EN and PT-BR complete without missing translations or destructive word wrapping. Canonical responsive derivatives remain in use. Non-Homepage style isolation tests pass.

## 39–44. Test and quality gates

- Focused Homepage/Hero/Block14/responsive suite: **36 passed**.
- Full pytest: **269 passed, 30 setup errors, 1 warning**. All 30 errors are PostgreSQL connection failures; `pg_isready` reported no response and the sandbox could not authenticate `sudo systemctl start postgresql`. No SQLite fallback was used.
- Ruff: **PASS**.
- mypy application: **PASS**, 88 source files.
- mypy tests: **PASS**, 44 source files.
- Django system check: **PASS**, zero issues.
- Structure, documentation, naming, and secrets checks: **PASS**.
- `git diff --check`: **PASS**.

## 45–46. Evidence and findings closure

Evidence is under `artifacts/responsive-visual/geometry-remediation/`: live Figma geometry, deterministic mapping, browser geometry, eight reference screenshots, 26 FIT boundary screenshots, reference/interpolation validation JSON, and the full-width sweep.

- Portrait geometry: **RESOLVED**, subject to human review.
- Code geometry: **RESOLVED**, subject to human review.
- Explorer geometry: **RESOLVED**, subject to human review.
- Professional-title wrapping: **RESOLVED** for automated EN/PT-BR constraints.
- Homepage background fidelity: **ACCEPTED DEVIATION pending human judgment**; canonical asset and continuous scaling are correct, but screenshot perception remains a human gate.
- Header: **RESOLVED**.
- AI/RAG position: **RESOLVED**; no collisions.
- Footer interaction safety: **RESOLVED**.
- Full database regression: **BLOCKED** by unavailable local PostgreSQL, not by an application failure.

## 47–50. Diff audit, changed files, risk, and human checklist

The cumulative diff contains no new dependency, AI/RAG functionality, asset replacement, duplicate Hero/background, global overflow masking, fixed document height, page-level screenshot hack, or restored portrait-rim rectangle. Remediation-owned changes are `frontend/static/css/home.css`, `frontend/templates/includes/profile-photo.html`, `scripts/capture-responsive-visual.py`, `scripts/measure-responsive-fit.py`, `scripts/run-browser-evidence-server.py`, this report, current geometry documentation, and the dedicated evidence namespace.

Remaining risks: human-perceived background crop/section rhythm must be reviewed; browser layout widths exclude the vertical scrollbar while Figma frames do not model it; full DB-backed pytest must be rerun once PostgreSQL is available.

Human review checklist: compare EN/PT-BR at 360/768/1024/1440; inspect portrait/code/explorer occlusion; verify title line breaks; follow blue/gold background arcs through transitions; verify Header/menu and footer targets; confirm AIR-00 does not obscure actions.

## 51. Final gate

`GEOMETRY-DRIVEN-REMEDIATION — HOLD — HUMAN-VISIBLE DEVIATION REMAINS`

The implementation and browser evidence are ready for review, but the full engineering baseline is not technically green until PostgreSQL-backed tests run, and visual acceptance remains explicitly human-gated.
