# SDD-RWD-001 — Human Visual Findings Register

## Integrated remediation closure — 2026-08-23

All CRITICAL/HIGH findings below were revalidated against native Figma nodes, corrected, and closed with Chromium evidence under `artifacts/responsive-visual/integrated-remediation/`. Root causes were the wrong brand asset, native select presentation, hidden compact WhatsApp, divergent component anatomy/content, oversized accumulated spacing, and incomplete AIR-00 structure. Files changed and correction details are consolidated in `SDD-RWD-001-integrated-visual-remediation.md`. Final status: **RESOLVED**, pending human visual acceptance.

The Hero technology composition received a scoped architectural refactor on 2026-08-23. IMG-02, IDE, gutter, Explorer, and IMG-00 now have independent geometry and explicit stacking; the competing stretched IMG-02 rule was removed, and the rejected HERO-09A rim remains disabled. Deterministic Chromium evidence is under `artifacts/responsive-visual/hero-tech-refactor/`. Status: **TECHNICALLY RESOLVED — PENDING HUMAN VISUAL REVIEW**; automated evidence does not constitute human acceptance of the atmospheric crop.

Status: OPEN<br>
Date: 2026-08-23<br>
Scope: Phase 0 traceability and visual audit only. No remediation was performed.

## Preflight and authority

- Current governance: Blocks 1–13 human approved; Block 14 technical pass but human visual review rejected; responsive implementation is not human accepted.
- Live Figma file inspected: `Site Portfolio — Target Product`, file key `7XIYTbKZrLk77biI0UhRIb`.
- Approved frames inspected: 360 `316:615`, 768 `297:373`, 1024 `270:1357`, 1440 `153:2`.
- Localhost captured at exactly the four required CSS widths in Chromium 151, DPR 1, 100% zoom.
- Severity vocabulary: CRITICAL, HIGH, MEDIUM only. Every finding below begins OPEN.

## Header findings

### VIS-360-HDR-001 — OPEN — wrong logo presentation — HIGH

- Viewport/section: 360 / Header; Traceability: IMG-01; Figma node: `I316:617;169:1131`; layer: `IMG-01 | LF Brand Logo`.
- Figma evidence: transparent horizontal LF mark in a 68×44 image-FIT rectangle at (24,14).
- Localhost evidence: visibly black square tile; the browser selects `static/images/brand/lf-information-system-600.webp` and CSS constrains it to 48×48.
- Repository: `brand-logo.html` → `.site-nav__brand img.brand-logo`; `site.css` → `.site-nav__brand .brand-logo`.
- Deviation/cause: the responsive `<picture>` serves a square asset containing a black background, while the reference uses a transparent horizontal lockup. This is an asset/presentation mismatch, not a missing file.
- Remediation scope: brand asset authority, responsive source selection, Header sizing only. Confidence: HIGH.

### VIS-360-HDR-002 — OPEN — unauthorized compact locale control — HIGH

- Viewport/section: 360 / Header; Traceability: HDR-02; Figma node: `I316:617;136:755`; layer: `HDR-02 | Compact Controls`.
- Figma evidence: compact controls contain only WhatsApp and Menu (111×44); there is no locale selector descendant in the 360 Header instance. Full Figma Headers at 1024/1440 use the explicit `PT | EN` Language selector component.
- Localhost evidence: native select is always present and displays `English` or `Português (Brasil)`, consuming substantial Header width.
- Repository: `language-selector.html` → `form.language-selector > select#language-selector`; `site.css` has no compact-hide or compact replacement rule.
- Deviation/cause: implementation divergence. The native select is accessibility-capable, but no approved evidence records it as an intentional replacement, and it contradicts both compact Figma composition and full-mode `PT | EN` treatment. Product/design decision remains unresolved.
- Remediation scope: Header product decision, accessible locale interaction, compact/full presentation. Confidence: HIGH.

### VIS-360-HDR-003 — OPEN — WhatsApp absent in resting compact Header — CRITICAL

- Viewport/section: 360 / Header; Traceability: HDR-03; Figma node: `I316:617;136:756`; layer: `HDR-03 | WhatsApp Action`; expected 44×44 instance with `Icon/WhatsApp` (`74:15`).
- Figma evidence: WhatsApp icon is visible beside the Menu toggle.
- Localhost evidence: no WhatsApp action is visible in the closed 360 Header.
- Repository: `.site-nav__whatsapp` exists conditionally in `.site-nav__menu`; the entire menu is `display:none` through 847px until JS adds `.is-open`.
- Deviation/cause: DOM presence but CSS-hidden resting state; implementation structure cannot realize the approved persistent compact action.
- Remediation scope: Header DOM/component placement and compact CSS visibility, without inferring unrelated navigation behavior. Confidence: HIGH.

