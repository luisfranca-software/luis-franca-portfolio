# SDD-RWD-001 — Homepage Responsive Implementation Specification

**Document ID:** SDD-RWD-001

**Specification ID:** SDD-RWD-001

**Version:** 1.0.0

**Status:** Human Approved

**Project:** Site Portfolio

**Owner:** Architecture & Engineering Review

**Approver:** Product Owner

**Development Model:** Specification-Driven Development (SDD)

**Last Updated:** 2026-08-21

**Target Release:** Release 1.1 — Platform Maturity

**Design Authority:** FIGMA-04 / FIGMA-05

**Specification Gate:** Approved for Implementation Preparation

**Implementation State:** Not Started

**Intrinsic-Fit State:** FIT-CANDIDATE

---

# 1. Purpose

This specification defines the approved responsive implementation contract for the Release 1.1 Homepage. It translates the human-approved FIGMA-04 responsive compositions and FIGMA-05 implementation handoff into deterministic, testable, and traceable engineering requirements.

Approval of this document authorizes only the next responsive implementation preflight. It does not record implementation as started and does not independently authorize production mutation.

---

# 2. Revalidated Repository Baseline

The specification was approved against the following repository evidence:

* repository root: `/home/luis/projects/luis-franca-portfolio`;
* branch: `main`;
* inspected commit: `10ce72cc9c6cf1481a174c68c3cdfbc41c8f435f`;
* presentation architecture: Django Templates, shared base template, shared Header and Footer, global CSS, and minimal framework-free JavaScript;
* supported languages: English and Brazilian Portuguese through Django i18n;
* existing Header behavior: `position: sticky`, top-anchored, with an existing compact disclosure;
* existing navigation: shared links to Home, About, Skills, Experience, Portfolio, and Contact;
* existing WhatsApp behavior: active viewport-fixed Release 1 control;
* current AI/RAG state: no assistant, RAG, retrieval, intelligent search, AI API, chat, or launcher behavior implemented;
* current responsive tests: primarily integration and CSS-source assertions, without demonstrated real-browser intrinsic-fit or visual-regression infrastructure.

Protected untracked design and image assets existed during approval. They are repository inputs, not evidence that responsive production implementation has begun.

No new normative conflict was identified during the approval revalidation.

---

# 3. Governance and Normative Authority

This specification is governed by EGS-001, PB-001, TS-001, ARCH-001, approved ADRs, TST-001, SPEC-001, SPEC-002, SPEC-003, FIGMA-04, FIGMA-05, and the human-approved decisions consolidated in section 5.

For Release 1.1 Homepage visual implementation, FIGMA-04 and FIGMA-05 supersede conflicting SPEC-001 visual clauses only. SPEC-001 and the remaining governance hierarchy continue to govern functionality, architecture, routes, accessibility, security, testing, operations, internationalization, non-conflicting visual requirements, and unrelated routes.

Homepage styling shall be scoped. Shared tokens or components shall not silently propagate the Homepage visual language to unrelated pages.

---

# 4. Scope

## 4.1 In Scope

* one coherent responsive Homepage;
* the approved 360, 768, 1024, and 1440 reference compositions;
* Homepage navigation for Engineering, Projects, Process, and Contact;
* preservation of existing non-Homepage routes and navigation behavior;
* preservation of sticky Header runtime behavior;
* migration of WhatsApp access from the Release 1 floating control to the approved Header;
* Hero copy, actions, technology composition, portrait, and background;
* Engineering, Projects, Process, Evidence, Contact CTA, and Footer presentation;
* a noninteractive AI/RAG reserved visual;
* intrinsic-fit validation, responsive images, accessibility, i18n, and regression protection.

## 4.2 Out of Scope

* AI assistant behavior, RAG, retrieval, intelligent search, AI backend or API integration, and chat;
* deleting or replacing existing routes;
* global information-architecture or unrelated-page visual redesign;
* Analytics, advanced SEO, numeric performance budgets, and broad design-system refactoring;
* dependency or frontend-framework replacement;
* Figma modification and deployment.

---

# 5. Consolidated Human Decisions

| Decision | Status | Normative outcome |
| --- | --- | --- |
| C-001 — Homepage Header / information architecture | RESOLVED / HUMAN APPROVED | Homepage primary navigation is Engineering, Projects, Process, and Contact. Existing routes and non-Homepage navigation remain preserved. |
| C-002 — AI/RAG release scope | RESOLVED / HUMAN APPROVED | Release 1.1 provides only a fixed, noninteractive reserved visual. Functional AI/RAG remains Release 2. |
| C-003 — Homepage visual authority | RESOLVED / HUMAN APPROVED | FIGMA-04/05 supersede conflicting SPEC-001 visual clauses for the Homepage only. |
| HEADER-STICKY | RESOLVED / HUMAN APPROVED | Existing sticky Header behavior shall be preserved. |
| WHATSAPP-HEADER-MIGRATION | RESOLVED / HUMAN APPROVED | WhatsApp moves to the approved Header; the legacy floating presentation is removed before AI/RAG reserved-visual acceptance. |

