# ADR-003 — Python Runtime and Development Toolchain

| Field | Value |
|---|---|
| **Document ID** | ADR-003 |
| **Decision ID** | ARCH-DEC-003 |
| **Title** | Python Runtime and Development Toolchain |
| **Version** | 1.1.0 |
| **Status** | Approved Baseline |
| **Decision Status** | Accepted |
| **Decision Classification** | Strategic Runtime and Engineering Toolchain Decision |
| **Project** | Site Portfolio |
| **Release** | Release 1 — MVP |
| **Owner** | Solution Architecture |
| **Approver** | Product Owner |
| **Development Model** | Specification-Driven Development (SDD) |
| **Created** | 2026-08-05 |
| **Last Updated** | 2026-08-14 |

---

# 1. Purpose

This Architectural Decision Record establishes the authoritative runtime, dependency management, dependency locking, PostgreSQL driver, development toolchain, and engineering bootstrap policies for the Site Portfolio project.

This ADR closes the runtime and engineering-toolchain decision gap identified after approval of the Release 1 Engineering Documentation Baseline.

The decisions established herein are normative for Release 1 and shall govern:

- local development;
- automated verification;
- Continuous Integration environments when introduced;
- testing environments;
- staging;
- production deployment;
- dependency maintenance;
- engineering bootstrap;
- future Release 1 maintenance activities.

This ADR complements **ADR-002 — Technology Stack**.

It shall not replace, redefine, or supersede the technology selections established by ADR-002.

---

# 2. Normative Authority

This ADR derives its authority from:

- EGS-001 — Engineering Generation Standard;
- PB-001 — Product Brief;
- TS-001 — Technical Specification;
- ARCH-001 — Software Architecture;
- ADR-001 — Release Strategy;
- ADR-002 — Technology Stack;
- BASELINE-001 — Engineering Documentation Baseline.

Within the project engineering hierarchy, this ADR refines the approved architecture by defining runtime and engineering-toolchain decisions required to implement and operate the approved technology stack.

No implementation artifact, local environment, deployment procedure, automation, or engineering convention shall contradict the decisions established herein.

A deviation from this ADR requires controlled engineering review and, when materially architectural, an approved superseding ADR or approved revision of this document.

---

# 3. Context

The approved engineering baseline establishes:

- Python as the primary backend language;
- Django as the primary web framework;
- PostgreSQL as the authoritative relational database;
- a Modular Monolith architecture;
- Specification-Driven Development;
- environment-based configuration;
- automated verification whenever practical;
- reproducible deployment and operational procedures.

The baseline did not originally establish:

- the supported Python release line;
- the supported Django release line;
- the dependency management mechanism;
- dependency locking policy;
- PostgreSQL driver policy;
- official quality and development tooling;
- deterministic engineering bootstrap;
- version-update governance.

Allowing these decisions to originate informally during implementation would violate the project's requirements for explicitness, reproducibility, traceability, maintainability, and controlled architectural evolution.

ADR-003 therefore establishes these policies as explicit architectural decisions.

---

# 4. Problem Statement

Release 1 requires an engineering environment that can be reproduced consistently across development, verification, staging, and production.

Without an authoritative runtime and toolchain policy, the project would permit uncontrolled variation in:

- Python versions;
- Django versions;
- dependency resolution;
- virtual environments;
- PostgreSQL drivers;
- test tooling;
- static-analysis tooling;
- linting and formatting;
- dependency installation;
- deployment environments.

Such variation would compromise:

- deterministic dependency resolution;
- test reproducibility;
- architecture compliance;
- operational consistency;
- security maintenance;
- deployment reliability;
- engineering traceability.

The project shall therefore maintain one controlled runtime and engineering-toolchain baseline.

---

# 5. Decision Drivers

## DD-001 — Governance Compliance

Runtime and toolchain decisions shall comply with EGS-001 and the approved Release 1 engineering baseline.

Implementation shall not independently redefine architectural tooling decisions.

## DD-002 — Reproducibility

Equivalent engineering inputs shall produce equivalent dependency environments whenever practical.

Engineering setup shall not depend on undocumented local state.

## DD-003 — Simplicity