### VIS-1440-HDR-001 — OPEN — full Header controls and branding diverge — HIGH

- Viewport/section: 1440 / Header; Traceability: HDR-00/IMG-01; Figma node: `153:3`; layer: `[HDR-00] Header`, instance of Full Header `136:708`.
- Figma evidence: 80px Header, transparent horizontal logo, plain `PT | EN`, circular 44px WhatsApp icon.
- Localhost evidence: 72px-like compact visual density, black square logo, native `English` select, and green text pill `WhatsApp`.
- Repository: `navigation.html`, `brand-logo.html`, `language-selector.html`, `.site-header`, `.site-nav`, `.site-nav__whatsapp`, `.language-selector select`.
- Deviation/cause: current shared Header predates or bypasses the approved Header component variants.
- Remediation scope: Header component presentation and asset choice. Confidence: HIGH.

## Hero findings

### VIS-360-HERO-001 — OPEN — professional title wrapping differs — HIGH

- Viewport/section: 360 / Hero; Traceability: HERO-02; Figma node: `316:621`; layer: `HERO-02 | Professional Titles`.
- Figma evidence: 320×102, Inter Semi Bold 26/34; exactly three title lines.
- Localhost evidence: `Software Engineer` and `Python Backend Engineer` wrap into additional lines; Hero title block is materially taller.
- Repository: `h1.home-hero__titles > span.home-hero__title`; font uses `clamp(2rem,7.7vw,4rem)` (about 32px at 360), line-height 1.06.
- Deviation/cause: mobile font sizing is larger than Figma and each title span is allowed to wrap.
- Remediation scope: Hero responsive typography/available width. Confidence: HIGH.

### VIS-360-HERO-002 — OPEN — primary CTA has wrong fill — HIGH

- Viewport/section: 360 / Hero; Traceability: HERO-04A; Figma node `316:624`; layer `HERO-04A | Primary CTA`.
- Figma evidence: deep blue fill (approximately RGB 1/50/174) and blue stroke, 145×48.
- Localhost evidence: yellow CTA.
- Repository: `a.home-hero__cta.button.button--primary`; `.button--primary` resolves to shared yellow accent variables.
- Deviation/cause: shared Release 1 primary-button token conflicts with approved Homepage component appearance.
- Remediation scope: Homepage-scoped button appearance/token mapping. Confidence: HIGH.

### VIS-360-HERO-003 — OPEN — LinkedIn visual identity differs — HIGH

- Viewport/section: 360 / Hero; Traceability: HERO-05A; Figma node `I316:625;133:613`; layer `HERO-05A | LinkedIn Action`.
- Figma evidence: approved 44×44 action component with recognizable LinkedIn-blue icon treatment.
- Localhost evidence: neutral outlined square with a text `in` glyph.
- Repository: `a.home-hero__social[aria-label="LinkedIn"] > span` and generic `.home-hero__social`.
- Deviation/cause: hand-authored text glyph/generic style substitutes for the approved icon component. GitHub uses a recognizable inline SVG and is present.
- Remediation scope: social icon asset/component and Homepage-scoped appearance. Confidence: HIGH.

### VIS-360-HERO-004 — OPEN — technology and portrait composition differs — HIGH

- Viewport/section: 360 / Hero; Traceability: HERO-07A/HERO-08/IMG-00; Figma nodes `316:633`, `316:634`, `316:707`.
- Figma evidence: visual frame 320×500; IDE 186×246 at (14,24), Explorer 148×310 at (172,21), portrait 320×262.58 at (0,220).
- Localhost evidence: portrait renders materially narrower and higher relative to the reference; code/explorer proportions, margins, and occlusion differ.
- Repository: `.home-hero__visual`, `.home-hero__ide`, `.home-hero__explorer`, `.home-hero__visual picture`, `.profile-photo`.
- Deviation/cause: percentage/clamp-based absolute composition does not reproduce the approved reference relationship at 360.
- Remediation scope: responsive Hero visual layout rules; do not translate Figma coordinates directly to page-level absolute positioning. Confidence: HIGH.

### VIS-768-HERO-001 — OPEN — Hero scale and vertical composition differ — HIGH

