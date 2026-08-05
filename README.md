# Luis França Portfolio

Repository slug: `luis-franca-portfolio`

Personal professional portfolio of Luís Eduardo Carvalho França (Software Engineer).
The engineering documents refer to this project as **Site Portfolio**.

## Governance

This repository is governed by an approved engineering baseline (Specification-Driven Development).
The normative engineering documentation is maintained under `docs/`:

- Engineering Generation Standard — `docs/00-engineering-generation-standard.md`
- Product Brief — `docs/01-product-brief.md`
- Technical Specification — `docs/02-technical-specification.md`
- Software Architecture — `docs/03-architecture.md`
- API and Data Contracts — `docs/04-api-and-data-contracts.md`
- Testing and Acceptance — `docs/05-testing-and-acceptance.md`
- Deployment and Operations — `docs/06-deployment-and-operations.md`
- Architectural Decision Records — `docs/adr/`
- Feature Specifications and Engineering Baseline — `docs/specs/`

The approved engineering baseline is certified by `docs/specs/BASELINE-001.md`.

## Approved Technology Stack

Per `docs/adr/ADR-002-technology-stack.md`:

- Backend: Python + Django
- Frontend: Django Templates + HTMX (minimal vanilla JavaScript)
- Database: PostgreSQL (development and production)
- Architecture: Modular Monolith
- Hosting: Hostinger VPS
- Internationalization: Django i18n — English (default) and Brazilian Portuguese

## Development Status

- Engineering Documentation baseline: **Approved** (BASELINE-001)
- Implementation phase: **Initiated** — repository structure and Git baseline established
- Next implementation activity: **SPEC-001 — MVP Foundation** (not yet started)

## Repository Structure

```
├── backend/      Django application (content defined by SPEC-001)
├── frontend/     Presentation assets (Django Templates + HTMX per ADR-002)
├── docs/         Approved engineering baseline
├── scripts/      Operational scripts (content per 06-deployment-and-operations.md)
├── docker/       Container artifacts (deferred until runtime is approved)
├── nginx/        Reverse proxy artifacts (deferred until proxy is approved)
├── .github/      CI workflows (deferred until CI is defined)
└── tests/        Test suite (content per 05-testing-and-acceptance.md)
```

## Local Setup Entry Points

Authoritative local development and deployment guidance is defined in:

- `docs/03-architecture.md` — architecture and module organization
- `docs/06-deployment-and-operations.md` — environment model and configuration
- `docs/adr/ADR-002-technology-stack.md` — approved stack and constraints
- `docs/specs/SPEC-001-mvp-foundation.md` — first implementation scope

Environment configuration is environment-based and external to source code.
Copy `.env.example` to `.env` for local values; never commit real secrets.
