# Visual Assets — Release 1

Canonical repository location for the approved visual assets of the Site
Portfolio. Serving is handled by Django `staticfiles` (`STATICFILES_DIRS`
points at `frontend/static`).

Governing documents: SPEC-001 (Branding; SPEC-001-REQ-003), EGS-001,
BASELINE-001, ADR-002.

## Provenance

Two authoritative raster sources were approved for Release 1 ingestion. The
external originals under `/home/luis/portfolio-luis/img` were copied into the
repository; they were never moved or deleted.

| Repository master | Source | Dimensions | SHA-256 |
| --- | --- | --- | --- |
| `brand/lf-information-system.png` | `lf-information-system.png` | 1254x1254 | `65610007eafd5d27d53b81819a31a44ea2a07322260dd4a64dfe589a161181fc` |
| `profile/luis-franca.png` | `luis-franca.png` | 896x1195 | `b80db13f3044c862321e4b081e67a20ca7b8af3f65f70b5470cfd9eacd25bacb` |
| `projects/enterprise-platform.png` | `projetos/enterprise-platform.png` | 1480x16384 | `bc67f8aa848d01521dc99602f9ee5d4e18a536eb649f2729753bdbffb559a10d` |
| `projects/intelligent-currency-platform.png` | `projetos/intelligent-currency-platform.png` | 1480x16384 | `05a437030881ccb68bf748f892574847db1f7aaa55640f1b5817e7b8112f1fb3` |
| `projects/sistema_cotacao_moedas.png` | `projetos/sistema_cotacao_moedas.png` | 1480x7636 | `e6223dbb6e288a75e8337945f003027c7e6e5ac319eafc8e80506c55b531c7da` |

The repository masters are pixel-identical copies of the approved sources and
are the authoritative raster masters. They are never modified by generation
tooling.

## Approved visual identity decisions

- The original PNG logo is the authoritative raster master.
- SVG vectorization is **not** required for Release 1; no artificial or
  vector recreation of the logo is permitted.
- Generated derivatives must originate from the approved raster masters.
- The professional photograph must not be distorted, recolored or edited
  beyond deterministic downscaling (no generative edits).
- The logo's black background is part of the approved visual identity and is
  preserved in the logo and in the favicon candidates.

## Structure

| Directory | Contents |
| --- | --- |
| `brand/` | Logo master (PNG) and WebP delivery derivatives. |
| `profile/` | Photograph master (PNG) and WebP delivery derivatives. |
| `projects/` | Featured project screenshot masters (PNG) and WebP delivery derivatives. |
| `favicon/` | Favicon candidates (see Favicon status below). |

Naming is lowercase and deterministic: `<name>-<width>.webp` for delivery
derivatives. Masters carry no size suffix and are the largest authoritative
raster available; derivatives are never upscaled beyond master resolution.

## Regeneration

Derivatives are generated programmatically from the repository masters:

```sh
bash scripts/generate-assets.sh   # or: make generate-assets
```

Requires ImageMagick (`magick`/`convert`) with PNG and WebP delegates. The
generation is deterministic for fixed parameters and does not require any
project dependency. Masters are validated (expected dimensions) and left
untouched.

## Responsive delivery

Delivery strategy: WebP derivatives selected with `<picture>`/`srcset`,
PNG master as the fallback, explicit `width`/`height` attributes, and CSS
`max-width: 100%; height: auto`. No single hardcoded display size; no layout
shift.

Reusable partials (ready for page integration):

- `frontend/templates/includes/brand-logo.html`
- `frontend/templates/includes/profile-photo.html`
- `frontend/static/css/images.css`

Reference markup (brand logo):

```html
{% load static %}
<picture>
    <source
        type="image/webp"
        srcset="{% static 'images/brand/lf-information-system-300.webp' %} 300w,
                {% static 'images/brand/lf-information-system-600.webp' %} 600w,
                {% static 'images/brand/lf-information-system-1254.webp' %} 1254w"
        sizes="(min-width: 992px) 220px, (min-width: 640px) 30vw, 45vw">
    <img
        class="brand-logo"
        src="{% static 'images/brand/lf-information-system.png' %}"
        alt="Luis Franca — Site Portfolio logo"
        width="1254"
        height="1254">
</picture>
```

The `sizes` values are conservative placeholders and should be tuned when the
pages that include these partials are implemented under the approved
specification sequence.

## Release 1.1 Homepage authorities

The human-approved Homepage portrait master is
`profile/luis-franca-transparent-02.png` (1385x1136, RGBA). Deterministic
transparent WebP delivery derivatives are generated at 480, 768, and 1024 px
wide; the master PNG is the fallback.

The human-approved Homepage background master is
`background/homepage-background-desktop-02.png` (933x1686, RGB). It is
delivered directly with Homepage-scoped CSS crop/focal adjustment; no
breakpoint-specific background derivatives are generated in Block 4.

The similarly named variants without `-02` are not approved substitutes and
remain in the repository only as protected obsolete candidates.

Project screenshots are full-page captures (taller than their display
container). They are delivered through the same WebP `<picture>` pipeline and
are scrolled within a fixed-height container on user interaction
(SPEC-003-REQ-006); see `frontend/static/css/portfolio.css`.

## Favicon

**FAVICON STATUS: MANUAL VISUAL VALIDATION REQUIRED.**

The favicon must use only the LF brand mark, without the "INFORMATION
SYSTEM" text. The LF mark was extracted deterministically from the approved
logo master — no redraw, recolor or vectorization:

- Mark bounds inside the 1254x1254 master: x=217..1115, y=286..802 (899x517).
- Deterministic crop of the exact mark region (pixel-identical to the master),
  padded with the logo's black background onto a centered 1019x1019 canvas.
  The "INFORMATION SYSTEM" and tagline text bands (y>=829) are excluded.

Candidates generated:

- `favicon/lf-mark-master.png` (1019x1019 intermediate LF master)
- `favicon/favicon-16x16.png`
- `favicon/favicon-32x32.png`
- `favicon/apple-touch-icon.png` (180x180)
- `favicon/favicon.ico` (16, 32, 48)

Human visual validation is required before these candidates are adopted as
the site favicon. They are not presented as a completed feature.
