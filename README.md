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
- **SPEC-001 — MVP Foundation, Phase 1 (Project Bootstrap and Django Foundation):**
  - Implementation: **complete** — uv toolchain, Django project with split settings, approved modular apps, frontend and test scaffolding
  - Runtime and toolchain validation: **passed** (Python 3.13.14, Django 5.2.17, PostgreSQL 18.4, uv)
  - Django validation: **passed** (`manage.py check` — no issues)
  - PostgreSQL local connectivity: **passed** (localhost:5432, database `luis_franca_portfolio`)
  - Migrations: **passed**
  - Automated tests: **passed** (pytest — 2 passed)
  - Ruff: **passed**
  - mypy: **passed** (no issues in 60 source files)
  - Final acceptance: **approved**
  - Phase 1 status: **closed**
- **SPEC-002 — Contact & Communication (Phase 2):**
  - Implementation: **complete** — contact and quotation form, transactional email notification (Brevo SMTP per ADR-004), persistence with retention policy, controlled success/failure confirmation, floating WhatsApp entry point
  - Automated tests: **passed** (pytest)
  - Status: **implemented and validated**
- **SPEC-003 — Portfolio & Projects:**
  - Implementation: **complete** — dedicated Portfolio section, three featured projects using the approved Product Owner data, reusable project cards, hover elevation, screenshot scrolling, responsive 3/2/1-column layout, Release 1 project screenshot assets
  - Automated tests: **passed** (pytest — 92 passed)
  - Status: **implemented and validated** — Product Owner acceptance and integration approval pending
- Per the approved release strategy and specification sequence, the next Feature Specification is eligible for planning once the current increment is reviewed and authorized.

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

## Development Setup

The Python toolchain is managed by `uv` (ADR-003):

```sh
uv sync                                  # create .venv and install dependencies
uv run python backend/manage.py runserver
uv run pytest                            # test suite (from repository root)
uv run ruff check                        # lint
uv run mypy -p config -p apps            # static type checking
uv run mypy tests
```

Run `make help` for repository health-check targets (`check-structure`, `check-docs`,
`check-names`, `check-secrets`).