The preceding decisions are not open implementation choices.

---

# 6. Functional Requirements

| ID | Requirement |
| --- | --- |
| RWD-FR-001 | Release 1.1 shall use one coherent responsive Homepage and one semantic content structure. |
| RWD-FR-002 | The Homepage shall preserve approved content and semantic section order at all supported widths. |
| RWD-FR-003 | The Homepage Header shall visibly expose Engineering, Projects, Process, and Contact as its primary navigation destinations. |
| RWD-FR-004 | Existing non-Homepage routes shall remain directly addressable and their approved navigation behavior and content accessibility shall not regress. |
| RWD-FR-005 | The Header shall use Full presentation where content fit permits and Compact presentation where Full presentation does not fit. |
| RWD-FR-006 | The existing sticky Header runtime behavior shall be preserved in every responsive state. |
| RWD-FR-007 | The Compact Header shall operate as an accessible disclosure, close on Escape and after applicable navigation, and return focus to its trigger after Escape dismissal. |
| RWD-FR-008 | The Hero shall transition between approved stacked and split compositions without duplicating semantic content. |
| RWD-FR-009 | Hero Technology shall use a local positioning context and preserve the approved IDE, line-number, Explorer, portrait, rim, and depth relationships. |
| RWD-FR-010 | The Hero portrait shall scale and crop responsively without distortion or page-level overflow. |
| RWD-FR-011 | Engineering shall render 1, 2, or 4 columns according to validated intrinsic fit and the approved reference states. |
| RWD-FR-012 | Projects shall preserve source order and render one column, two columns with a centered final card, or three columns according to validated intrinsic fit. |
| RWD-FR-013 | Process shall preserve its seven-step sequence and transition through Vertical, Grid2, Grid3, and Horizontal presentations. |
| RWD-FR-014 | The final Validation process item shall remain centered in incomplete grid rows without DOM reordering. |
| RWD-FR-015 | Evidence shall transition among one-column, 2x2, and four-column presentations according to validated intrinsic fit. |
| RWD-FR-016 | Evidence and Contact CTA shall use the approved desktop side relationship and a stacked relationship below its validated fit threshold. |
| RWD-FR-017 | The Contact CTA shall remain content-driven, readable, and usable without fixed page or section heights. |
| RWD-FR-018 | The Footer shall transition between approved Horizontal and Stacked presentations while preserving semantic order and link availability. |
| RWD-FR-019 | Release 1.1 shall render the approved AI/RAG launcher visual as a noninteractive reserved visual element. |
| RWD-FR-020 | The reserved AI/RAG visual shall be fixed to the viewport bottom-right, independent of document flow and Footer position. |
| RWD-FR-021 | The reserved AI/RAG visual shall execute no AI, RAG, retrieval, search, API, chat, navigation, or other Release 2 behavior. |
| RWD-FR-022 | Responsive gutters shall follow the approved reference contract and interpolate without arbitrary framework-driven changes. |
| RWD-FR-023 | Every section shall use natural content height and remain continuous between approved reference widths. |
| RWD-FR-024 | Release 1.1 shall preserve the existing WhatsApp destination and external-link behavior through the approved Header, remove the legacy floating WhatsApp presentation, and render no duplicate Header and floating WhatsApp controls. |

---

# 7. Non-Functional Requirements

