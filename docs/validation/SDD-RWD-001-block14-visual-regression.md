# SDD-RWD-001 — Block 14 Visual Regression and Interpolation

Status: COMPLETE / PENDING HUMAN REVIEW

## Authority and environment

FIGMA-04/05 and the persisted reference exports under `docs/design/references/`
remain visual authority. Blocks 1–13 and the 13 FIT-VALIDATED decisions remain
the protected responsive baseline. Validation used Chromium 151.0.7922.108
(snap), headless Linux x86_64, DPR 1, zoom 100%, and a 900 CSS-pixel viewport
height against the local Django/PostgreSQL runtime.

## Method and evidence

Complete Homepage renderings were inspected in EN and PT-BR at 360, 768, 1024,
and 1440 CSS px. Interpolation was accepted in both locales at 390, 480, 640,
820, 900, 1100, and 1280. Machine geometry, mode, overflow, destructive-break,
component-collision, and Footer-target collision evidence is stored at:

- `artifacts/responsive-visual/block14/block14-visual-validation.json`
- `artifacts/responsive-visual/block14/block14-full-width-sweep.json`
- `artifacts/responsive-visual/block14/homepage-{locale}-{width}.png`

Block 12/13 captures provide immutable before evidence for HERO-BG-001 and the
AI/RAG/Footer finding. The eight Block 14 full-page captures provide final after
evidence.

## HERO-BG-001 resolution

Diagnosis: the correct 933×1686 approved asset was rendered behind the entire
Homepage, but a 933px minimum display width removed most side structure on
narrow viewports and an opaque 50rem gradient endpoint suppressed the arc and
particle field before Engineering.

Correction: the approved `homepage-background-desktop-02.png` remains unchanged.
Its minimum rendered width is now 720px, and a gentler overlay remains mostly
transparent through 42rem before reaching the page color at 78rem. Center-top
anchoring, aspect ratio, natural page height, and no-repeat behavior remain.
Final captures materially restore the luminous blue arc and particle continuity
through Hero into Engineering without a seam, readability loss, or overflow.

## AI/RAG/Footer resolution

Diagnosis: at maximum document scroll, the fixed bottom-right visual occupied
the same viewport band as natural-flow Footer actions. Correction adds 3.5rem
of bounded extra bottom clearance only to `.site-footer--homepage`. There is no
global page padding, new FIT, JavaScript behavior, hidden link, or Footer flow
change. Final runtime probes show Projects, Contact, LinkedIn, GitHub, and the
Contact CTA unobstructed at every reference/interpolation width in both locales.
The visual remains visible, fixed, bottom-right, safe-area aware, pointer-neutral,
and absent from the accessibility tree.

## Final observations

- The official logo now appears in the Homepage Header as required by the
  approved reference; non-Homepage Header branding remains unchanged.
- All required component modes match the finalized FIT inventory.
- Both 360–1440 integer sweeps report zero page-overflow widths, healthy FIT
  probes, and no recorded AI/RAG collision.
- Reference and interpolation evidence reports zero destructive word breaks and
  zero Footer-target collisions.
- Accessibility, i18n, responsive-image, reduced-motion, route-isolation, and
  complete regression suites pass.

## State boundary

Technical responsive implementation, visual regression, and interpolation
validation are complete. Block 14 and final responsive implementation remain
pending human review; no human-accepted status is asserted here.
