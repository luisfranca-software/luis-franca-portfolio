# SDD-RWD-001 — Visual Traceability Matrix

Status: INTEGRATED REMEDIATION / GATES A+B PASS<br>
Date: 2026-08-23<br>
Figma authority: `Site Portfolio — Target Product` (`7XIYTbKZrLk77biI0UhRIb`)<br>
Repository authority: working tree inspected as found; no production file was changed by this audit.

Integrated remediation update: all materially applicable layers now use canonical bracketed IDs across 360/768/1024/1440. DOM correlations expose `data-trace-id`; machine-readable evidence is at `artifacts/responsive-visual/integrated-remediation/figma-traceability.json`. The exact Figma logo export is now IMG-01 authority. Final status for CRITICAL/HIGH mappings: **CONFORMANT**.

## Method and conventions

The four approved Figma frames were read through the Figma Plugin API and rendered through the Figma screenshot API. Localhost was rendered by Chromium at DPR 1, 100% zoom, a 900 CSS-pixel viewport height, and exactly 360, 768, 1024, and 1440 CSS pixels. A bracketed or pipe-delimited Traceability ID below is present in the native Figma layer name. `semantic carry-forward` means the same semantic ID is assigned by correlation even though that responsive layer has not yet been renamed in Figma.

Repository selectors were checked in the current templates and stylesheets. Asset dimensions and SHA-256 identities were checked from disk. Figma image hashes are included for correlation; they are Figma-native image identities and are not byte hashes of repository files.

## Reference frames

| Viewport | Page | Frame | Native node ID | Geometry |
|---:|---|---|---|---:|
| 360 | `04 — Responsive` (`9:5`) | `Homepage / 360 v1` | `316:615` | 360×6960 |
| 768 | `04 — Responsive` (`9:5`) | `Homepage / 768 v1` | `297:373` | 768×5416 |
| 1024 | `04 — Responsive` (`9:5`) | `Homepage / 1024 v1` | `270:1357` | 1024×4428 |
| 1440 | `02 — Homepage` (`9:3`) | `Homepage / Desktop v1` | `153:2` | 1440×2604 |

## Canonical mapping

Common implementation abbreviations: `home.html` = `frontend/templates/home/home.html`; `home.css` = `frontend/static/css/home.css`; `site.css` = `frontend/static/css/site.css`; `navigation.html` = `frontend/templates/includes/navigation.html`.