| ID | Requirement |
| --- | --- |
| RWD-NFR-001 | The implementation shall use semantic HTML, logical DOM order, valid landmarks, one `h1`, and ordered section headings. |
| RWD-NFR-002 | All available controls and links shall be keyboard operable and expose visible focus indication. |
| RWD-NFR-003 | Controls introduced or materially changed by this work shall provide at least a 44x44 CSS-pixel target area. |
| RWD-NFR-004 | The AI/RAG reserved visual shall not be focusable or expose button, link, launcher, or other false control semantics. |
| RWD-NFR-005 | The Homepage shall have no page-level horizontal overflow or accidental critical-content clipping at or between supported widths. |
| RWD-NFR-006 | Responsive behavior shall use mobile-first CSS, intrinsic sizing, Grid, Flexbox, and component-owned media queries. |
| RWD-NFR-007 | The implementation shall not create four independent Homepages or duplicate breakpoint-specific content markup without documented necessity. |
| RWD-NFR-008 | JavaScript layout calculation shall not be introduced where CSS provides the required behavior. |
| RWD-NFR-009 | Motion shall be restrained, honor `prefers-reduced-motion`, and never be required for content or operation. |
| RWD-NFR-010 | Images shall reserve layout space, preserve aspect ratio, use correct alternative-text treatment, and avoid avoidable oversized delivery. |
| RWD-NFR-011 | Homepage visual rules shall be scoped so unrelated routes do not inherit unauthorized FIGMA-04/05 styling. |
| RWD-NFR-012 | English and Brazilian Portuguese content shall pass equivalent fit, wrapping, overflow, and accessibility validation. |
| RWD-NFR-013 | The implementation shall remain compatible with the existing Django Template architecture and introduce no new frontend framework or dependency. |
| RWD-NFR-014 | Responsive and visual behavior shall be testable in a real browser at reference widths and transition boundaries. |
| RWD-NFR-015 | Sticky Header and fixed-overlay layering shall be deterministic and shall not conceal focused controls or critical content. |

---

# 8. Responsive Architecture Decision

## 8.1 Requirements and Constraints

One semantic Homepage must reproduce the approved states, preserve routes and sticky behavior, remain bilingual, and fit the existing Django Template and static-asset architecture.

## 8.2 Alternatives

* duplicated markup by breakpoint: rejected due to accessibility, i18n, testing, and maintenance risk;
* scaled Desktop composition: rejected because it does not implement approved reflow;
* JavaScript-computed responsive layout: rejected because CSS can express the required transitions;
* one semantic DOM with scoped mobile-first CSS and component-owned intrinsic thresholds: approved.

## 8.3 Decision

Use one semantic DOM, Homepage-scoped styling, reusable Django includes where cohesive, mobile-first CSS, intrinsic sizing, Grid and Flexbox, natural document flow, a local Hero positioning context, component-specific media queries after FIT validation, and minimal JavaScript limited to genuine interaction behavior.

The shared Header may render a route-aware Homepage composition. Shared Header, Footer, and global CSS changes require explicit regression protection.

---

# 9. Responsive Reference Contract

| Width | Approved state |
| --- | --- |
| 360 | Compact sticky Header; stacked Hero; 1-column Engineering; 1-column Projects; Vertical Process; 1-column Evidence; stacked Evidence/Contact; Stacked Footer |
| 768 | Compact sticky Header; stacked Hero; 2-column Engineering; 1-column Projects; Grid2 Process; 2x2 Evidence; stacked Evidence/Contact; Horizontal Footer |
| 1024 | Full sticky Header; split Hero; 2-column Engineering; 2+1 centered Projects; Grid3 Process; 2x2 Evidence; stacked Evidence/Contact; Horizontal Footer |
| 1440 | Full sticky Header; split Hero; 4-column Engineering; 3-column Projects; Horizontal Process; 4-column Evidence; desktop Evidence/Contact relationship; Horizontal Footer |

These widths are validation references, not automatically media-query thresholds. Interpolation probes shall include at least 390, 480, 640, 820, 900, 1100, and 1280 pixels.

---

# 10. Container and Gutter Contract

| Viewport | Gutter | Content width |
| --- | ---: | ---: |
| 360 | 20 px | 320 px |
| 768 | 32 px | 704 px |
| 1024 | 48 px | 928 px |
| 1440 | 48 px | 1344 px |

The Homepage shall use available width minus two responsive gutters, capped at the approved 1344 px desktop content width. Intermediate gutters shall use the simplest validated fluid or stepped expression. `clamp()` is permitted only if it reproduces the approved references and healthy interpolation. Fixed overlays shall account for safe-area insets independently.

---

# 11. Intrinsic-Fit Protocol

All structural thresholds begin as `FIT-CANDIDATE` and follow:

`FIT-CANDIDATE -> future implementation -> browser measurement -> FIT-TESTED -> boundary validation -> FIT-VALIDATED`

For every candidate, implementation shall:

1. render actual English and Brazilian Portuguese production content;
2. begin from a known valid composition;
3. vary viewport width progressively;
4. identify the first invalid width or first safely viable width;
5. inspect wrapping, overflow, clipping, child width, gaps, targets, collision, readability, and hierarchy;
6. record the measured threshold and environment;
7. test immediately below and above it;
8. compare with the applicable Figma references;
9. promote the state only after functional, accessibility, and visual acceptance.

Framework breakpoints shall not substitute for evidence. Candidates may be consolidated only where measured ranges safely overlap without regression.

---

# 12. FIT Candidate Matrix