The project shall use the smallest toolchain that fully satisfies implementation, verification, and deployment requirements.

Parallel tools serving equivalent responsibilities shall not be introduced without justified engineering need.

## DD-004 — Maintainability

Runtime and dependency policies shall support controlled maintenance and predictable upgrades.

## DD-005 — Security

Dependency acquisition, configuration, and maintenance shall minimize supply-chain and configuration risk.

Secrets shall remain outside source control.

## DD-006 — Testability

The toolchain shall support the verification and acceptance activities defined by TST-001.

## DD-007 — Operational Consistency

Development, testing, staging, and production shall operate under compatible runtime and dependency assumptions.

---

# 6. Alternatives Considered

## 6.1 Alternative A — Leave Runtime and Tooling Undefined

### Decision

Rejected.

### Rationale

This alternative would permit environment divergence, undocumented implementation decisions, non-deterministic installations, and broken engineering traceability.

---

## 6.2 Alternative B — Expand ADR-002

### Decision

Rejected.

### Rationale

ADR-002 governs technology selection.

Runtime lifecycle, dependency locking, bootstrap, and quality-tool configuration constitute separate engineering responsibilities and shall remain independently governed.

---

## 6.3 Alternative C — Dedicated Runtime and Toolchain ADR

### Decision

Accepted.

### Rationale

A dedicated ADR preserves separation of responsibilities while establishing explicit and independently evolvable runtime and engineering-toolchain governance.

---

# 7. Architectural Decision

The Site Portfolio project shall use one standardized Python runtime line, one dependency-management workflow, one deterministic dependency lock, one PostgreSQL driver family, and one approved engineering toolchain throughout Release 1.

The following decisions are mandatory:

- Python 3.13 release line;
- Django 5.2 release line;
- `uv` for Python runtime and dependency management;
- `pyproject.toml` for project metadata and compatible dependency declarations;
- `uv.lock` for deterministic resolved dependency state;
- Psycopg 3 for PostgreSQL connectivity;
- pytest-based automated testing;
- Ruff for linting, formatting, and import organization;
- mypy for static type analysis;
- django-stubs for Django-aware static analysis.

Alternative runtime versions, dependency managers, PostgreSQL drivers, or overlapping engineering tools shall not be introduced without approved engineering review.

---

# 8. Python Runtime Policy

## 8.1 Approved Runtime

The supported Python runtime shall be:

```text
>=3.13,<3.14
```

Python 3.13 is the authoritative minor release line for Release 1.

The project shall not depend on another Python major or minor version.

## 8.2 Patch-Level Evolution

Compatible Python 3.13 patch updates may be adopted through normal controlled maintenance.

A patch update shall require:

- dependency compatibility verification;
- automated test execution;
- static-analysis verification;
- application system checks;
- operational validation where the update affects deployed environments.

A patch update shall not require a new ADR unless it introduces a material incompatibility or architectural consequence.

## 8.3 Minor or Major Runtime Changes

Migration outside the Python 3.13 release line shall require:

- architecture review;
- compatibility analysis;
- dependency validation;
- regression verification;
- deployment impact analysis;
- Product Owner approval;
- an approved revision or superseding ADR where required.

## 8.4 Runtime Declaration

The supported Python range shall be declared in `pyproject.toml`.

Undocumented interpreter selection shall not constitute an approved project runtime.

---

# 9. Django Release Policy

## 9.1 Approved Framework Line

The supported Django runtime shall be:

```text
>=5.2,<5.3
```

Release 1 shall remain on the Django 5.2 release line.

## 9.2 Compatibility

Django updates within the approved release line shall preserve compatibility with:

- Python 3.13;
- Psycopg 3;
- approved application behavior;
- migrations;
- automated tests;
- deployment configuration.

## 9.3 Framework Evolution

Migration outside the Django 5.2 release line shall require architectural evaluation.

A framework migration shall not occur solely through dependency-file modification.

---

# 10. Dependency Management Policy

## 10.1 Approved Dependency Manager

The official dependency and runtime management tool shall be:

```text
uv
```

`uv` shall be responsible for:

- runtime acquisition where required;
- virtual environment management;
- dependency resolution;
- dependency installation;
- dependency synchronization;
- lockfile generation and validation;
- execution within the managed environment.

The project shall not maintain a parallel dependency-management workflow for the same Python application environment.

## 10.2 Project Metadata

`pyproject.toml` shall be the authoritative source for:

- project metadata;
- supported Python range;
- direct runtime dependencies;
- development dependency groups;
- compatible dependency ranges;
- engineering-tool configuration where supported.

## 10.3 Dependency Introduction

A dependency shall be introduced only when justified by an approved implementation or engineering requirement.

Dependencies shall be evaluated for:

- necessity;
- compatibility;
- maintainability;
- security;
- testability;
- operational impact;
- architectural impact.

Dependencies shall not be introduced solely for speculative future functionality.

## 10.4 Runtime and Development Dependencies

Runtime dependencies and development-only dependencies shall remain logically separated.

Production behavior shall not depend on tooling required exclusively for development or verification.

---

# 11. Dependency Lock Strategy

## 11.1 Authoritative Dependency Artifacts

The authoritative Python dependency artifacts shall be:

```text
pyproject.toml
uv.lock
```

Their responsibilities are distinct.

### `pyproject.toml`

Defines architectural and project compatibility intent.

### `uv.lock`

Defines the resolved dependency graph used for deterministic installations.

Both files shall remain version controlled.

## 11.2 Locked Synchronization

CI, staging, production, and release-validation environments shall use the committed lockfile.

A deployment or verification workflow shall not silently resolve a dependency graph different from the committed lock state.

## 11.3 Lockfile Changes

A change to `uv.lock` shall be intentional and reviewable.

A lockfile update shall require:

1. controlled dependency resolution;
2. compatibility verification;
3. automated testing;
4. static-analysis verification;
5. Django/application validation where applicable;
6. review of material security or architectural consequences;
7. version-control commit.

Unreviewed dependency upgrades are prohibited.

## 11.4 Artifact Consistency

`pyproject.toml` and `uv.lock` shall remain mutually consistent.

A repository state in which declared dependency intent and the committed lockfile disagree shall not be considered release-ready.

---

# 12. PostgreSQL Driver Policy

## 12.1 Approved Driver

The project shall use Psycopg 3.

The approved dependency compatibility policy shall be:

```text
psycopg[binary]>=3.2,<4
```

## 12.2 Integration Boundary

Psycopg shall be consumed through Django's PostgreSQL database backend.

The driver shall not become an application-domain abstraction or direct business dependency.

## 12.3 Database Access

Django ORM shall remain the default persistence interface, consistent with ARCH-001.

Raw SQL shall be used only where permitted by ARCH-001 and justified by an actual engineering requirement.

## 12.4 Driver Replacement

An additional or replacement PostgreSQL driver shall require architectural evaluation and approval.

---

# 13. Development and Verification Toolchain

## 13.1 Automated Testing

The approved automated testing toolchain shall include:

```text
pytest
pytest-django
pytest-cov
```

These tools shall support the applicable unit, integration, functional, regression, and acceptance verification defined by TST-001 and Feature Specifications.

## 13.2 Static Type Analysis

The approved static-analysis tool shall be:

```text
mypy
```

Static type verification shall form part of the engineering verification workflow where configured by the repository baseline.

## 13.3 Django Type Support

The approved Django typing extension shall be:

```text
django-stubs
```

Its configuration shall remain compatible with the project's approved Django settings structure.

## 13.4 Linting, Formatting, and Imports

The approved code-quality tool shall be:

```text
Ruff
```

Ruff shall provide the repository's configured responsibilities for:

- linting;
- formatting where configured;
- import organization;
- enforceable code-quality rules.

An overlapping formatter or linter shall not be added without demonstrated engineering benefit and controlled review.

## 13.5 Tool Configuration

Engineering-tool configuration shall be centralized in `pyproject.toml` whenever supported and when doing so preserves clarity.

Duplicated configuration shall be avoided.

---

# 14. Engineering Bootstrap Policy

## 14.1 Reproducible Bootstrap

An engineering environment shall be reproducible from:

- version-controlled source code;
- approved engineering documentation;
- `pyproject.toml`;
- `uv.lock`;
- documented environment configuration.