- Viewport/section: 768 / Hero; Traceability: HERO-02/HERO-07A/HERO-08/IMG-00; Figma nodes `297:379`, `297:391`, `297:392`, `297:465`.
- Figma evidence: 1088px Hero; full-width copy followed by a deliberate 704px visual composition with 462×379 portrait.
- Localhost evidence: title typography, whitespace, portrait scale, and technology occlusion differ; local section rhythm contributes to a 5760px document versus Figma 5416px.
- Repository: Hero selectors in `home.css`; single-column Hero remains active below 967px.
- Deviation/cause: typography clamps and percentage-based visual geometry diverge from the reference state.
- Remediation scope: 768 Hero typography and local composition rules. Confidence: HIGH.

### VIS-1024-HERO-001 — OPEN — split Hero is over-wrapped and miscomposed — HIGH

- Viewport/section: 1024 / Hero; Traceability: HERO-02/HERO-07A/HERO-08/IMG-00; Figma nodes `270:1363`, `270:1375`, `270:1376`, `270:1449`.
- Figma evidence: 640px Hero; 416px copy and 480px visual; IDE 332×336, Explorer 174×324, portrait 470×385.5.
- Localhost evidence: professional titles break into many more lines and the visual cluster/portrait relation differs; local document is about 5101px versus Figma 4428px.
- Repository: desktop Hero switches at 967px to `0.9fr / minmax(28rem,1.1fr)` while the global title clamp can reach 64px.
- Deviation/cause: copy column and global clamp combine into excessive wrapping; implementation geometry is not aligned with the approved 1024 art direction.
- Remediation scope: 1024 Hero responsive typography and visual layout only. Confidence: HIGH.

### VIS-1440-HERO-001 — OPEN — Desktop Hero geometry differs — HIGH

- Viewport/section: 1440 / Hero; Traceability: HERO-00/02/07A/08/IMG-00; Figma nodes `153:1171`, `153:1174`, `170:373`, `192:373`, `153:1200`.
- Figma evidence: Hero 1440×480; headline 688×168 at 48/56; visual 608×384; portrait 600×492.13 and deliberately overhangs into Engineering.
- Localhost evidence: Hero consumes substantially more vertical space; title copy is constrained and `Python Backend Engineer` wraps; portrait and technology composition are larger/differently aligned.
- Repository: `.home-hero` has fluid padding/gap and two fractional columns; `.home-hero__visual` min-height reaches about 42rem.
- Deviation/cause: implementation min-height and column proportions conflict with the compact approved Desktop composition.
- Remediation scope: Desktop Hero grid, min-height, typography, and local overlap relationship. Confidence: HIGH.

### VIS-1440-HERO-002 — OPEN — Hero action treatments differ — HIGH

- Viewport/section: 1440 / Hero; Traceability: HERO-04A/HERO-05; Figma nodes `153:1177`, `153:1183`.
- Figma evidence: deep-blue primary CTA and blue LinkedIn action.
- Localhost evidence: yellow primary CTA and neutral LinkedIn action.
- Repository: shared `.button--primary` and `.home-hero__social`.
- Deviation/cause/remediation: same component/token mismatch as 360, observable at Desktop. Homepage-scoped action alignment required. Confidence: HIGH.

## Engineering, projects, process, evidence/contact, footer, and AI/RAG

### VIS-360-ENG-001 / VIS-768-ENG-001 / VIS-1440-ENG-001 — OPEN — Engineering card anatomy differs — HIGH

- Traceability/Figma: ENG-00/ENG-01; 360 `316:708/711`, 768 `297:466/469`, 1440 `153:1201/1204`.
- Figma evidence: restrained ordinal/title/description cards; approved frame heights are 1090, 616, and 380 respectively.
- Localhost evidence: extra prominent icon tiles and direction arrows change card anatomy, density, and height; Desktop section is materially taller than 380px.
- Repository: `home/includes/engineering.html` explicitly renders `.home-engineering__icon` and `.home-engineering__direction`; `home.css` styles both.
- Deviation/cause: implementation adds visual elements not present in the approved Homepage references.
- Remediation scope: Engineering card template/component presentation and section spacing. Confidence: HIGH.

### VIS-360-PRJ-001 / VIS-768-PRJ-001 / VIS-1440-PRJ-001 — OPEN — Project card content and actions diverge — HIGH

- Traceability/Figma: PRJ-00/PRJ-01; 360 `316:716/719`, 768 `297:474/477`, 1440 `153:1221/1224`.
- Figma evidence: concise summaries/tags and `View case study` plus recognizable GitHub icon action; approved section heights 1950, 1708, 700.
- Localhost evidence: much denser summaries and tag sets, long accessibility-label text is visibly used as the source link, no matching case-study button/icon pair; Desktop section is substantially taller.
- Repository: `home/includes/project-card.html`; `.home-project__summary`, `__technologies`, `__actions`.
- Deviation/cause: current data/template contract and action markup do not match approved card component content hierarchy.
- Remediation scope: project-card presentation/content decision and action components. Confidence: HIGH.
- Evidence caveat: first/second lazy images are blank in some automated full-page captures because Chromium captured before offscreen lazy loads; assets exist and this capture artifact is not registered as a product defect.