The intervals bracket transitions using approved states and are not final thresholds.

| ID | Transition | Candidate interval | Primary constraints |
| --- | --- | --- | --- |
| FIT-HDR-001 | Compact to Full | greater than 768 through 1024 px | four destinations, locale, Header WhatsApp, targets, no collision |
| FIT-HERO-001 | Stacked to Split | greater than 768 through 1024 px | copy, actions, artwork width, portrait/Explorer integrity |
| FIT-ENG-001 | 1 to 2 columns | greater than 360 through 768 px | readable card width and gap |
| FIT-ENG-002 | 2 to 4 columns | greater than 1024 through 1440 px | four useful card widths |
| FIT-PRJ-001 | 1 to 2 columns | greater than 768 through 1024 px | card content and centered incomplete row |
| FIT-PRJ-002 | 2 to 3 columns | greater than 1024 through 1440 px | three useful card widths |
| FIT-PRC-001 | Vertical to Grid2 | greater than 360 through 768 px | labels, connectors, sequence clarity |
| FIT-PRC-002 | Grid2 to Grid3 | greater than 768 through 1024 px | three useful cells and centered Validation |
| FIT-PRC-003 | Grid3 to Horizontal | greater than 1024 through 1440 px | seven-step readability and connectors |
| FIT-EVD-001 | 1 to 2 columns | greater than 360 through 768 px | evidence card width |
| FIT-EVD-002 | 2 to 4 columns | greater than 1024 through 1440 px | four readable evidence items |
| FIT-EVD-003 | stacked to side relationship | greater than 1024 through 1440 px | Evidence and CTA useful widths |
| FIT-FTR-001 | Stacked to Horizontal | greater than 360 through 768 px | hierarchy, translated links, spacing |

Every entry remains `FIT-CANDIDATE` until a future implementation supplies browser evidence.

---

# 13. Header and WhatsApp Migration Specification

The Homepage Header shall expose Engineering, Projects, Process, and Contact. Existing `/`, `/about/`, `/skills/`, `/experience/`, `/portfolio/`, and `/contact/` routes and non-Homepage navigation behavior remain protected.

The Header shall preserve sticky top anchoring. Its layer shall remain above normal content, and its expanded Compact menu shall not be obscured by Hero artwork or fixed overlays. In-page targets shall account for sticky Header height.

The Compact disclosure shall use a native button, accessible name, `aria-expanded`, `aria-controls`, a 44x44 target, visible focus, Escape dismissal, focus return, and close-after-navigation behavior. Application-menu roles are prohibited.

Release 1.1 shall migrate WhatsApp to the approved Header while preserving its intended configured destination and external-link behavior. The Release 1 floating WhatsApp presentation shall be removed before AI/RAG reserved-visual acceptance. Header and floating WhatsApp controls shall not coexist as duplicates.

This is a current-state migration constraint, not an unresolved visual decision.

---

# 14. Hero Specification

Hero copy remains first in semantic order, preserves the approved hierarchy and actions, uses constrained fluid typography, and has no fixed height. Actions shall maintain accessible names and targets and wrap or stack without reordering.

Hero Technology shall use a bounded local coordinate system:

```text
Hero
├── Hero copy and actions
└── Hero visual
    ├── decorative depth/background
    ├── IDE/code and line-number layer
    ├── repository Explorer
    ├── portrait rim/depth
    └── portrait
```

Absolute positioning is permitted only within this Hero visual context. Page-global coordinates and hardcoded Figma page positions are prohibited. Approved IDE, Explorer, and portrait occlusion is intentional. Decorative layers shall be excluded from assistive technology.

The portrait shall preserve aspect ratio, reserve layout space, and use only approved cropping. Homepage background treatment shall remain scoped.

---

# 15. Engineering Specification

Engineering shall preserve semantic card order and reusable card structure. Its reference modes are 1, 2, 2, and 4 columns at 360, 768, 1024, and 1440 respectively. Cards shall use intrinsic height; equal mobile heights shall not be forced. FIT-ENG-001 and FIT-ENG-002 own transition validation.

---

# 16. Projects Specification

Projects shall preserve source order and reusable card semantics. Its modes are one column at 360 and 768, two columns with the final card centered at 1024, and three columns at 1440. Centering shall use layout rather than duplicate or reordered DOM. FIT-PRJ-001 and FIT-PRJ-002 own transition validation. The existing Portfolio route remains protected.

---

# 17. Process Specification

The semantic sequence is Requirements, Specification, Architecture, Implementation, Testing, Deployment, and Validation. Modes are Vertical at 360, Grid2 at 768, Grid3 at 1024, and Horizontal at 1440. Validation shall remain centered in incomplete rows without source-order changes. Connectors are presentational and shall not be the only expression of sequence.

