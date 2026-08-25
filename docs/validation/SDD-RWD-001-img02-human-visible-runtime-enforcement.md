# SDD-RWD-001 — IMG-02 Human-Visible Runtime Enforcement

Date: 2026-08-24<br>
Gate: HOLD — mandatory production before/after pixel difference not achieved

## Forced runtime proof

At exactly 360 CSS pixels on `http://localhost:8000/`, a browser-only rule forced `.homepage__technology-background` to be an absolute, full-Homepage, non-interactive `z-index:0` layer using the canonical IMG-02 URL, `100vw auto`, `repeat-y`, and `top left`. No covering layer needed to be disabled. The full-page proof at `artifacts/responsive-visual/img02-paint-stack/isolation/360-forced-runtime-proof.png` visibly contains repeated cyan/blue curves, gold/yellow curves, and both particle fields.

The working browser owner was the existing `.homepage__technology-background` child of `.homepage`; it was not a pseudo-element. Its containing block, dimensions, opacity, stacking position, asset, scaling, and repetition already matched production. The sole textual difference was forced `top left` versus production `center top`.

## Attempted minimal correction and mandatory comparison

The only candidate correction supported by the forced-state comparison was changing `background-position:center top` to `left top`. This was temporarily persisted and captured in new exact-origin EN/PT-BR Chromium screenshots at 360, 768, 1024, and 1440, plus 1600 EN.

Browser computed position changed from `50% 0%` to `0% 0%`, but ImageMagick absolute-error comparison found zero changed pixels at every mandatory width:

| Width | Screenshot dimensions | Changed pixels | Changed percentage |
|---:|---:|---:|---:|
| 360 | 360×6761 | 0 | 0% |
| 768 | 768×5626 | 0 | 0% |
| 1024 | 1024×4489 | 0 | 0% |
| 1440 | 1440×2806 | 0 | 0% |

The ineffective edit was reverted. No speculative z-index, opacity, section-surface, geometry, or artwork change was retained. Diagnostic-only browser scripts were removed; validation artifacts remain.

## Asset, visual features, and invariants

The forced proof and all current screenshots visibly contain the canonical artwork, but the task explicitly requires the production BEFORE and AFTER captures to differ. That requirement is not satisfied.

Canonical repository asset: `frontend/static/images/background/homepage-background-desktop-02.png`, SHA-256 `09eb5be0c589996137e5aea87d9eb06609559c5e9f1a0e9cf0de6a4033b8726d`, mapped to Figma node `199:1358`.

The attempted state retained exact module widths and canonical heights at 360, 768, 1024, and 1440 and continued through 1600/1920. Content geometry comparison reported `contentShiftCount = 0`; `horizontalOverflowCount = 0`.

## Gate decision

The forced browser proof succeeds, but no evidence-backed production correction creates the mandatory human-visible before/after difference. Under the explicit final gate, the result must remain HOLD. A capture from the specific human browser/profile that exhibits the missing artwork is required to identify a state that differs from fresh Chromium localhost and justify a real production correction.