### VIS-360-PRC-001 / VIS-768-PRC-001 / VIS-1440-PRC-001 — OPEN — Process descriptions missing — HIGH

- Traceability/Figma: PRC-00; nodes `316:723`, `297:481`, `154:1283`.
- Figma evidence: each of seven stages includes a title and explanatory body; mobile uses substantial cards and Desktop remains a compact seven-card row.
- Localhost evidence: only marker and title are rendered at every width; descriptions are absent. At 360 the local Process is far shorter than the 1366px Figma section.
- Repository: `home/includes/process.html` renders only `step.ordinal` and `step.title`; `.home-process__step` has no body selector.
- Deviation/cause: required explanatory content is absent from the DOM, not merely hidden by CSS.
- Remediation scope: content contract/template plus responsive card anatomy; content changes require later authorization. Confidence: HIGH.

### VIS-360-EVD-001 / VIS-768-EVD-001 / VIS-1440-EVD-001 — OPEN — Evidence cards omit approved explanatory copy — HIGH

- Traceability/Figma: EVD-00/EVD-01/EVD-02 and CTA-00; 360 `316:727`, 768 `297:485/486/489/502`, 1440 `154:1315/1316/1319/1332`.
- Figma evidence: four Evidence cards contain headings and explanatory body copy; Contact CTA uses approved blue primary action.
- Localhost evidence: Evidence items are icon/title chips without descriptions; Contact CTA is yellow and the card treatment/spacing differs.
- Repository: `home.html` renders only icon and `theme.title`; `.home-contact__action.button--primary` inherits yellow shared styling.
- Deviation/cause: missing Evidence body DOM plus shared CTA token mismatch.
- Remediation scope: Evidence content/template and Contact action appearance. Confidence: HIGH.

### VIS-360-FTR-001 / VIS-768-FTR-001 / VIS-1440-FTR-001 — OPEN — Footer branding and social actions differ — HIGH

- Traceability/Figma: FTR-00/FTR-01; nodes `316:749`, `297:507/508`, `154:1342/1343`.
- Figma evidence: transparent horizontal LF mark and compact LinkedIn/GitHub icon actions; reference heights 344/194/188.
- Localhost evidence: black square logo and text links `LinkedIn`/`GitHub`; Footer geometry differs, especially at 1440.
- Repository: `homepage-footer.html`, shared `brand-logo.html`, `.homepage-footer*`.
- Deviation/cause: same wrong logo variant and non-component social markup.
- Remediation scope: Footer asset/action components and spacing. Confidence: HIGH.

### VIS-360-AIR-001 / VIS-768-AIR-001 / VIS-1440-AIR-001 — OPEN — AI/RAG reserved visual is incomplete — HIGH

- Traceability/Figma: AIR-00; nodes `316:751`, `297:509`, `154:1374`, all instances of `115:417`, 210×48.
- Figma evidence: label/copy plus a separate circular blue robot action; positioned near the bottom-right reference state.
- Localhost evidence: a small fixed text-only `AI / RAG` pill, lacking the robot action and supporting copy; it appears over Hero/other content according to viewport because it is fixed.
- Repository: `<div class="home-ai-rag" aria-hidden="true"><span>AI / RAG</span></div>`; fixed CSS.

2026-08-23 closure: **RESOLVED — PENDING HUMAN VISUAL REVIEW**. The invariant approved product label is now `Jujuju AI`; supporting copy is removed in code and on live Figma instances. The position regression was traced to a higher-specificity direct-child rule introduced with IMG-02 ownership and corrected by excluding `.home-ai-rag`. Dedicated evidence: `artifacts/responsive-visual/air-00-jujuju/`.

2026-08-23 brand supersession: the approved AIR-00 identity changed from historical `Jujuju AI` to current `Juju IA`. Application and the same four live Figma instance IDs were synchronized without geometry or positioning changes. Evidence: `artifacts/responsive-visual/air-00-brand-rename/`.
- Deviation/cause: placeholder implementation represents only part of the approved reserved visual.
- Remediation scope: reserved visual markup/presentation and fixed-position behavior, while preserving Release 1 non-functional semantics. Confidence: HIGH.