---

# 18. Evidence and Contact Specification

Evidence uses one column at 360, 2x2 at 768 and 1024, and four columns at 1440. It preserves semantic order and content-driven height.

Evidence and Contact CTA use the approved side relationship at 1440 and stack below FIT-EVD-003. The CTA shall preserve readable line length, prominence, target size, natural height, and the existing Contact route.

---

# 19. Footer Specification

The Footer is Horizontal at 768, 1024, and 1440 and Stacked at 360. Stacked semantic order is:

1. LF;
2. copyright and Luís França;
3. Engineering with evidence.;
4. Projects / Contact;
5. LinkedIn / GitHub.

Dynamic year and translated content shall be included in FIT-FTR-001. Existing required route and professional links remain available. Homepage-specific Footer visual treatment shall not silently alter unrelated routes.

---

# 20. AI/RAG Reserved Visual Specification

In Release 1.1, visual presence is not a functional control. The reserved visual shall:

* have no `href` and not be a button;
* have no focusable `tabindex`;
* receive no click, keyboard, submit, navigation, dialog, or chat handler;
* expose no button, link, `aria-expanded`, `aria-haspopup`, or action-oriented semantics;
* be omitted from the accessibility tree where it communicates no available information;
* remain absent from sequential keyboard navigation;
* execute no Release 2 capability.

It shall use fixed bottom-right viewport anchoring, remain independent of Footer and document height, use the greater of the responsive gutter and applicable safe-area inset, remain visible during scroll, and avoid Header, Footer, and critical-content overlap.

The legacy floating WhatsApp control shall already be absent. WhatsApp remains accessible through the Header; the two controls shall not compete for a bottom-corner position.

---

# 21. Accessibility Specification

Implementation shall validate one Homepage `h1`, ordered `h2` sections, landmarks, meaningful navigation destinations, sticky-safe target positioning, logical DOM order, appropriate portrait alternative text, decorative-image handling, keyboard operation, visible focus, 44x44 targets, disclosure semantics, Escape and focus return, noninteractive AI/RAG semantics, meaningful external-link names, contrast, reduced motion, and EN/PT-BR text expansion.

---

# 22. Performance and Layout Stability

No authoritative numeric performance budget exists. Implementation shall nevertheless select appropriate portrait and background sources, avoid loading redundant large alternatives, define responsive derivative widths and formats during validation, reserve image space, prevent avoidable layout shift, avoid JavaScript responsive measurement and unnecessary dependencies, and preserve semantic content when decorative assets are delayed or unavailable.

Numeric budgets remain deferred to a Performance workstream.

---

# 23. Test Strategy

## 23.1 Template and Integration Tests

Validate Homepage section order, Homepage navigation labels and targets, existing route availability, Header WhatsApp destination and behavior, absence of the legacy floating WhatsApp control, absence of duplicate WhatsApp controls, AI/RAG noninteractive markup, absence of Release 2 endpoints or handlers, Footer links, and EN/PT-BR rendering.

## 23.2 Interaction Tests

Validate Compact menu open/close, `aria-expanded`, `aria-controls`, Escape dismissal, focus return, close after navigation, 44x44 targets, Header WhatsApp access, and sticky Header persistence.

## 23.3 Responsive Browser Tests

At 360, 768, 1024, and 1440 validate the Header, Hero, Engineering, Projects, Process, Evidence/Contact, Footer, overflow, clipping, natural height, fixed AI/RAG placement, safe-area behavior, and absence of collision with Header, Footer, or critical content.

## 23.4 FIT Tests

For every FIT ID, test the measured threshold and widths immediately below and above it. Record actual content, locale, browser, viewport, and result. English and PT-BR worst cases are mandatory.

## 23.5 Route Regression

Validate every existing route for HTTP availability, navigation reachability, Header/Footer usability, absence of unauthorized Homepage styling, preserved Contact behavior, Header WhatsApp access, and absence of the obsolete floating WhatsApp presentation.

---

# 24. Visual-Regression Contract

Structural comparison covers layout mode, ordering, columns, component variants, Process and Footer modes, and reserved-visual presence. Visual comparison covers typography, spacing, gutters, surfaces, gradients, translucency, Hero layering, portrait scale, alignment, and background. Functional comparison covers sticky Header, Compact menu, focus, destinations, Header WhatsApp, removal of floating WhatsApp, and fixed noninteractive AI/RAG behavior.