| Traceability ID | Viewport | Figma native node / layer | Geometry (x,y,w,h) | Repository file | DOM selector | CSS selector / responsive authority | Asset | Status | Finding IDs |
|---|---:|---|---|---|---|---|---|---|---|
| IMG-01 | 360 | `I316:617;169:1131` `IMG-01 \| LF Brand Logo` (RECTANGLE, image FIT) | 24,14,68,44 | `frontend/templates/includes/brand-logo.html` | `.site-nav__brand img.brand-logo` | `.site-nav__brand .brand-logo`; compact Header through 847px | browser selects `brand/lf-information-system-600.webp`; Figma hash `3083b91c…` | MAPPED / DIVERGENT | VIS-360-HDR-001 |
| HDR-02 | 360 | `I316:617;136:755` `HDR-02 \| Compact Controls` (FRAME) | 225,14,111,44 | `navigation.html` | `.site-nav__toggle`, `.language-selector` | `@media (max-width:847px)` and `.language-selector select` | — | MAPPED / DIVERGENT | VIS-360-HDR-002, VIS-360-HDR-003 |
| HDR-03 | 360 | `I316:617;136:756` `HDR-03 \| WhatsApp Action` (INSTANCE of `83:186`) | 0,0,44,44 within compact controls | `navigation.html` | `.site-nav__whatsapp` (inside hidden `.site-nav__menu`) | `.site-nav__menu {display:none}` through 847px | Figma component `Appearance=WhatsApp, State=Default` | MAPPED / MISSING AT REST | VIS-360-HDR-003 |
| HDR-04 | 360 | `I316:617;136:761` `HDR-04 \| Menu Toggle` (INSTANCE of `102:316`) | 67,0,44,44 within compact controls | `navigation.html`; `frontend/static/js/site.js` | `button.site-nav__toggle` | `@media (max-width:847px)`; JS toggles `.is-open` | inline CSS bars; Figma `Icon/Menu` (`99:308`) | MAPPED / PRESENT | — |
| IMG-02 | 360 | `316:616` `IMG-02 \| Homepage Background` (RECTANGLE, image FILL) | 0,0,360,6960 | `home.css` | `.homepage__technology-background` | `background-size:100vw auto`; center top; `repeat-y` | `background/homepage-background-desktop-02.png`; Figma hash/SHA-1 `b06fb16c…` | MAPPED / CONTINUOUS | SDD-RWD-001 IMG-02 finalization |
| HERO-01 | 360 | `316:620` `HERO-01 \| Greeting` (TEXT) | 0,0,320,20 | `home.html` | `.home-hero__greeting` | `.home-hero__greeting` | — | MAPPED / PRESENT | — |
| HERO-02 | 360 | `316:621` `HERO-02 \| Professional Titles` (TEXT, Inter Semi Bold 26/34) | 0,36,320,102 | `home.html` | `h1.home-hero__titles > .home-hero__title` | `clamp(2rem,7.7vw,4rem)`, 1.06 line-height | — | MAPPED / DIVERGENT | VIS-360-HERO-001 |
| HERO-03 | 360 | `316:622` `HERO-03 \| Positioning Statement` (TEXT, Inter 16/26) | 0,154,320,130 | `home.html`; `backend/apps/home/content.py` | `.home-hero__positioning` | `.home-hero__positioning` | — | MAPPED | — |
| HERO-04A | 360 | `316:624` `HERO-04A \| Primary CTA` (INSTANCE of `77:28`) | 0,0,145,48 | `home.html`; `site.css` | `a.home-hero__cta.button--primary` | `.button--primary` | — | MAPPED / WRONG FILL | VIS-360-HERO-002 |
| HERO-05A | 360 | `I316:625;133:613` `HERO-05A \| LinkedIn Action` | 0,0,44,44 | `home.html` | `a.home-hero__social[aria-label="LinkedIn"]` | `.home-hero__social` | text glyph `in` rather than component icon | MAPPED / DIVERGENT | VIS-360-HERO-003 |
| HERO-06 | 360 | `I316:625;133:626` `HERO-06 \| GitHub Action` | 52,0,44,44 | `home.html` | `a.home-hero__social[aria-label="GitHub"]` | `.home-hero__social` | inline GitHub SVG | MAPPED / PRESENT | — |
| HERO-07A | 360 | `316:633` `HERO-07A \| IDE Code` (TEXT, Roboto Mono 10.5/14, opacity .84) | 14,24,186,246 | `home.html` | `.home-hero__ide`, `.home-hero__code` | absolute, top 3%, width 76% | — | MAPPED / DIVERGENT | VIS-360-HERO-004 |
| HERO-08 | 360 | `316:634` `HERO-08 \| Repository Explorer` (FRAME) | 172,21,148,310 | `home.html` | `.home-hero__explorer` | absolute, top 9%, right 0, width ≤46% | — | MAPPED / DIVERGENT | VIS-360-HERO-004 |
| IMG-00 | 360 | `316:707` `IMG-00 \| Professional Portrait` (FRAME, image FIT) | 0,220,320,262.58 | `frontend/templates/includes/profile-photo.html` | `.home-hero__visual img.profile-photo` | picture absolute; width ≤92%; centered bottom | `profile/luis-franca-transparent-02-{480,768,1024}.webp`; Figma hash `0d13002a…` | MAPPED / DIVERGENT | VIS-360-HERO-004 |
| ENG-00 | 360 | `316:708` `ENG-00 \| Engineering Section` | 0,1016,360,1090 | `frontend/templates/home/includes/engineering.html` | `section#engineering.home-engineering` | `.home-engineering*`; 1 column below 640px | — | MAPPED / DIVERGENT | VIS-360-ENG-001 |
| PRJ-00 | 360 | `316:716` `PRJ-00 \| Selected Work Section` | 0,2106,360,1950 | `home.html`; `home/includes/project-card.html` | `section#projects.home-projects` | `.home-projects*`; 1 column below 896px | project PNG/WebP variants | MAPPED / DIVERGENT | VIS-360-PRJ-001 |
| PRC-00 | 360 | `316:723` `PRC-00 \| Process Section` | 0,4056,360,1366 | `home/includes/process.html` | `section#process.home-process` | `.home-process*`; 1 column below 640px | — | MAPPED / DIVERGENT | VIS-360-PRC-001 |
| EVD-00 | 360 | `316:727` `EVD-00 \| Evidence and Contact Section` | 0,5422,360,1194 | `home.html` | `.home-evidence-contact`, `#evidence`, `#contact` | `.home-evidence*`, `.home-contact*` | — | MAPPED / DIVERGENT | VIS-360-EVD-001 |
| FTR-00 | 360 | `316:749` `FTR-00 \| Footer` | 0,6616,360,344 | `frontend/templates/includes/homepage-footer.html` | `.site-footer--homepage .homepage-footer` | `.site-footer--homepage`, `.homepage-footer*` | same logo family as IMG-01 | MAPPED / DIVERGENT | VIS-360-FTR-001 |
| AIR-00 | 360 | `316:751` `AIR-00 \| AI RAG Reserved Visual` (INSTANCE of `115:417`) | 130,6834,210,48 | `home.html` | `.home-ai-rag[aria-hidden=true]` | fixed bottom/right, pointer-events none | — | MAPPED / DIVERGENT | VIS-360-AIR-001 |
| IMG-02 | 768 | `297:374` `Homepage background — approved desktop asset` | 0,0,768,5416 | `home.css` | `.homepage__technology-background` | same continuous rule as above; 768×1388.8 module | same background asset | SEMANTIC CARRY-FORWARD / CONTINUOUS | SDD-RWD-001 IMG-02 finalization |
| HERO-02 | 768 | `297:379` `Professional titles` | 0,36,704,168 | `home.html` | `.home-hero__titles` | mobile grid remains active | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-HERO-001 |
| HERO-07A | 768 | `297:391` `IDE Code Region — Python Code` | 60,48,332,336 | `home.html` | `.home-hero__ide` | absolute | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-HERO-001 |
| HERO-08 | 768 | `297:392` `Repository Explorer` | 504,48,200,324 | `home.html` | `.home-hero__explorer` | absolute | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-HERO-001 |
| IMG-00 | 768 | `297:465` `Professional portrait — approved transparent production asset` | 153,720,462,379.05 | profile include | `.profile-photo` | mobile visual composition | portrait responsive set | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-HERO-001 |
| ENG-00 | 768 | `297:466` `Engineering` | 0,1160,768,616 | engineering include | `#engineering` | 2 columns from 640px | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-ENG-001 |
| PRJ-00 | 768 | `297:474` `Selected Work` | 0,1776,768,1708 | project include | `#projects` | 1 column below 896px | project responsive sets | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-PRJ-001 |
| PRC-00 | 768 | `297:481` `Process` | 0,3484,768,888 | process include | `#process` | 2-column staged layout from 640px | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-PRC-001 |
| EVD-00 / CTA-00 | 768 | `297:485` / `297:502` `Evidence and Contact` / `Contact CTA` | 0,4372,768,850 / 32,440,704,282 | `home.html` | `.home-evidence-contact`, `#contact` | 2-column evidence, stacked CTA | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-EVD-001 |
| FTR-00 / AIR-00 | 768 | `297:507` / `297:509` | 0,5222,768,194 / 526,5126,210,48 | footer include / `home.html` | `.homepage-footer` / `.home-ai-rag` | horizontal footer ≥640px / fixed AIR | logo family | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-768-FTR-001, VIS-768-AIR-001 |
| IMG-02 | 1024 | `270:1358` `Homepage background — approved desktop asset` | 0,0,1024,4428 | `home.css` | `.homepage__technology-background` | same continuous rule as above; 1024×1851.7333 module | same background asset | SEMANTIC CARRY-FORWARD / CONTINUOUS | SDD-RWD-001 IMG-02 finalization |
| HERO-02 | 1024 | `270:1363` `Professional titles` | 0,36,416,224 | `home.html` | `.home-hero__titles` | desktop Hero starts at 967px | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-1024-HERO-001 |
| HERO-07A / HERO-08 | 1024 | `270:1375` / `270:1376` | 28,36,332,336 / 306,36,174,324 | `home.html` | `.home-hero__ide`, `.home-hero__explorer` | desktop Hero rules | — | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-1024-HERO-001 |
| IMG-00 | 1024 | `270:1449` portrait | 514,278,470,385.5 | profile include | `.profile-photo` | picture left 52%, width ≤88% | portrait responsive set | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-1024-HERO-001 |
| ENG-00 / PRJ-00 / PRC-00 | 1024 | `270:1450` / `270:1458` / `270:1465` | section frames | section templates | `#engineering`, `#projects`, `#process` | 2-col, 2+1 cards, 3+3+1 process modes | project assets | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-1024-LAYOUT-001 |
| EVD-00 / CTA-00 / FTR-00 / AIR-00 | 1024 | `270:1469` / `270:1486` / `270:1491` / `270:1493` | section frames | `home.html`, footer include | evidence/contact/footer/AIR selectors | current responsive rules | logo family | SEMANTIC CARRY-FORWARD / DIVERGENT | VIS-1024-LAYOUT-001 |
| IMG-02 | 1440 | `199:1358` `[IMG-02] Homepage background — approved desktop asset` (RECTANGLE, image FILL) | 0,0,1440,2604 | `home.css` | `.homepage__technology-background` | same continuous rule as above; 1440×2604 module; unclamped above 1440 | background asset; Figma hash/SHA-1 `b06fb16c…` | MAPPED / CONTINUOUS | SDD-RWD-001 IMG-02 finalization |
| HDR-00 | 1440 | `153:3` `[HDR-00] Header` (INSTANCE of `136:708`) | 0,0,1440,80 | `navigation.html`, language include | `.site-header .site-nav` | full Header ≥848px | logo family | MAPPED / DIVERGENT | VIS-1440-HDR-001 |
| HERO-01/02/03 | 1440 | `153:1173` / `153:1174` / `153:1175` | headline: 0,36,688,168; Inter Semi Bold 48/56 | `home.html` | greeting/titles/positioning selectors | desktop Hero rules | — | MAPPED / DIVERGENT | VIS-1440-HERO-001 |
| HERO-04A / HERO-05 | 1440 | `153:1177` / `153:1183` | 145×48 / 96×44 | `home.html` | CTA and social selectors | shared button/social styles | inline icons | MAPPED / DIVERGENT | VIS-1440-HERO-002 |
| HERO-07A / HERO-08 | 1440 | `170:373` / `192:373` | 28,12,332,336 / 360,20,248,324 | `home.html` | IDE/explorer selectors | absolute desktop Hero rules | — | MAPPED / DIVERGENT | VIS-1440-HERO-001 |
| IMG-00 | 1440 | `153:1200` `[IMG-00] Professional portrait…` | 760,203.87,600,492.13 | profile include | `.profile-photo` | centered absolute picture | portrait responsive set; Figma hash `0d13002a…` | MAPPED / DIVERGENT | VIS-1440-HERO-001 |
| ENG-00/01 | 1440 | `153:1201` / `153:1204` | 0,560,1440,380 / 48,136,1344,204 | engineering include | `#engineering`, `.home-engineering__list` | 4 columns ≥1200px | — | MAPPED / DIVERGENT | VIS-1440-ENG-001 |
| PRJ-00/01 | 1440 | `153:1221` / `153:1224` | 0,940,1440,700 / 48,168,1344,502 | project include | `#projects`, `.home-projects__list` | 3 columns ≥1200px | project PNG/WebP variants | MAPPED / DIVERGENT | VIS-1440-PRJ-001 |
| PRC-00 | 1440 | `154:1283` `[PRC-00] Process` | 0,1640,1440,366 | process include | `#process` | 7 columns ≥1200px | — | MAPPED / DIVERGENT | VIS-1440-PRC-001 |
| EVD-00/01/02 | 1440 | `154:1315` / `154:1316` / `154:1319` | 0,2006,1440,410 | `home.html` | `#evidence`, `.home-evidence__list` | 4 columns ≥1200px | — | MAPPED / DIVERGENT | VIS-1440-EVD-001 |
| CTA-00 | 1440 | `154:1332` `[CTA-00] Contact CTA` | 916,64,476,282 | `home.html` | `#contact.home-contact` | evidence/contact 2fr:1fr | — | MAPPED / DIVERGENT | VIS-1440-EVD-001 |
| FTR-00/01 | 1440 | `154:1342` / `154:1343` | 0,2416,1440,188 / 120,32,1200,130 | footer include | `.homepage-footer` | horizontal ≥640px | logo family | MAPPED / DIVERGENT | VIS-1440-FTR-001 |
| AIR-00 | 1440 | `154:1374` `[AIR-00] AI RAG Launcher` | 1182,2360,210,48 | `home.html` | `.home-ai-rag` | fixed in browser vs flow-positioned reference state | — | MAPPED / DIVERGENT | VIS-1440-AIR-001 |