Undocumented manual dependency installation shall not be required.

## 14.2 Environment Isolation

Project dependencies shall execute within an isolated project environment.

Globally installed Python packages shall not constitute project dependencies.

## 14.3 Environment-Specific Configuration

Runtime dependencies shall remain reproducible across environments, while environment-specific operational values shall remain externally configured in accordance with AR-009, SEC-003, ES-005, and OPS-001.

Runtime reproducibility shall not require production secrets to exist in source control.

## 14.4 Bootstrap Verification

An engineering bootstrap shall not be considered valid solely because dependencies install successfully.

Applicable verification shall include:

- dependency consistency;
- Django system checks;
- automated testing;
- lint/static-analysis gates defined by the repository;
- documentation/repository health checks where applicable.

---

# 15. Environment Consistency

The same approved runtime compatibility policy shall apply to:

- development;
- testing;
- CI;
- staging;
- production.

Environment-specific differences shall be limited to legitimate operational configuration, platform characteristics, or approved deployment concerns.

An environment shall not introduce a different Python minor release, Django release line, dependency graph, or PostgreSQL driver without approved engineering justification.

Patch-level runtime or dependency differences shall be controlled and shall not invalidate deterministic release behavior.

---

# 16. Version Update and Change-Control Policy

## 16.1 Controlled Evolution

Runtime, framework, driver, dependency-manager, and engineering-tool versions shall evolve through controlled changes.

Updates shall not be performed solely because a newer version exists.

## 16.2 Evaluation Criteria

Version changes shall evaluate:

- compatibility;
- security impact;
- regression risk;
- architecture impact;
- deployment impact;
- operational complexity;
- maintenance benefit.

## 16.3 Material Changes

The following changes are material and shall require Architecture & Engineering Review:

- Python minor or major release change;
- Django release-line change;
- dependency-manager replacement;
- dependency-locking strategy change;
- PostgreSQL driver replacement;
- replacement of core testing or static-analysis tooling.

Where such a change alters an approved architectural decision, an approved ADR revision or superseding ADR is required.

## 16.4 Security Maintenance

Urgent security updates may use the emergency-change provisions of OPS-001.

Emergency handling shall not permanently bypass documentation, verification, traceability, or post-change validation requirements.

---

# 17. Security Requirements

Runtime and dependency management shall preserve the project's security baseline.

The following requirements are mandatory:

- secrets shall not be stored in `pyproject.toml` or `uv.lock`;
- local secret files shall not be committed;
- dependency changes shall remain reviewable;
- unnecessary dependencies shall not be introduced;
- production configuration shall remain environment-based;
- engineering tools shall not require production credentials for normal validation;
- sensitive configuration shall remain outside source-controlled implementation artifacts.

Dependency locking improves reproducibility but shall not be treated as a substitute for dependency-security review.

---

# 18. Verification and Quality Gates

Compliance with this ADR shall be objectively verifiable.

Applicable verification evidence shall include:

- supported Python runtime declaration;
- supported Django dependency range;
- Psycopg 3 dependency declaration;
- committed `uv.lock`;
- successful locked dependency synchronization;
- successful automated tests;
- successful Ruff checks according to repository configuration;
- successful mypy checks according to repository configuration;
- successful Django system checks;
- successful canonical-document and repository-governance checks where defined.

Failure of a mandatory verification gate shall prevent the affected increment from being considered release-ready.

This ADR does not replace TST-001.

Testing and acceptance remain governed by TST-001.

---

# 19. Operational Requirements

Deployment and Operations shall preserve the runtime and dependency policies defined by this ADR.

Production deployment shall:

- use the approved Python release line;
- use a dependency environment derived from the committed project artifacts;
- avoid uncontrolled dependency resolution;
- preserve environment-based configuration;
- maintain separation between source-controlled configuration definitions and production secrets;
- support deterministic restoration of the approved application dependency state.

This ADR does not define infrastructure installation commands, service-management commands, or release runbooks.

Those responsibilities remain governed by OPS-001 and approved operational procedures.

---

# 20. Consequences

## 20.1 Positive Consequences

The decision provides:

- deterministic dependency management;
- controlled runtime compatibility;
- consistent engineering environments;
- explicit dependency governance;
- reproducible testing;
- reduced tooling fragmentation;
- clear upgrade boundaries;
- improved deployment reproducibility;
- explicit engineering traceability.

## 20.2 Negative Consequences

The decision introduces:

- controlled constraints on runtime and framework upgrades;
- mandatory lockfile maintenance;
- required validation before dependency changes;
- governance overhead for material toolchain substitutions.

These consequences are accepted because they preserve Release 1 correctness, reproducibility, and maintainability.

---

# 21. Requirement and Decision Traceability

This ADR maintains traceability to the approved engineering baseline.

## 21.1 Business Requirements

Applicable business requirements include:

- BR-005 — support future business expansion;
- BR-006 — provide an excellent user experience across supported devices;
- BR-008 — preserve long-term product evolution without architectural redesign.

## 21.2 Technical Requirements

Applicable requirements include:

- TR-001 — preserve engineering traceability;
- TR-002 — require approved specification before implementation;
- TR-004 — preserve modular evolution;
- TR-005 — synchronize documentation and implementation;
- TR-006 — ensure independent testability;
- TR-007 — incorporate security by default;
- TR-008 — prioritize engineering quality;
- NFR-003 — maintainability;
- NFR-008 — portability;
- NFR-009 — extensibility;
- SEC-003 — environment-based sensitive configuration;
- SEC-005 — secure dependency management;
- SEC-006 — secure defaults;
- ES-002 — version-controlled engineering documentation;
- ES-005 — environment-based configuration;
- ES-006 — automated verification whenever feasible;
- ES-009 — implementation consistency with architecture.

## 21.3 Architecture Requirements

Applicable architecture requirements include:

- AR-001 — Modular Monolith;
- AR-004 — Single Deployable Application;
- AR-005 — Relational Persistence;
- AR-009 — Environment-Based Configuration;
- AR-010 — Controlled Architectural Evolution.

## 21.4 Architectural Decisions

This ADR:

- implements and refines ADR-002;
- remains consistent with ADR-001;
- is referenced by ADR-004 where runtime and engineering-toolchain policy applies;
- does not supersede ADR-001, ADR-002, or ADR-004.

## 21.5 Downstream Artifacts

The following artifacts shall conform to this ADR where applicable:

- `pyproject.toml`;
- `uv.lock`;
- dependency bootstrap procedures;
- testing configuration;
- CI configuration;
- staging configuration;
- production dependency provisioning;
- SPEC-001 implementation;
- SPEC-002 implementation;
- SPEC-003 implementation;
- operational release procedures.

---

# 22. Cross-Document References

This ADR shall be interpreted together with:

- EGS-001 — Engineering Generation Standard;
- PB-001 — Product Brief;
- TS-001 — Technical Specification;
- ARCH-001 — Software Architecture;
- ADC-001 — API and Data Contracts;
- TST-001 — Testing and Acceptance;
- OPS-001 — Deployment and Operations;
- ADR-001 — Release Strategy;
- ADR-002 — Technology Stack;
- ADR-004 — Transactional Email Integration;
- SPEC-001 — MVP Foundation;
- SPEC-002 — Contact & Communication;
- SPEC-003 — Portfolio & Projects;
- BASELINE-001 — Engineering Documentation Baseline.

No lower-authority implementation artifact shall redefine the policies established herein.

---

# 23. Cross-Document Reconciliation

The reconciliation represented by version 1.1.0 resolves the governance inconsistency present in ADR-003 version 1.0.0.

The following corrections are normative:

1. the document status is reconciled from the historical `Proposed` state to `Approved Baseline`;
2. the decision status is explicitly recorded as `Accepted`;
3. conditional future-approval language is removed;
4. mandatory decisions use normative `shall`, `shall not`, and `requires` language;
5. the document receives explicit Decision ID `ARCH-DEC-003`;
6. runtime, dependency, tooling, security, operational, and verification responsibilities are explicitly bounded;
7. `pyproject.toml` and `uv.lock` responsibilities are formally separated;
8. compatibility with TST-001 and OPS-001 is explicit;
9. ADR-004 is incorporated into the cross-document relationship model;
10. implementation and repository evidence are treated as validation of the decision rather than as the source of the decision.