Validation references are 360, 768, 1024, and 1440, supplemented by interpolation probes. Literal pixel equality is not required where browser rendering differs, but structural and perceptual fidelity is mandatory. Snapshot tooling and tolerance remain implementation-validation items.

---

# 25. Acceptance Criteria

| ID | Acceptance criterion |
| --- | --- |
| RWD-AC-001 | One semantic Homepage produces the approved compositions at all four reference widths. |
| RWD-AC-002 | Approved Homepage content and section order are preserved in English and PT-BR. |
| RWD-AC-003 | Homepage Header visibly presents Engineering, Projects, Process, and Contact. |
| RWD-AC-004 | Existing non-Homepage routes remain accessible and their navigation behavior does not regress. |
| RWD-AC-005 | Header is Full at 1024/1440, Compact at 360/768, and transitions at FIT-HDR-001's validated threshold. |
| RWD-AC-006 | Header remains sticky without unintended content or open-menu overlap. |
| RWD-AC-007 | Compact disclosure satisfies naming, state, target, Escape, focus-return, and close-after-navigation requirements. |
| RWD-AC-008 | Hero matches approved stacked/split states and preserves technology/portrait layering without page-global positioning. |
| RWD-AC-009 | Engineering, Projects, Process, Evidence/Contact, and Footer match every approved reference state and preserve source order. |
| RWD-AC-010 | No tested width has page-level horizontal overflow, accidental critical clipping, or hardcoded Figma page height. |
| RWD-AC-011 | AI/RAG visual remains fixed bottom-right, Footer-independent, gutter-aware, and safe-area-aware. |
| RWD-AC-012 | AI/RAG visual is absent from keyboard navigation and exposes no false interactive semantics. |
| RWD-AC-013 | No AI, RAG, retrieval, intelligent search, chat, AI API, or other Release 2 behavior is present. |
| RWD-AC-014 | Sticky Header, open menu, AI/RAG reserved visual, and critical page controls do not collide. |
| RWD-AC-015 | Every FIT candidate completes boundary validation and reaches FIT-VALIDATED before breakpoint finalization. |
| RWD-AC-016 | 390, 480, 640, 820, 900, 1100, and 1280 probes show continuous usable interpolation. |
| RWD-AC-017 | Keyboard access, focus, landmarks, headings, alternative text, contrast, and reduced motion pass validation. |
| RWD-AC-018 | Homepage conforms to FIGMA-04/05 while unrelated routes show no unauthorized visual change. |
| RWD-AC-019 | Images preserve aspect ratio, reserve layout space, and avoid preventable layout shift. |
| RWD-AC-020 | No duplicated breakpoint Homepage, new styling framework, or unnecessary layout JavaScript is introduced. |
| RWD-AC-021 | WhatsApp exists once in the approved Header with its intended destination and behavior; the legacy floating WhatsApp control is absent before AI/RAG reserved-visual acceptance. |

---

# 26. Traceability Matrix