## Image authority inventory

| Authority | Repository identity | Dimensions | Browser presentation | Result |
|---|---|---:|---|---|
| IMG-00 portrait | `luis-franca-transparent-02.png`, SHA-256 `1c2a24c…`; WebP derivatives `5cc3410e…`, `55bf14b3…`, `dc316ae6…` | master 1385×1136 | `<picture>`; FIT-like `object-fit:contain`; current source selected by viewport | Asset family exists and visually matches subject; geometry differs |
| IMG-01 brand | `lf-information-system.png`, SHA-256 `65610007…`; WebP derivatives including current 600px `65145642…` | square 1254/600/300 | 48×48 Header box (`site.css`), `object-fit:contain`; black pixels are in the chosen square asset | Wrong presentation/asset variant for Figma's transparent horizontal 68×44 mark |
| IMG-02 background | `homepage-background-desktop-02.png`, SHA-1 `b06fb16c…`, SHA-256 `09eb5be0…` | repository export 933×1686; canonical presentation 1440×2604 | dedicated absolute decorative layer; center-top; `100vw auto`; `repeat-y` | Canonical asset and continuous presentation mapped; pending human visual review |
| Project 1 | `enterprise-platform.png` + 450/900 WebP | 1480×16384 master | `<picture>`, 16:7 crop, `object-fit:cover`, top | Exists; text/action density diverges; lazy full-page capture limitation noted |
| Project 2 | `intelligent-currency-platform.png` + 450/900 WebP | 1480×16384 master | same | Exists; text/action density diverges; lazy full-page capture limitation noted |
| Project 3 | `sistema_cotacao_moedas.png` + 450/900 WebP | 1480×7636 master | same | Exists; composition/text/actions diverge |

## Validation summary

- All Figma node IDs cited in this matrix were returned by the live Figma API.
- All repository files, selectors, and assets cited above exist in the inspected working tree.
- Semantic IDs are consistent across viewports in this matrix.
- Native traceability naming is complete for the important 360 and 1440 layers but incomplete for 768 and 1024; those mappings are explicitly labeled semantic carry-forward.
- No production HTML, CSS, JavaScript, asset, breakpoint, content, or Figma geometry was changed.