No technology selection is changed by this reconciliation.

No business requirement, Feature Specification, API contract, deployment topology, or Release 1 functional scope is modified.

---

# 24. Compliance

This ADR complies with:

- EGS-001 — Engineering Generation Standard;
- Specification-Driven Development;
- approved Project Governance;
- PB-001;
- TS-001;
- ARCH-001;
- ADC-001;
- TST-001;
- OPS-001;
- ADR-001;
- ADR-002;
- ADR-004;
- approved Release 1 Feature Specifications.

The reconciliation has been evaluated for:

- normative authority;
- responsibility boundaries;
- canonical terminology;
- mandatory-language consistency;
- architectural consistency;
- traceability;
- implementation independence;
- testing compatibility;
- operational compatibility;
- controlled evolution.

No architectural conflict is introduced.

---

# 25. Future Review Triggers

This ADR shall be reviewed when any of the following occurs:

- Python release-line replacement;
- Django release-line replacement;
- dependency-manager replacement;
- dependency-locking strategy replacement;
- PostgreSQL driver replacement;
- material engineering-toolchain replacement;
- substantial CI/runtime architecture change;
- revised architecture that invalidates assumptions in this ADR;
- revised EGS or higher-authority baseline affecting its normative scope.

---

# 26. Supersession Policy

This ADR remains authoritative until:

- superseded by an approved Architectural Decision Record;
- superseded by an approved revision of this ADR;
- formally retired through the controlled lifecycle established by EGS-001.

An implementation change shall not implicitly supersede this ADR.

---

# 27. Approval Statement

ADR-003 version 1.1.0 constitutes the approved architectural decision governing the Python runtime, dependency management, dependency locking, PostgreSQL driver, development toolchain, and engineering bootstrap policies for Release 1.

The Product Owner approval establishes that:

- Python 3.13 is the approved runtime release line;
- Django 5.2 is the approved framework release line;
- `uv` is the approved dependency and runtime management solution;
- `pyproject.toml` and `uv.lock` are the authoritative dependency-management artifacts;
- Psycopg 3 is the approved PostgreSQL driver;
- pytest, Ruff, mypy, and django-stubs constitute the approved engineering verification toolchain;
- material deviations require controlled engineering approval.

All Release 1 implementation, verification, staging, production deployment, and maintenance activities shall comply with this ADR while it remains in Approved Baseline status.

---

# 28. Document Status

| Field | Value |
|---|---|
| Document ID | ADR-003 |
| Decision ID | ARCH-DEC-003 |
| Version | 1.1.0 |
| Status | **Approved Baseline** |
| Decision Status | **Accepted** |
| Classification | Architectural Decision Record |
| Authority | Release 1 Engineering Baseline |
| Applies To | Release 1 — MVP |
| Next Review | Upon a material runtime, framework, dependency-management, driver, or toolchain change |

---

# 29. Revision History

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0.0 | 2026-08-05 | Proposed | Initial ADR defining Python runtime, Django release line, `uv`, dependency locking, Psycopg 3, development tooling, bootstrap, and update policies. |
| 1.1.0 | 2026-08-14 | Approved Baseline | Governance reconciliation. Resolved inconsistent Proposed/mandatory status, established `ARCH-DEC-003`, normalized normative language, formalized approval and authority, strengthened traceability, verification, operational boundaries, security, dependency governance, and alignment with ADR-004 and the implemented Release 1 baseline. |

---

# 30. Final Normative Provision

ADR-003 establishes the authoritative Release 1 runtime and engineering-toolchain baseline.

All affected engineering and implementation artifacts shall remain consistent with this decision.

Runtime versions, framework versions, dependency management, locking, PostgreSQL driver selection, and core engineering tooling shall not evolve through undocumented implementation changes.

Material changes shall follow:

**Requirement → Impact Analysis → Architecture Review → Decision → Implementation → Verification → Validation → Approval → Release**

No deviation from this ADR shall be considered approved unless processed through the controlled engineering governance established by EGS-001.

---

# End of Document