| Authority / decision | Requirements | Engineering decision | Planned implementation area | Planned tests | Acceptance |
| --- | --- | --- | --- | --- | --- |
| C-001 | FR-003–005; NFR-001–003, 012 | route-aware shared Header and preserved routes | base template, navigation include, Homepage anchors, Header CSS/JS | template, route, keyboard, browser | AC-003–007 |
| C-002 | FR-019–021; NFR-004, 015 | presentational fixed overlay with no behavior | template scope, overlay CSS, no handler | semantics, tab order, browser collision | AC-011–014 |
| C-003 | FR-001–002, 008–018, 022–023; NFR-005–014 | Homepage-scoped visual system | Homepage templates, CSS, assets | visual, responsive, route regression | AC-001–002, 008–010, 016–020 |
| HEADER-STICKY | FR-006–007; NFR-002–003, 015 | preserve sticky runtime and layering | Header CSS/JS | scroll, menu, focus, overlap | AC-006–007, 014 |
| WHATSAPP-HEADER-MIGRATION | FR-024; NFR-002–003, 015 | move access to Header and remove legacy floating control | base/navigation templates, Header CSS, legacy overlay removal | destination, uniqueness, absence, responsive Header | AC-014, 021 |
| FIGMA-04 | FR-008–020, 022–023 | protected visual compositions | all Homepage sections | four-width screenshots | AC-001, 008–011, 018 |
| FIGMA-05 | FR-001, 005, 008–020; NFR-006–009 | one intrinsic responsive system | Homepage components and CSS | structural, interaction, interpolation | AC-001, 005, 008–010, 016, 020 |
| Intrinsic-fit protocol | FR-005, 008, 011–018, 022–023; NFR-012, 014 | evidence-based component thresholds | responsive CSS and browser evidence | every FIT boundary in EN/PT-BR | AC-005, 009, 015–016 |
| Reference widths | FR-001–002, 008–020; NFR-005 | validate without treating references as automatic breakpoints | complete Homepage | browser and visual suite | AC-001–002, 008–011 |
| SPEC-001 nonvisual authority | FR-002, 004, 018, 024; NFR-001–003, 011–013 | preserve routes, i18n, accessibility, architecture, and WhatsApp destination | shared templates and routes | full integration regression | AC-002, 004, 017–021 |
| Container evidence | FR-022–023; NFR-005–006 | max-width container and validated gutters | Homepage CSS | geometry at references and probes | AC-001, 010, 016 |
| Hero handoff | FR-008–010; NFR-001, 005, 010 | local artwork coordinate system | Home template, CSS, image assets | layering, overflow, image tests | AC-008, 010, 019 |
| Engineering handoff | FR-011; NFR-005–007 | intrinsic Grid | Engineering component | FIT-ENG and screenshots | AC-009–010, 015 |
| Projects handoff | FR-012; NFR-005–007 | Grid with centered incomplete row | project cards | FIT-PRJ and source-order tests | AC-009–010, 015 |
| Process handoff | FR-013–014; NFR-001, 005–007 | variants without DOM reordering | Process component | FIT-PRC and reading order | AC-009–010, 015, 017 |
| Evidence/Contact handoff | FR-015–017; NFR-005–007 | intrinsic grids and stacked/side composition | Evidence and CTA | FIT-EVD and destination tests | AC-009–010, 015 |
| Footer handoff | FR-018; NFR-011–012 | responsive shared Footer with isolation | Footer include and CSS | FIT-FTR, route, i18n | AC-004, 009, 015, 018 |
| Accessibility baseline | FR-007, 019–021, 024; NFR-001–004, 009–010, 012, 015 | semantic DOM and native controls | templates, CSS, JS | automated and manual keyboard checks | AC-007, 012, 014, 017, 021 |
| Performance/layout stability | NFR-008, 010, 013 | CSS-led layout and responsive assets | image markup, assets, CSS | layout stability and asset inspection | AC-019–020 |

No requirement or acceptance criterion is orphaned. No operative requirement depends on unresolved C-001, C-002, C-003, HEADER-STICKY, or WhatsApp migration authority.

---

# 27. Impact Analysis

| Area | Blast radius | Reason |
| --- | --- | --- |
| Shared Header | HIGH | all routes; route-aware navigation, sticky behavior, Compact interaction, and WhatsApp migration |
| Global `site.css` | HIGH | owns shared layout, Header, Hero, Footer, tokens, and current floating control |
| Shared base template | HIGH | owns shared landmarks and fixed controls |
| Shared Footer | HIGH | all routes; Homepage visual isolation required |
| Existing routes | HIGH | C-001 protects route and navigation availability |
| Homepage template/view | MEDIUM | large route-local composition change |
| i18n | MEDIUM | new content and dual-locale FIT validation |
| Portrait/background assets | MEDIUM | large raster sources require controlled delivery |
| Browser test infrastructure | MEDIUM/HIGH | real-browser FIT and visual regression are not currently demonstrated |
| Backend/data architecture | LOW | no new domain or persistence behavior |

Overall implementation blast radius remains HIGH. Decision certainty does not reduce implementation reach.

---

# 28. Implementation Plan

1. responsive implementation preflight and baseline verification;
2. scoped Homepage foundations, containers, gutters, and semantic sections;
3. Header navigation, sticky preservation, Compact accessibility, and WhatsApp migration;
4. Hero composition;
5. Engineering;
6. Projects;
7. Process;
8. Evidence and Contact;
9. Footer;
10. AI/RAG reserved visual after removal of legacy floating WhatsApp;
11. accessibility, i18n, responsive images, and reduced motion;
12. intrinsic-fit browser measurement;
13. breakpoint finalization or evidence-based consolidation;
14. visual regression and interpolation validation;
15. full regression, lint, type, build, and human acceptance.

---

# 29. Decision Classification

## 29.1 Resolved

Homepage navigation, existing-route preservation, Homepage-specific visual authority, visual-only AI/RAG scope, noninteractive semantics, viewport-fixed positioning, sticky Header preservation, responsive reference states, semantic order, and WhatsApp Header migration are resolved.

## 29.2 Implementation Validation

Exact FIT thresholds, safe threshold consolidation, gutter expression, Hero interpolation, local clipping bounds, overlay stacking details, image formats and derivative widths, snapshot tooling and tolerance, EN/PT-BR worst-case fit, sticky anchor offset, and supported-browser evidence remain implementation-validation work.