## Background findings

### VIS-360-BG-001 / VIS-768-BG-001 / VIS-1024-BG-001 / VIS-1440-BG-001 — OPEN — HERO-BG-001 remains visually rejected — HIGH

- Traceability: IMG-02. Figma nodes: 360 `316:616`, 768 `297:374`, 1024 `270:1358`, 1440 `199:1358`; all use image hash `b06fb16c…` as a full-frame image fill.
- Figma evidence: background authority covers each entire approved frame (6960/5416/4428/2604px high) with persistent luminous arcs/particles through lower sections.
- Localhost evidence: correct-named 933×1686 repository asset is present, but the overlay reaches opaque `#020b1f` at 78rem and the no-repeat image is scaled by width only. Lower sections become almost uniform dark; at 1440 the document is about 3774px, far beyond the visual asset/fade range.
- Repository: `.homepage` in `home.css`; `background-size:max(100%,720px) auto`, `background-position:center top`, no-repeat, gradient overlay.
- Deviation/cause: asset presentation and total document geometry suppress/cut off the approved background; existence of the asset is not proof of correctness.
- Remediation scope: Homepage background crop/coverage/overlay coordinated with section geometry. Confidence: HIGH.

## Whole-page geometry findings

### VIS-1024-LAYOUT-001 — OPEN — reference-state vertical rhythm diverges — HIGH

- Viewport: 1024; sections: Engineering through Footer; Traceability: ENG-00, PRJ-00, PRC-00, EVD-00, CTA-00, FTR-00.
- Figma evidence: frame height 4428; section boundaries at y=720,1336,2666,3384,4234.
- Localhost evidence: capture height about 5101; repeated larger gaps/card heights accumulate after Hero.
- Repository: fluid section padding `clamp(2.5rem,7vw,5.5rem)`, card content-driven heights, and current breakpoint modes.
- Deviation/cause: aggregate content anatomy and spacing mismatch, not a single absolute-position defect.
- Remediation scope: later section-by-section responsive remediation while protecting approved FIT breakpoints. Confidence: HIGH.

### VIS-1440-LAYOUT-001 — OPEN — Desktop page is approximately 45% taller than authority — HIGH

- Viewport: 1440; sections: full Homepage; Traceability: all top-level IDs.
- Figma evidence: 1440×2604 with section boundaries 0/80/560/940/1640/2006/2416/2604.
- Localhost evidence: 1440×about 3774; Hero, Engineering, Projects, Process, Evidence/Contact, and Footer all consume more vertical space.
- Repository: fluid padding, content-rich cards, Hero min-height, and differing component anatomy compound the result.
- Deviation/cause: systemic reference-state geometry mismatch.
- Remediation scope: coordinated section-level remediation, not direct page-level absolute coordinates or breakpoint redesign. Confidence: HIGH.

## Browser evidence and validation

- Figma screenshots: `artifacts/responsive-visual/phase0/figma/homepage-{360,768,1024,1440}.png`.
- Localhost screenshots: `artifacts/responsive-visual/phase0/localhost/homepage-{en-us,pt-br}-{360,768,1024,1440}.png`.
- Browser measurement record: `artifacts/responsive-visual/phase0/localhost/block14-visual-validation.json` (legacy filename from the existing capture harness; directory establishes Phase 0 ownership).
- Localhost routes loaded successfully in both locales. Existing capture measurements report no horizontal overflow at the reference widths.
- Project image blanks in some 768/1024 automated captures are a lazy-loading evidence limitation; they are not classified as missing-product findings.

## Remaining uncertainties and final gate

1. Native Figma Traceability IDs are embedded on important 360 and 1440 layers, but most 768 and 1024 layers still retain plain semantic names. Their native IDs are known and semantic correlations are reliable, but normalization is incomplete.
2. The compact Header has no locale control in its actual 360 descendant tree, while the task prose describes `PT | EN`; this is an unresolved design/product decision, not silently adjudicated here.
3. Figma image hashes establish cross-viewport design identity, but repository asset bytes were not exported from Figma for byte-level equivalence. Visual identity is sufficient for portrait/background correlation; the brand is visibly divergent.
4. Human review is required to prioritize and approve remediation; every finding remains OPEN.

**VISUAL-REMEDIATION-P0 — HOLD — TRACEABILITY GAP**

Exact gaps: native Traceability ID normalization is absent on most 768/1024 nodes; the 360 locale-control authority conflicts with the prose requirement; and the Figma image hash-to-repository-byte mapping is not canonical for IMG-01/IMG-02. No visual remediation may begin under this gate.
