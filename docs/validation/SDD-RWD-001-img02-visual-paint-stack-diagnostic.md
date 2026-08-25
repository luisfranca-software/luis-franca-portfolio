# SDD-RWD-001 — IMG-02 Visual Paint-Stack Diagnostic

Date: 2026-08-24<br>
Diagnostic state: live artwork visible; reported hidden state not reproduced

## Previous false-positive risk and reported symptom

The earlier runtime gate proved computed CSS and network loading but did not, by itself, prove visible pixels. Human inspection subsequently reported that the canonical cyan/blue/gold IMG-02 composition was absent. This diagnostic therefore treats fresh full-page Chromium screenshots and controlled paint isolation as authority.

No production CSS, template, asset, or Figma mutation was made during this diagnostic. The current exact-origin `http://localhost:8000/` state does not reproduce the reported symptom: new screenshots visibly contain the canonical cyan/blue curves, gold/yellow curves, and both particle fields at 360, 768, 1024, 1440, and 1600.

## Asset identity and visual authority

Figma authority remains file `7XIYTbKZrLk77biI0UhRIb`, node `199:1358`, canonical presentation 1440×2604. The live URL is `http://localhost:8000/static/images/background/homepage-background-desktop-02.png`; it returns HTTP 200 and is byte-identical to `frontend/static/images/background/homepage-background-desktop-02.png`.

- intrinsic raster: 933×1686, sRGB;
- SHA-1: `b06fb16c56279829bc6adb74058b8d60081e5854`;
- SHA-256: `09eb5be0c589996137e5aea87d9eb06609559c5e9f1a0e9cf0de6a4033b8726d`.

Direct raster inspection visibly confirms cyan/blue luminous curves, gold/yellow curves, cyan/blue and gold/yellow particle fields, and a dark navy base.

## Paint owner and stacking chain

The complete machine-readable inventory is `artifacts/responsive-visual/img02-paint-stack/isolation/paint-stack.json`. It records element and `::before`/`::after` styles for `html`, `body`, `main`, `.homepage`, IMG-02, Hero, Engineering, Projects, Process, Evidence/Contact, and Footer at all four reference widths.

The relevant chain is:

1. `.homepage` establishes `position:relative` and `isolation:isolate`, with the navy color as the stacking-context canvas.
2. `.homepage__technology-background` is an absolute full-Homepage child at `z-index:0`, opacity 1, normal blend, no filter or transform, and `pointer-events:none`.
3. Homepage content children are positioned at `z-index:1` but their section roots and pseudo-elements are transparent; cards retain legitimate translucent dark surfaces.
4. Header and Footer paint opaque local surfaces outside the Homepage content layer. They do not cover the Homepage root.

At every reference width IMG-02 is visible, uses the canonical URL, and retains `100vw auto`, `repeat-y`, and centered top positioning. No full-page pseudo-element, gradient, mask, opacity layer, competing image, or later selector covers it.

## Runtime-only isolation proof

At 1440, Chromium captured these states after waiting for two animation frames after each toggle:

- normal restored;
- section-root backgrounds disabled;
- Homepage/Hero pseudo-elements disabled;
- all suspected coverings disabled;
- IMG-02 disabled;
- IMG-02 restored.

The restored, section-disabled, pseudo-disabled, and all-coverings-disabled images have the same SHA-256: `3ae93355cf2c259461ffe6ec7b3c8bf641394527dc2a74c9bc3ac043b4b2ae1f`. Therefore none of those suspected layers hides or suppresses the artwork.

Disabling IMG-02 produces SHA-256 `2cb0c8a18d7f2c605f98fa5191ec36c609a4685a87d8dfc26d2a06e5ec906172` and changes 3,164,880 pixels (78.3821% of the screenshot). This directly proves IMG-02 is painted and materially visible. Restoring it restores the cyan/blue/gold composition. There is no failure-causing selector in the tested live paint stack.

## Responsive screenshots and invariants

Pre-diagnostic EN/PT-BR full-page captures are under `artifacts/responsive-visual/img02-paint-stack/before/`. Exact `localhost` EN/PT-BR captures at 360, 768, 1024, and 1440 are under `after/`; the 1600 EN capture and checkpoint geometry are under `after-extra/`. All visibly show canonical artwork.

Before/after rectangles for Header, Hero, Engineering, Projects, Process, Evidence/Contact, Footer, and Juju IA are identical: `contentShiftCount = 0`. Both sets have `horizontalOverflowCount = 0`. Evidence is in `content-invariants.json`.

## Root-cause and remediation decision

The reported hidden-artwork state cannot be reproduced in fresh Chromium against either `127.0.0.1:8000` or the exact `localhost:8000` origin. Both origins serve identical CSS and asset bytes. Browser isolation proves there is currently no occluding layer and no stacking defect to correct. A cache-disabled temporary profile was used, so its captures do not depend on an existing user-profile cache.

Because no runtime paint defect exists in the tested application, changing production stacking or backgrounds would be speculative and would violate the requirement to apply only the smallest proven correction. No persistent remediation was applied. If a specific human browser still differs, that browser/profile/session must be captured directly (exact URL, DevTools screenshot, and loaded-resource state) to diagnose the external discrepancy.

## Tests

The diagnostic scripts are Ruff-clean. Focused Homepage/background tests, normal static analysis, Django checks, repository checks, and diff checks are recorded with the task handoff. PostgreSQL-dependent full-suite setup remains environment-blocked and is not represented as passing.