## 29.3 Deferred

Functional AI/RAG, retrieval, intelligent search, AI backend/API/chat, Analytics, advanced SEO, numerical performance budgets, broader design-system refactoring, site-wide redesign, and unrelated-route adoption of Homepage tokens are deferred.

---

# 30. Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| Homepage Header changes regress other routes | High | route-aware rendering and non-Homepage regression suite |
| Global tokens redesign unrelated pages | High | Homepage-scoped tokens and selector boundaries |
| Release 1 floating WhatsApp is not fully removed during Header migration | High | verify Header access, intended destination, uniqueness, and legacy floating-control absence before AI/RAG acceptance |
| Static references become arbitrary breakpoints | High | mandatory FIT lifecycle |
| Hero artwork causes overflow or inaccessible order | High | local positioning context, semantic DOM, boundary tests |
| PT-BR breaks English-validated layouts | High | dual-locale FIT validation |
| CSS-source tests provide false confidence | Medium | real-browser tests and visual validation |
| Large raster assets degrade delivery or stability | Medium | responsive formats, dimensions, and layout reservation |
| Sticky Header conceals anchors or focus | Medium | scroll-offset and focus tests |
| Excessive thresholds increase complexity | Medium | evidence-based consolidation after individual validation |
| Footer changes propagate globally | High | shared-component regression and scoped treatment |
| Reserved visual appears actionable | High | presentational semantics, no focus, no handlers, and accessibility review |

No risk constitutes a new normative blocker.

---

# 31. Delivery Status

| Deliverable | Status |
| --- | --- |
| FIGMA-04 — Homepage Responsive | COMPLETE / HUMAN APPROVED |
| FIGMA-05 — Responsive Design Consolidation and Implementation Handoff | COMPLETE / HUMAN APPROVED |
| SDD-RWD-001 | COMPLETE / HUMAN APPROVED / PERSISTED |
| Homepage Responsive Implementation | READY / NOT STARTED |
| Intrinsic-Fit Validation | PENDING IMPLEMENTATION |
| Responsive Browser Validation | PENDING |
| Responsive Visual Regression | PENDING |
| Responsive Implementation Acceptance | PENDING |

Task sequence:

* [COMPLETE] Responsive visual design — 1440
* [COMPLETE] Responsive visual design — 1024
* [COMPLETE] Responsive visual design — 768
* [COMPLETE] Responsive visual design — 360
* [COMPLETE] Responsive design consolidation / FIGMA-05
* [COMPLETE] Responsive implementation specification / SDD-RWD-001
* [PENDING] Responsive implementation preflight
* [PENDING] Responsive foundations/container implementation
* [PENDING] Header migration and responsive implementation
* [PENDING] Hero responsive implementation
* [PENDING] Engineering responsive implementation
* [PENDING] Projects responsive implementation
* [PENDING] Process responsive implementation
* [PENDING] Evidence/Contact responsive implementation
* [PENDING] Footer responsive implementation
* [PENDING] AI/RAG reserved visual runtime implementation
* [PENDING] Intrinsic-fit browser validation
* [PENDING] Breakpoint finalization
* [PENDING] Accessibility validation
* [PENDING] Responsive visual regression
* [PENDING] Full regression/build validation
* [PENDING] Human implementation acceptance

---

# 32. Approval and Phase Boundary

SDD-RWD-001 is human approved and persisted as the normative responsive implementation specification for Release 1.1 preparation.

Implementation remains **NOT STARTED**. All FIT entries remain **FIT-CANDIDATE**. The next permitted stage is Homepage Responsive Implementation — Phase 0 / Preflight. That stage shall inspect this specification, the current production implementation, affected files, test baseline, protected working-tree state, and implementation blast radius before production mutation.

**SDD-RWD-001 — PERSISTED / BASELINED — READY FOR RESPONSIVE IMPLEMENTATION PREFLIGHT**

---

## Current implementation-status addendum — 2026-08-22

The baseline status above records the specification's approval-time state and
remains historical. Blocks 1–12 are complete and human approved. Block 13
breakpoint finalization is complete pending human review, and all 13 intrinsic
FIT entries are now FIT-VALIDATED. Block 13 evidence is persisted in
`docs/validation/SDD-RWD-001-block13-breakpoint-validation.md`. Block 14 visual
regression/interpolation and final human acceptance remain pending.

Block 14 visual regression and interpolation validation subsequently completed
pending human review. Technical responsive implementation is complete, all 13
FIT decisions remain FIT-VALIDATED, and final human acceptance remains pending.
Evidence is persisted in
`docs/validation/SDD-RWD-001-block14-visual-regression.md`.
