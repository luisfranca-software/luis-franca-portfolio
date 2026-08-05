# **Site Portfolio**

# **Software Architecture**

**Document ID:** ARCH-001  
**Version:** 2.0.0  
**Status:** Approved Baseline  
**Project:** Site Portfolio  
**Owner:** Architecture & Engineering Review  
**Approver:** Product Owner  
**Development Model:** Specification-Driven Development (SDD)  
**Normative Authority:** Software Architecture  
**Last Updated:** 2026-08-02

---

# **1\. Document Control**

## **1.1 Purpose**

This document establishes the official software architecture baseline for the Site Portfolio project.

It defines the approved architectural style, system decomposition, logical boundaries, technology baseline, dependency rules, data architecture, integration boundaries, security architecture, deployment topology, operational characteristics, and controlled evolution model.

This document translates the approved business and technical baselines into architectural structures and constraints that shall govern downstream engineering artifacts and implementation activities.

The architecture defined herein is normative.

Implementation shall conform to this architecture unless a specific architectural decision is formally superseded by an approved Architectural Decision Record or by an approved revision of this document.

---

## **1.2 Document Scope**

This document governs:

* architectural style;  
* system structure;  
* logical layers;  
* application modules;  
* dependency direction;  
* technology baseline;  
* data architecture;  
* integration architecture;  
* security architecture;  
* deployment architecture;  
* operational architecture;  
* architecture evolution;  
* architectural constraints;  
* architectural traceability.

This document intentionally excludes:

* business requirements;  
* product priorities;  
* detailed functional behavior;  
* page-level requirements;  
* user interface specifications;  
* API payload definitions;  
* database schema details;  
* implementation tasks;  
* source code;  
* test case implementation;  
* deployment procedures.

Those responsibilities belong to their respective engineering documents.

---

## **1.3 Intended Audience**

This document is intended for:

* Product Owner;  
* Architecture & Engineering Review;  
* Solution Architect;  
* Software Engineers;  
* Quality Engineering;  
* DevOps and Operations Engineering;  
* future project maintainers.

---

## **1.4 Document Responsibility Boundary**

This document defines **how the system is structurally organized**.

It shall not redefine:

* business intent established by the Product Brief;  
* project-wide technical requirements established by the Technical Specification;  
* detailed contracts defined by API and Data Contract documentation;  
* validation procedures defined by Testing and Acceptance documentation;  
* feature behavior defined by Feature Specifications;  
* implementation details contained in source code.

Architectural content shall remain at system-design level.

Implementation-specific decisions shall be delegated to Feature Specifications or implementation artifacts unless they materially affect the architecture.

---

# **2\. Normative Authority**

This Software Architecture derives its authority from:

* Engineering Generation Standard;  
* Project Governance;  
* approved Product Brief;  
* approved Technical Specification.

Within the project documentation hierarchy, this document occupies the Software Architecture level.

The normative hierarchy is:

Engineering Generation Standard (EGS)

↓

Project Governance

↓

Product Brief

↓

Technical Specification

↓

Software Architecture

↓

Architectural Decision Records

↓

API and Data Contracts

↓

Testing and Acceptance

↓

Deployment and Operations

↓

Feature Specifications

↓

Implementation

This document shall not contradict any higher-authority baseline.

Every lower-authority engineering artifact shall conform to the architectural rules, boundaries, constraints, and decisions defined herein.

An Architectural Decision Record may refine or supersede a specific architectural decision only when:

* the affected decision is explicitly identified;  
* technical justification is documented;  
* impact analysis is completed;  
* cross-document consistency is verified;  
* Product Owner approval is obtained.

An ADR shall not supersede the entire architecture baseline.

---

# **3\. Normative Compliance**

This document has been prepared according to the Engineering Generation Standard and the complete Specification Engineering lifecycle.

Compliance has been reviewed against:

* Engineering Generation Standard;  
* Project Governance;  
* Specification-Driven Development;  
* approved Product Brief;  
* approved Technical Specification;  
* Documentation Quality Assurance requirements;  
* approved engineering baselines.

The compliance review covers:

* canonical terminology;  
* normative authority;  
* scope ownership;  
* responsibility separation;  
* architectural traceability;  
* consistency with business requirements;  
* consistency with technical requirements;  
* absence of implementation leakage;  
* architectural completeness;  
* controlled document evolution.

---

# **4\. Source Baselines**

The architecture defined in this document originates from approved higher-authority baselines.

| Source Document | Architectural Role |
| ----- | ----- |
| `00-engineering-generation-standard.md` | Governs document generation, authority, traceability, quality assurance, lifecycle, and approval |
| `01-product-brief.md` | Defines approved business intent, product scope, business constraints, and roadmap |
| `02-technical-specification.md` | Defines project-wide technical requirements, non-functional requirements, engineering principles, security baseline, integration baseline, and technical constraints |

Architectural decisions shall be traceable to one or more requirements contained in these source baselines.

Informal discussions, implementation preferences, or undocumented assumptions shall not constitute valid architectural authority.

---

# **5\. Architecture Purpose**

The architecture shall provide a stable, maintainable, secure, and evolvable foundation capable of supporting:

* Release 1 — Professional Portfolio MVP;  
* approved Release 1.1 improvements;  
* planned Release 2 capabilities;  
* incremental delivery;  
* long-term maintainability;  
* controlled technology evolution;  
* future integrations;  
* future administrative capabilities;  
* future artificial intelligence capabilities;  
* Specification-Driven Development.

The architecture shall satisfy current approved requirements without introducing infrastructure or system complexity justified only by speculative future needs.

The selected architecture shall prioritize:

1. correctness;  
2. simplicity;  
3. maintainability;  
4. testability;  
5. security;  
6. operational clarity;  
7. controlled extensibility.

---

# **6\. Architecture Objectives**

The architecture shall achieve the following objectives.

## **AO-001 — Structural Simplicity**

The system shall use the smallest architectural structure capable of satisfying approved business and technical requirements.

---

## **AO-002 — Modular Evolution**

The application shall support incremental evolution through explicit and cohesive module boundaries.

---

## **AO-003 — Maintainability**

Architectural organization shall enable components to be understood, tested, modified, and replaced without unnecessary impact on unrelated responsibilities.

---

## **AO-004 — Explicit Dependencies**

Dependencies between layers, modules, infrastructure components, and integrations shall remain visible and controlled.

---

## **AO-005 — Testability**

Architectural boundaries shall support isolated verification of domain, application, integration, and presentation behavior where applicable.

---

## **AO-006 — Security by Design**

Security responsibilities shall be incorporated into architectural boundaries, configuration, data handling, integrations, and deployment topology.

---

## **AO-007 — Operational Simplicity**

The production topology shall remain proportional to the maturity, scale, and operational needs of the product.

---

## **AO-008 — Controlled Extensibility**

The architecture shall support approved future capabilities without requiring avoidable system-wide redesign.

---

# **7\. Architectural Traceability**

The architecture shall maintain explicit and bidirectional traceability across the complete engineering lifecycle.

The mandatory traceability chain is:

Business Requirement (`BR-*`)

↓

Technical Requirement (`TR-*`, `NFR-*`, `SEC-*`, `INT-*`, `DATA-*`)

↓

Architecture Requirement (`AR-*`)

↓

Architectural Decision (`AD-*` or `ADR-*`)

↓

API or Data Contract

↓

Feature Specification (`SPEC-*`)

↓

Implementation

↓

Verification and Validation

↓

Release

Every architecture requirement shall identify its originating technical and business requirements.

Every architectural decision shall identify:

* the architecture requirement it satisfies;  
* the affected architectural components;  
* relevant constraints;  
* consequences;  
* downstream documents affected by the decision.

Implementation activities shall not originate new architectural decisions.

When implementation reveals a required architectural change, the change shall return to Architecture & Engineering Review before implementation continues.

---

# **8\. Architecture Requirement Baseline**

The following Architecture Requirements constitute the approved system-level architecture baseline.

## **AR-001 — Modular Monolith**

The system shall be structured as a Modular Monolith and deployed as a single application unit.

**Source traceability:** TR-004, NFR-003, NFR-009, TCN-001.

---

## **AR-002 — Explicit Module Boundaries**

The application shall be decomposed into cohesive modules with explicit responsibilities and controlled dependencies.

**Source traceability:** TR-004, QA-001, QA-002.

---

## **AR-003 — Layered Responsibility Separation**

The architecture shall separate presentation, application, domain, infrastructure, and integration responsibilities where those responsibilities exist.

**Source traceability:** TR-003, TR-006, EP-004, QA-001, QA-002.

---

## **AR-004 — Single Deployable Application**

Release 1 shall operate as a single deployable application.

**Source traceability:** TCN-001, QA-007, NFR-003.

---

## **AR-005 — Relational Persistence**

Persistent application data shall use PostgreSQL as the authoritative relational data store.

**Source traceability:** DATA-001, DATA-002, DATA-003, DATA-004.

---

## **AR-006 — Server-Side Web Delivery**

The primary user interface shall use server-side rendering through Django Templates.

**Source traceability:** NFR-001, NFR-003, NFR-006, TCN-001.

---

## **AR-007 — Progressive Interaction**

Interactive behavior that does not require a dedicated client application shall use progressive enhancement through HTMX and minimal JavaScript.

**Source traceability:** NFR-001, NFR-003, QA-007, TCN-001.

---

## **AR-008 — Isolated External Integrations**

External services shall be isolated behind explicit integration boundaries and shall not be directly coupled to core application behavior.

**Source traceability:** INT-001, INT-002, INT-003, INT-005.

---

## **AR-009 — Environment-Based Configuration**

Environment-specific and sensitive configuration shall remain external to source code.

**Source traceability:** TR-007, SEC-003, SEC-006.

---

## **AR-010 — Controlled Architectural Evolution**

Architectural changes shall occur only through approved Architecture revisions or Architectural Decision Records.

**Source traceability:** TR-001, TR-002, ES-008, ES-010.

---

# **9\. Architectural Principles**

The following principles govern architectural design and evolution.

## **AP-001 — Modular Monolith First**

The system shall remain a Modular Monolith while this architecture satisfies approved functional, quality, operational, and scalability requirements.

Distributed services shall not be introduced without documented evidence that the Modular Monolith no longer satisfies approved requirements.

---

## **AP-002 — Separation of Concerns**

Each architectural element shall have a clear and cohesive responsibility.

Business behavior, presentation concerns, persistence concerns, external integrations, and operational configuration shall not be unnecessarily mixed.

---

## **AP-003 — High Cohesion**

Responsibilities that change for the same business or technical reason should remain grouped within the same module or architectural component.

---

## **AP-004 — Low Coupling**

Modules and layers shall minimize dependencies on internal details of other architectural elements.

---

## **AP-005 — Dependency Explicitness**

Dependencies shall be visible through imports, interfaces, configuration, contracts, or documented architectural relationships.

Hidden runtime dependencies are prohibited.

---

## **AP-006 — Simplicity Before Distribution**

Architectural complexity shall be introduced only when required by approved requirements or demonstrated operational constraints.

---

## **AP-007 — Security by Design**

Security shall be incorporated into architectural decisions involving configuration, data, external input, integration, deployment, and access control.

---

## **AP-008 — Maintainability by Design**

Architectural decisions shall optimize for understandable boundaries, controlled change impact, testability, and long-term support.

---

## **AP-009 — Progressive Evolution**

The architecture shall evolve incrementally through controlled and traceable decisions.

---

## **AP-010 — Specification Before Implementation**

Architectural changes shall be specified and approved before implementation.

---

# **10\. Approved Architecture Style**

The approved architecture style is a **Modular Monolith**.

The application shall consist of cohesive functional modules running within a single application process and deployed as one application unit.

The Modular Monolith shall provide:

* centralized configuration;  
* a shared deployment lifecycle;  
* explicit internal module boundaries;  
* controlled internal dependencies;  
* common relational persistence infrastructure;  
* simplified local development;  
* simplified deployment;  
* simplified observability;  
* controlled future extraction of modules when justified.

The use of a single deployable unit shall not permit unstructured coupling.

Internal boundaries shall be treated as architectural contracts.

---

## **10.1 Architectural Characteristics**

The Modular Monolith shall have the following characteristics:

* one primary application repository;  
* one primary deployable application;  
* one primary relational database;  
* cohesive functional modules;  
* centralized runtime configuration;  
* shared operational infrastructure;  
* explicit internal dependency rules;  
* controlled integration adapters;  
* common release coordination.

---

## **10.2 Microservices Exclusion**

Microservices are intentionally excluded from the approved architecture baseline.

Microservices shall not be introduced based solely on:

* perceived industry trends;  
* speculative scalability;  
* organizational patterns that do not exist in the project;  
* technology preference;  
* anticipated future features without approved requirements.

A transition to distributed services would require:

* demonstrated limitations of the Modular Monolith;  
* measurable operational or scalability requirements;  
* detailed impact analysis;  
* documented data ownership;  
* documented service boundaries;  
* distributed observability planning;  
* deployment and operational readiness;  
* an approved ADR;  
* Product Owner approval.

---

# **11\. Technology Baseline**

The approved technology baseline is defined below.

## **11.1 Backend**

* Python  
* Django

Django shall provide the primary web application framework and application runtime.

---

## **11.2 Frontend**

* Django Templates  
* HTMX  
* minimal Vanilla JavaScript

Django Templates shall provide server-side HTML rendering.

HTMX shall support progressive interaction where server-driven updates satisfy the approved user experience requirements.

Vanilla JavaScript shall be introduced only where browser-side behavior cannot be adequately provided through HTML, CSS, or HTMX.

---

## **11.3 Database**

* PostgreSQL

PostgreSQL shall serve as the authoritative production relational database.

---

## **11.4 Version Control and Repository**

* Git  
* GitHub

Engineering documents, source code, tests, configuration templates, migrations, and deployment artifacts shall be maintained under version control.

---

## **11.5 Development Model**

* Specification-Driven Development

Implementation shall originate from approved requirements, architecture, contracts, and Feature Specifications.

---

## **11.6 Technology Introduction Rule**

Additional frameworks, libraries, databases, infrastructure components, or external platforms shall require architectural evaluation before adoption.

Technology evaluation shall consider:

* requirement fit;  
* architectural consistency;  
* maintenance burden;  
* security impact;  
* testing impact;  
* operational impact;  
* deployment complexity;  
* cost;  
* vendor dependency;  
* long-term sustainability.

Technologies with material architectural impact shall require an approved ADR.

---

# **12\. Logical Architecture**

The application shall use a layered logical architecture to separate system responsibilities and control dependency direction.

The logical architecture shall contain the following layers where applicable:

1. Presentation;  
2. Application;  
3. Domain;  
4. Infrastructure;  
5. Integrations.

Layering shall support separation of concerns without creating unnecessary abstraction.

A module may omit a dedicated layer when that layer has no meaningful responsibility within the module.

---

## **12.1 Presentation Layer**

The Presentation Layer shall manage interaction between external users or clients and the application.

Its responsibilities include:

* receiving HTTP requests;  
* routing requests;  
* validating presentation-level input;  
* invoking application operations;  
* rendering HTML responses;  
* returning appropriate HTTP responses;  
* displaying validation and application errors;  
* managing progressive web interactions.

The Presentation Layer may include:

* Django views;  
* URL routing;  
* Django forms;  
* Django Templates;  
* HTMX response fragments;  
* presentation-specific serializers where required;  
* browser-facing static assets.

The Presentation Layer shall not contain:

* persistence logic;  
* external provider implementation details;  
* reusable domain rules;  
* infrastructure configuration;  
* direct orchestration of unrelated modules.

---

## **12.2 Application Layer**

The Application Layer shall coordinate system use cases.

Its responsibilities include:

* executing application workflows;  
* coordinating domain behavior;  
* invoking persistence operations;  
* invoking integration interfaces;  
* enforcing use-case sequencing;  
* managing application-level transactions where required;  
* returning structured operation results.

The Application Layer shall describe what the system does for a specific use case without depending directly on presentation technology.

Application services shall not contain provider-specific integration logic or presentation rendering behavior.

---

## **12.3 Domain Layer**

The Domain Layer shall contain reusable business behavior where meaningful business rules exist.

Its responsibilities may include:

* domain entities;  
* value objects;  
* domain validation;  
* business invariants;  
* domain services;  
* domain-specific exceptions.

Domain behavior shall remain independent from:

* HTTP;  
* templates;  
* database drivers;  
* external providers;  
* deployment configuration.

Simple modules shall not be forced to introduce domain abstractions when their behavior consists only of straightforward data presentation or orchestration.

---

## **12.4 Infrastructure Layer**

The Infrastructure Layer shall provide technical implementations required by the application.

Its responsibilities may include:

* database persistence;  
* repository implementations;  
* cache access;  
* file storage;  
* configuration access;  
* logging infrastructure;  
* framework-specific adapters;  
* technical utility services.

Infrastructure components shall implement interfaces or contracts required by the Application or Domain layers where such abstraction provides a clear engineering benefit.

Infrastructure details shall not propagate into domain behavior.

---

## **12.5 Integrations Layer**

The Integrations Layer shall isolate communication with external systems and services.

Its responsibilities include:

* external service clients;  
* provider authentication;  
* request and response transformation;  
* provider-specific error handling;  
* timeout configuration;  
* retry behavior where approved;  
* integration logging;  
* integration health verification where applicable.

External provider models shall not become internal domain models without explicit transformation.

---

# **13\. Dependency Rules**

Dependencies shall flow toward stable business and application responsibilities.

The permitted general dependency direction is:

Presentation

↓

Application

↓

Domain

Infrastructure and Integration implementations may depend on framework or provider technologies but shall be invoked through controlled application boundaries.

---

## **13.1 Permitted Dependencies**

The following dependencies are permitted where required:

* Presentation may depend on Application;  
* Application may depend on Domain;  
* Infrastructure may implement interfaces defined by Application or Domain;  
* Integrations may implement interfaces defined by Application;  
* module composition may connect concrete implementations during application startup.

---

## **13.2 Restricted Dependencies**

The following dependencies are prohibited unless explicitly justified by an approved architectural decision:

* Domain depending on Presentation;  
* Domain depending directly on Django views or templates;  
* Domain depending directly on external service clients;  
* Presentation directly accessing provider APIs;  
* Presentation directly executing persistence queries for reusable business workflows;  
* circular dependencies between modules;  
* infrastructure components defining business rules;  
* one module accessing another module's internal implementation details.

---

## **13.3 Framework Dependency**

Django is the approved framework and may be used directly where doing so preserves simplicity and maintainability.

Framework isolation shall not be implemented as an absolute objective.

Abstractions shall be introduced only when they:

* improve testability;  
* isolate meaningful volatility;  
* protect module boundaries;  
* support provider replaceability;  
* prevent infrastructure concerns from contaminating business behavior.

Unnecessary wrapper layers around stable Django functionality are prohibited.

---

# **14\. Module Architecture**

The application shall be organized into cohesive functional modules.

Each module shall represent a clear product, application, or supporting capability.

Modules shall:

* own a defined responsibility;  
* expose controlled entry points;  
* minimize dependencies on other modules;  
* protect internal implementation details;  
* maintain their own tests;  
* maintain explicit data ownership;  
* avoid circular dependencies.

---

## **14.1 Initial Module Categories**

The Release 1 architecture may contain modules corresponding to the approved product capabilities.

Expected module categories include:

* professional profile;  
* portfolio projects;  
* contact;  
* budget request;  
* shared platform services;  
* external integrations.

The exact module names and file structure shall be defined during implementation planning or within Feature Specifications.

This architecture does not mandate one Django application for every page or user-interface section.

Module boundaries shall be based on cohesive responsibilities rather than visual navigation alone.

---

## **14.2 Professional Profile Module**

The Professional Profile module may own content and behavior related to:

* professional summary;  
* skills;  
* education;  
* experience;  
* résumé availability;  
* public professional links.

It shall not own portfolio project behavior or contact submission processing.

---

## **14.3 Portfolio Module**

The Portfolio module may own:

* featured project information;  
* project metadata;  
* project presentation rules;  
* project links;  
* project ordering and visibility.

External GitHub data retrieval, when introduced, shall remain behind an integration boundary.

---

## **14.4 Contact Module**

The Contact module may own:

* contact form processing;  
* contact request validation;  
* contact request persistence when required;  
* contact notification workflows;  
* submission status handling.

Transactional email provider behavior shall remain in the Integrations Layer.

---

## **14.5 Budget Request Module**

The Budget Request module may own:

* quotation request input;  
* business contact details;  
* request validation;  
* request lifecycle state where persistence is required;  
* delivery to an approved communication channel.

The module may share selected application services with the Contact module only when the shared responsibility is explicit and cohesive.

---

## **14.6 Shared Platform Module**

Cross-cutting capabilities may be grouped into shared platform components when they are not owned by a single functional module.

These may include:

* common template structures;  
* shared presentation utilities;  
* localization support;  
* configuration access;  
* common logging;  
* common error handling;  
* reusable validation primitives.

The shared platform module shall not become a repository for unrelated code.

---

## **14.7 Module Interface Rules**

A module shall expose only the operations required by other modules.

Cross-module interaction shall occur through:

* application services;  
* explicitly published functions;  
* defined interfaces;  
* domain events only when justified;  
* stable shared contracts.

Direct imports from another module's internal packages are prohibited.

---

# **15\. Data Architecture**

PostgreSQL shall be the authoritative relational database for persistent production data.

The data architecture shall preserve:

* integrity;  
* consistency;  
* controlled ownership;  
* transactional correctness;  
* recoverability;  
* traceability where applicable;  
* controlled schema evolution.

---

## **15.1 Data Ownership**

Each persistent entity shall have one clearly identified owning module.

The owning module shall be responsible for:

* defining data semantics;  
* enforcing validation;  
* maintaining schema evolution;  
* controlling modification operations;  
* documenting relationships;  
* defining retention behavior where applicable.

Other modules shall not modify owned data through undocumented direct access.

---

## **15.2 Shared Database Model**

The Modular Monolith shall use a shared PostgreSQL database.

A shared database does not imply unrestricted schema access.

Logical data boundaries shall be preserved through:

* Django application ownership;  
* model ownership;  
* controlled application services;  
* explicit foreign-key relationships;  
* documented read dependencies;  
* restricted write operations.

---

## **15.3 Data Access**

Django ORM shall provide the default data-access mechanism.

Raw SQL may be used only when:

* Django ORM cannot express the required behavior adequately;  
* a measured performance requirement justifies it;  
* the query is documented;  
* tests verify its behavior;  
* database portability implications are accepted.

---

## **15.4 Schema Evolution**

Database schema changes shall be managed through version-controlled Django migrations.

Schema changes shall:

* remain reproducible;  
* support controlled deployment;  
* preserve existing data when required;  
* include rollback or recovery considerations;  
* be reviewed for operational impact;  
* remain traceable to an approved requirement or specification.

Manual production schema changes outside the controlled migration process are prohibited.

---

## **15.5 Transaction Management**

Transactions shall be defined according to use-case consistency requirements.

Transaction boundaries shall:

* remain as short as practical;  
* avoid unnecessary external network operations;  
* protect multi-step state changes;  
* preserve data integrity;  
* define failure behavior.

External provider calls should not be executed inside database transactions unless the consistency requirement and failure consequences are explicitly evaluated.

---

## **15.6 Data Validation**

Data shall be validated at appropriate boundaries.

Validation may occur through:

* Django forms;  
* model constraints;  
* application services;  
* domain objects;  
* database constraints.

Critical integrity rules shall not rely exclusively on presentation-level validation.

---

## **15.7 Personally Identifiable Information**

Personally identifiable information shall be collected only when required by an approved capability.

The architecture shall support:

* data minimization;  
* purpose limitation;  
* controlled access;  
* secure transmission;  
* retention decisions;  
* deletion where applicable;  
* compliance with applicable legal requirements.

Detailed privacy and retention rules require explicit project policy or lower-level specification because they are not defined in the current architecture source baseline.

---

## **15.8 Backup and Recovery**

Production data shall be included in the operational backup strategy.

Backup frequency, retention, storage location, encryption, recovery objectives, and restoration procedures shall be defined in `06-deployment-and-operations.md`.

The architecture shall not introduce persistence mechanisms that cannot participate in controlled backup and recovery.

---

# **16\. Integration Architecture**

External services shall be accessed through explicit integration components.

Initial external dependencies identified by the approved architecture include:

* transactional email provider;  
* WhatsApp contact link;  
* GitHub profile;  
* LinkedIn profile;  
* Google Drive résumé link.

Not every external link constitutes a runtime API integration.

Static outbound links may remain presentation configuration when they do not require remote data exchange.

---

## **16.1 Integration Boundary**

Runtime integrations shall be isolated from core application behavior.

Integration components shall be responsible for:

* provider-specific configuration;  
* authentication credentials;  
* request construction;  
* response parsing;  
* timeout management;  
* provider error mapping;  
* logging;  
* retry behavior where appropriate.

Application workflows shall depend on internal integration contracts rather than provider-specific client behavior when provider replaceability or isolated testing is required.

---

## **16.2 Transactional Email Integration**

The transactional email integration shall support contact and budget request delivery where approved by feature specifications.

The integration design shall account for:

* provider configuration;  
* sender identity;  
* destination configuration;  
* timeout behavior;  
* delivery failure;  
* provider unavailability;  
* logging without exposing sensitive content;  
* test substitution.

The specific provider shall be documented through an ADR or integration contract before implementation.

---

## **16.3 Social and Professional Links**

WhatsApp, GitHub, LinkedIn, and résumé links may initially operate as configured outbound links.

Configuration shall remain externalized where environment-specific values differ.

Future API-based synchronization with GitHub or other services shall require:

* an approved Feature Specification;  
* an explicit API contract;  
* rate-limit handling;  
* timeout behavior;  
* caching evaluation;  
* failure fallback;  
* security review.

---

## **16.4 Integration Failure Handling**

External service failure shall not produce uncontrolled application failure.

Integration behavior shall define:

* timeout limits;  
* recoverable and non-recoverable errors;  
* user-visible fallback behavior;  
* logging;  
* retry eligibility;  
* duplicate-operation prevention where applicable.

Retries shall not be introduced automatically.

Retry policies shall consider idempotency, provider limits, operational impact, and user experience.

---

## **16.5 Integration Observability**

Runtime integrations shall produce sufficient diagnostic information to investigate failure.

Logs shall include, where appropriate:

* integration name;  
* operation type;  
* outcome;  
* duration;  
* external correlation identifier;  
* normalized error category.

Logs shall not expose:

* credentials;  
* access tokens;  
* secrets;  
* unnecessary personal information;  
* full sensitive payloads.

---

# **17\. Security Architecture**

Security shall be implemented as a cross-cutting architectural responsibility.

The security architecture shall address:

* configuration;  
* external input;  
* output rendering;  
* data handling;  
* integrations;  
* network transport;  
* dependency management;  
* deployment;  
* future access control.

---

## **17.1 Secure Configuration**

Secrets and environment-specific configuration shall remain outside source code.

Sensitive values may include:

* Django secret keys;  
* database credentials;  
* email provider credentials;  
* integration tokens;  
* deployment credentials.

Configuration shall be supplied through approved environment-based mechanisms.

Production secrets shall not be committed to version control.

---

## **17.2 Input Validation**

All externally supplied input shall be validated before trusted use.

External input includes:

* form data;  
* query parameters;  
* URL parameters;  
* headers where used;  
* uploaded files if introduced;  
* provider responses;  
* configuration values.

Validation shall verify applicable:

* type;  
* format;  
* length;  
* allowed values;  
* required fields;  
* semantic constraints.

---

## **17.3 Output Security**

Django's default template escaping shall remain enabled.

Unescaped HTML output shall require explicit justification and trusted sanitization.

The application shall prevent unsafe rendering of user-submitted content.

---

## **17.4 Cross-Site Request Forgery Protection**

Django CSRF protection shall remain enabled for state-changing browser requests.

Disabling CSRF protection requires an approved security justification and compensating controls.

---

## **17.5 Transport Security**

Production traffic shall use HTTPS.

HTTP traffic shall be redirected to HTTPS where supported by the deployment topology.

Secure cookie and proxy-related settings shall be configured according to the final deployment architecture.

---

## **17.6 Dependency Security**

Python and frontend dependencies shall be:

* explicitly declared;  
* version controlled;  
* reviewed before introduction;  
* updated through controlled changes;  
* assessed for known vulnerabilities where tooling permits;  
* minimized to reduce attack surface.

Unused dependencies shall be removed.

---

## **17.7 Least Privilege**

Runtime processes, database users, deployment users, and external credentials shall receive only the permissions required for their responsibilities.

Shared administrative credentials shall be avoided where operationally practical.

---

## **17.8 User-Submitted Data**

Contact and budget request data shall be treated as untrusted input and potentially sensitive information.

The architecture shall support:

* validation;  
* secure transmission;  
* controlled storage where required;  
* limited logging;  
* restricted operational access;  
* defined retention through future policy or specification.

---

## **17.9 Authentication Boundary**

Authentication and administrative authorization are outside Release 1 scope.

Release 1 shall not introduce an application authentication system solely for anticipated future requirements.

When administrative capabilities enter an approved release, the architecture shall evaluate Django's native authentication and authorization framework.

The future access-control model is expected to support:

* authenticated administrators;  
* permission-based authorization;  
* protected administrative resources;  
* auditable administrative actions.

These expectations do not constitute an approved Release 1 implementation requirement.

---

## **17.10 Custom Authentication Restriction**

Custom authentication mechanisms shall not be introduced unless:

* native Django capabilities cannot satisfy approved requirements;  
* the deficiency is documented;  
* security impact is analyzed;  
* maintenance consequences are accepted;  
* an ADR is approved.

---

## **17.11 Security Decision Traceability**

Material security decisions shall be traceable to:

* `SEC-*` requirements;  
* affected architecture requirements;  
* applicable ADRs;  
* Feature Specifications;  
* verification evidence.

Security controls shall not be removed or weakened through implementation-only changes.

---

# **18\. Deployment Architecture**

The approved target production platform is a Hostinger Linux Virtual Private Server.

The deployment architecture shall preserve:

* operational simplicity;  
* secure configuration;  
* reproducibility;  
* environment isolation;  
* recoverability;  
* controlled release execution;  
* compatibility with the approved Modular Monolith.

Detailed installation commands, infrastructure procedures, and release runbooks shall be defined in `06-deployment-and-operations.md`.

---

## **18.1 Deployment Topology**

The production topology shall support the following logical components:

* public HTTPS endpoint;  
* reverse proxy;  
* Django application runtime;  
* PostgreSQL database;  
* static asset delivery;  
* persistent media storage where required;  
* centralized application configuration;  
* backup mechanism;  
* operational logging.

The exact infrastructure components, process manager, reverse proxy technology, and service configuration shall be documented in Deployment and Operations documentation or an approved ADR.

This Architecture document does not approve a specific reverse proxy, application server, container runtime, or process supervisor unless separately recorded through an approved architectural decision.

---

## **18.2 Single-Application Deployment**

The Modular Monolith shall be deployed as one coordinated application release.

The application release may contain:

* application code;  
* templates;  
* static assets;  
* database migrations;  
* configuration references;  
* operational scripts;  
* release metadata.

All release components shall remain version-compatible.

Partial deployment of incompatible application components is prohibited.

---

## **18.3 Environment Model**

The project shall maintain logically isolated environments.

The approved minimum environment model is:

* local development;  
* staging;  
* production.

Each environment shall use independent configuration.

Production credentials and persistent data shall not be reused in local development.

---

## **18.4 Local Development Environment**

The local development environment shall support:

* reproducible project setup;  
* isolated dependencies;  
* local configuration;  
* automated tests;  
* database migrations;  
* static asset development;  
* implementation verification.

Local development decisions shall not weaken production security requirements.

---

## **18.5 Staging Environment**

The staging environment shall provide pre-production verification where operationally feasible.

Staging shall support verification of:

* deployment procedures;  
* database migrations;  
* environment configuration;  
* external integrations;  
* static asset delivery;  
* user-facing workflows;  
* release candidate behavior.

Staging should resemble production sufficiently to detect deployment and configuration defects.

Differences between staging and production shall be documented.

---

## **18.6 Production Environment**

The production environment shall host only approved releases.

Production deployment shall require:

* completed implementation;  
* completed automated verification;  
* completed acceptance verification;  
* updated engineering documentation;  
* approved release artifacts;  
* Human Release Approval.

Direct unreviewed modification of production application files is prohibited.

---

## **18.7 HTTPS**

Production traffic shall use HTTPS.

The deployment topology shall support:

* valid TLS certificates;  
* certificate renewal;  
* HTTP-to-HTTPS redirection;  
* secure transport for user-submitted information;  
* secure proxy configuration.

Detailed certificate and renewal procedures belong to Deployment and Operations documentation.

---

## **18.8 Static Assets**

Static assets shall be built, collected, or otherwise prepared through a reproducible release process.

Static asset handling shall define:

* source ownership;  
* build or collection procedure;  
* deployment location;  
* cache behavior;  
* version compatibility;  
* failure handling.

The final static asset delivery mechanism shall remain proportional to project scale and operational requirements.

---

## **18.9 Media Storage**

Persistent user-managed media is not currently established as a Release 1 architectural requirement.

When persistent media storage becomes necessary, an approved specification shall define:

* ownership;  
* storage location;  
* access controls;  
* backup;  
* retention;  
* deletion;  
* migration;  
* production recoverability.

Local ephemeral filesystem storage shall not be assumed to provide durable media persistence.

---

## **18.10 Database Deployment**

PostgreSQL shall be deployed using secure and maintainable operational practices.

The deployment architecture shall support:

* restricted network access;  
* dedicated credentials;  
* controlled schema migrations;  
* automated backup;  
* restoration verification;  
* resource monitoring;  
* version compatibility.

The specific PostgreSQL hosting topology shall be defined in Deployment and Operations documentation.

---

## **18.11 Deployment Reproducibility**

Deployment shall be executable from version-controlled artifacts and documented configuration.

A release shall not depend on undocumented manual knowledge.

Deployment procedures shall produce consistent results when applied to equivalent environments.

---

## **18.12 Deployment Failure**

The operational design shall define behavior for failed deployments.

The release process shall account for:

* application startup failure;  
* migration failure;  
* configuration failure;  
* dependency installation failure;  
* health verification failure;  
* integration configuration failure.

Rollback or forward-recovery procedures shall be defined in Deployment and Operations documentation.

---

# **19\. Operational Architecture**

Operational architecture shall enable the system to be deployed, observed, maintained, recovered, and evolved without unnecessary operational complexity.

Operational responsibilities shall remain proportional to:

* current traffic;  
* data criticality;  
* release frequency;  
* product maturity;  
* business impact;  
* available operational capacity.

---

## **19.1 Operational Objectives**

The operational architecture shall support:

### **OP-001 — Reproducibility**

Equivalent release artifacts and configuration shall produce equivalent deployments.

### **OP-002 — Diagnosability**

Operational failures shall produce sufficient information for investigation.

### **OP-003 — Recoverability**

Application and persistent data shall support documented recovery procedures.

### **OP-004 — Controlled Change**

Production changes shall occur through the approved release process.

### **OP-005 — Configuration Isolation**

Environment-specific settings shall remain separate from source code.

### **OP-006 — Operational Simplicity**

Infrastructure components shall be introduced only when justified by approved requirements.

---

## **19.2 Application Runtime**

The Django application shall run under a production-capable application runtime.

The runtime shall support:

* controlled process startup;  
* controlled shutdown;  
* restart after failure;  
* environment-based configuration;  
* structured logging;  
* predictable resource use;  
* integration with the selected reverse proxy.

The specific application server and process management mechanism require an approved operational decision.

---

## **19.3 Health Verification**

The deployment architecture shall support objective verification that the application is operational after release.

Health verification may include:

* application process availability;  
* HTTP response verification;  
* database connectivity;  
* required configuration availability;  
* migration status;  
* critical integration readiness where applicable.

A health check shall not expose credentials, internal stack traces, or sensitive configuration.

---

## **19.4 Backup Architecture**

The operational architecture shall support backup of persistent production data.

The backup design shall define:

* protected resources;  
* backup frequency;  
* retention period;  
* storage location;  
* encryption where required;  
* access control;  
* restoration procedure;  
* restoration validation.

A backup shall not be considered operationally valid until restoration has been demonstrated or verified according to an approved procedure.

---

## **19.5 Recovery Architecture**

Recovery planning shall address:

* accidental data loss;  
* failed schema migration;  
* application release failure;  
* corrupted deployment;  
* infrastructure replacement;  
* configuration loss.

Recovery objectives such as Recovery Point Objective and Recovery Time Objective are not defined by the currently approved source baselines.

They shall be established through business and operational requirements before being treated as normative targets.

---

## **19.6 Release Coordination**

Application code, database migrations, configuration changes, and operational changes shall be coordinated as one controlled release when dependencies exist between them.

Release documentation shall identify:

* release version;  
* included requirements;  
* included migrations;  
* configuration changes;  
* verification evidence;  
* known limitations;  
* rollback or recovery considerations;  
* approval status.

---

## **19.7 Operational Access**

Production access shall follow the principle of least privilege.

Operational access shall be limited to authorized personnel and activities.

Privileged actions should be attributable to an identifiable operator where technically and operationally feasible.

Shared credentials shall be avoided.

---

# **20\. Observability Architecture**

The architecture shall provide sufficient observability to support fault detection, diagnosis, operational validation, and release verification.

Observability shall remain appropriate to project scale.

The architecture shall not require an unnecessarily complex observability platform for Release 1\.

---

## **20.1 Logging**

The application shall produce structured or consistently formatted logs.

Logs shall support identification of:

* timestamp;  
* severity;  
* application component;  
* operation;  
* outcome;  
* normalized error information;  
* correlation context where applicable.

Logs shall not expose:

* secrets;  
* passwords;  
* access tokens;  
* database credentials;  
* unnecessary personal information;  
* complete sensitive request payloads.

---

## **20.2 Log Categories**

The architecture should distinguish relevant log categories, including:

* application lifecycle;  
* HTTP request failures;  
* validation failures;  
* integration failures;  
* database failures;  
* security-relevant events;  
* deployment and startup failures;  
* unexpected exceptions.

Expected user validation errors shall not be treated as system failures.

---

## **20.3 Error Handling**

Unhandled exceptions shall be captured by the application boundary and converted into controlled responses.

Production responses shall not expose:

* stack traces;  
* source paths;  
* internal configuration;  
* SQL statements;  
* provider credentials;  
* internal infrastructure details.

Diagnostic details shall remain available only through approved operational channels.

---

## **20.4 Metrics**

Release 1 does not require a dedicated metrics platform unless justified by operational requirements.

The architecture shall permit future introduction of metrics for:

* request volume;  
* response duration;  
* error rate;  
* integration duration;  
* integration failure rate;  
* database performance;  
* resource utilization;  
* availability.

Metrics shall be introduced through controlled operational evolution.

---

## **20.5 Tracing**

Distributed tracing is not required for the approved Modular Monolith baseline.

Correlation identifiers or local request tracing may be introduced when they improve diagnostic value without adding disproportionate complexity.

Distributed tracing shall be reconsidered only if the architecture evolves toward multiple independently communicating runtime services.

---

## **20.6 Alerting**

Operational alerting requirements are not fully defined in the current source baselines.

Alerting shall be introduced when measurable operational conditions and responsible recipients have been defined.

Alerts shall correspond to actionable conditions.

---

# **21\. Performance and Scalability Architecture**

The architecture shall support acceptable performance for approved product usage while avoiding premature optimization.

Performance decisions shall be based on:

* measurable acceptance criteria;  
* observed behavior;  
* expected usage;  
* operational evidence;  
* business impact.

---

## **21.1 Performance Responsibility**

Performance shall be addressed across:

* application queries;  
* template rendering;  
* static asset delivery;  
* database access;  
* integration calls;  
* deployment configuration;  
* caching where justified.

No single architectural layer shall be assumed to solve all performance concerns.

---

## **21.2 Database Performance**

Database access shall avoid known inefficient patterns.

Architecture and implementation reviews shall evaluate:

* unnecessary query volume;  
* repeated database access;  
* missing indexes;  
* inefficient relationship loading;  
* unbounded result sets;  
* long-running transactions.

Indexes and query optimization shall be justified by data access requirements or measured behavior.

---

## **21.3 Caching**

Caching is not mandatory for Release 1\.

Caching may be introduced when:

* measurable performance requirements justify it;  
* cache ownership is explicit;  
* invalidation behavior is defined;  
* stale-data consequences are understood;  
* failure behavior is documented;  
* operational impact is acceptable.

A cache shall not become the authoritative source of persistent business data.

---

## **21.4 Horizontal Scaling**

The initial deployment does not require horizontal application scaling.

The architecture shall avoid unnecessary assumptions that permanently prevent future horizontal scaling.

Before horizontal scaling is introduced, the architecture shall evaluate:

* session storage;  
* local filesystem dependencies;  
* shared media storage;  
* cache topology;  
* database connections;  
* background processing;  
* load balancing;  
* deployment coordination.

---

## **21.5 Vertical Scaling**

Vertical resource scaling may be used as the initial capacity strategy when it satisfies approved performance and cost requirements.

Capacity changes shall be based on observed or forecast resource needs.

---

## **21.6 Background Processing**

Dedicated asynchronous processing infrastructure is not part of the current approved architecture baseline.

Background task infrastructure shall require:

* an approved functional requirement;  
* workload analysis;  
* failure and retry semantics;  
* idempotency evaluation;  
* persistence requirements;  
* operational monitoring;  
* an approved ADR.

---

# **22\. Availability and Reliability Architecture**

The architecture shall provide reliable operation appropriate to the approved product scope.

The current baselines do not define a numeric availability target.

Therefore, no availability percentage shall be treated as approved until established through an explicit requirement.

---

## **22.1 Reliability Principles**

The architecture shall promote reliability through:

* deterministic behavior;  
* validation;  
* controlled failures;  
* transactional consistency;  
* integration timeouts;  
* recovery procedures;  
* automated verification;  
* reproducible deployment.

---

## **22.2 Single-Server Consequence**

The initial Hostinger VPS deployment may contain infrastructure-level single points of failure.

This limitation is accepted provisionally because the current project baselines prioritize operational simplicity and do not establish high-availability requirements.

Any future high-availability architecture shall require:

* approved availability objectives;  
* cost analysis;  
* redundant infrastructure;  
* database availability planning;  
* load balancing;  
* operational ownership;  
* recovery testing;  
* an approved ADR.

---

## **22.3 Graceful Degradation**

Failure of a non-critical external service should not make unrelated public portfolio content unavailable.

Feature Specifications and integration contracts shall define appropriate fallback behavior.

Examples may include:

* preserving page access when an external profile API fails;  
* presenting a controlled error when email delivery fails;  
* retaining a submitted request for later processing when explicitly designed and approved.

These examples are architectural guidance and do not authorize unapproved feature behavior.

---

# **23\. Architecture Evolution**

The architecture shall evolve incrementally according to approved business and technical baselines.

Roadmap entries do not independently authorize architectural implementation.

Every architectural evolution shall originate from approved requirements and follow the Specification Engineering lifecycle.

---

## **23.1 Release 1 Architecture**

Release 1 shall support the Professional Portfolio MVP.

The architecture baseline includes:

* Modular Monolith;  
* Django application;  
* server-side rendering;  
* progressive HTMX interactions;  
* PostgreSQL;  
* public professional content;  
* contact capability;  
* budget request capability;  
* outbound professional links;  
* secure deployment on Hostinger Linux VPS.

Authentication, administrative functionality, RAG, and intelligent search are excluded from Release 1\.

---

## **23.2 Release 1.1 Architecture Evolution**

Release 1.1 may introduce architecture changes required by approved capabilities such as:

* expanded portfolio content;  
* analytics;  
* GitHub synchronization;  
* user experience improvements;  
* SEO improvements.

Each change shall be evaluated for:

* module ownership;  
* integration impact;  
* data ownership;  
* security impact;  
* operational impact;  
* testing impact;  
* traceability.

---

## **23.3 Release 2 Architecture Evolution**

Release 2 may require architecture support for:

* administrative interfaces;  
* authentication and authorization;  
* knowledge management;  
* artificial intelligence integration;  
* Retrieval-Augmented Generation;  
* intelligent search;  
* dashboards.

These capabilities shall not be pre-implemented within Release 1 solely to anticipate future needs.

---

## **23.4 Future AI Architecture**

Artificial intelligence capabilities are outside the approved Release 1 architecture.

Before AI functionality is introduced, approved specifications shall address:

* user purpose;  
* model provider;  
* data classification;  
* prompt management;  
* output validation;  
* privacy;  
* security;  
* latency;  
* cost;  
* observability;  
* failure behavior;  
* human oversight;  
* provider replaceability.

RAG shall additionally require decisions covering:

* source ownership;  
* ingestion;  
* chunking;  
* indexing;  
* embedding generation;  
* retrieval;  
* document synchronization;  
* access control;  
* evaluation;  
* deletion and retention.

No AI infrastructure technology is approved by this baseline.

---

## **23.5 Module Extraction**

A module may be considered for extraction into an independent service only when there is documented evidence of a material need.

Valid drivers may include:

* independent scaling;  
* independent release ownership;  
* isolation of a materially different workload;  
* security isolation;  
* availability isolation;  
* regulatory separation;  
* operational boundary.

Extraction shall require an approved ADR and shall not occur through implementation refactoring alone.

---

## **23.6 Backward Compatibility**

Architectural evolution shall preserve backward compatibility whenever practical and consistent with approved requirements.

When compatibility cannot be preserved, the architectural decision shall document:

* affected consumers;  
* data migration;  
* contract changes;  
* deployment sequencing;  
* operational impact;  
* rollback limitations;  
* required communication.

---

# **24\. Architectural Constraints**

The following constraints are mandatory.

## **AC-001 — Primary Language**

Python shall remain the primary application implementation language.

---

## **AC-002 — Primary Web Framework**

Django shall remain the primary web framework.

---

## **AC-003 — Rendering Model**

Django Templates shall provide the primary server-side rendering mechanism.

---

## **AC-004 — Progressive Interaction**

HTMX shall provide the default mechanism for server-driven progressive interaction where applicable.

---

## **AC-005 — Client-Side Simplicity**

Client-side JavaScript shall remain minimal and shall be introduced only where justified by approved interaction requirements.

---

## **AC-006 — Production Database**

PostgreSQL shall remain the authoritative production relational database.

---

## **AC-007 — Deployment Platform**

Hostinger Linux VPS shall remain the initial target production platform.

---

## **AC-008 — Architecture Style**

The application shall remain a Modular Monolith unless an approved ADR justifies a different architectural style.

---

## **AC-009 — Single Deployable Unit**

Release 1 shall remain a single coordinated application deployment.

---

## **AC-010 — Controlled Change**

Architecture shall not be modified solely through implementation changes.

---

## **AC-011 — Traceability**

Every material architectural change shall preserve bidirectional traceability.

---

## **AC-012 — Proportional Complexity**

Architectural and infrastructure complexity shall remain proportional to approved requirements and operational needs.

---

# **25\. Architectural Decision Governance**

Architectural decisions shall be governed through controlled documentation.

A decision shall require an Architectural Decision Record when it:

* changes the approved architecture style;  
* introduces a material technology;  
* changes system boundaries;  
* changes dependency direction;  
* changes data ownership;  
* changes deployment topology;  
* introduces distributed infrastructure;  
* introduces a material security mechanism;  
* creates significant operational consequences;  
* supersedes an existing architectural decision.

---

## **25.1 ADR Content**

Each ADR shall include:

* ADR identifier;  
* title;  
* status;  
* date;  
* owner;  
* approver;  
* context;  
* affected requirements;  
* constraints;  
* evaluated alternatives;  
* trade-offs;  
* decision;  
* consequences;  
* affected documents;  
* superseded decisions where applicable.

---

## **25.2 ADR Status**

ADR status shall use the controlled lifecycle established by project governance or an approved ADR standard.

At minimum, an ADR shall distinguish between:

* proposed;  
* approved;  
* superseded;  
* rejected.

ADR status shall not replace the document lifecycle status defined by the EGS for engineering documents.

---

## **25.3 Decision Precedence**

An approved ADR may refine or supersede a specific decision recorded in this Architecture document.

An ADR shall not:

* contradict the Product Brief;  
* contradict the Technical Specification;  
* bypass Product Owner approval;  
* redefine unrelated architectural decisions;  
* authorize new business scope;  
* silently modify architectural constraints.

When an ADR supersedes architecture content, affected documents shall be updated or explicitly cross-referenced.

---

## **25.4 Technology Decision Evaluation**

Technology decisions shall evaluate:

* functional requirement fit;  
* quality attribute impact;  
* architectural consistency;  
* security;  
* maintainability;  
* testability;  
* performance;  
* scalability;  
* operational complexity;  
* deployment impact;  
* cost;  
* vendor dependency;  
* migration consequences;  
* technical debt.

Technology shall not be selected solely because of popularity or familiarity.

---

# **26\. Architecture Validation**

The architecture shall be validated before implementation and throughout controlled evolution.

Architecture validation shall determine whether the architecture:

* satisfies approved business requirements;  
* satisfies approved technical requirements;  
* preserves responsibility separation;  
* maintains valid dependency direction;  
* supports required quality attributes;  
* respects architectural constraints;  
* preserves traceability;  
* remains operationally viable;  
* avoids unnecessary complexity;  
* provides implementation-ready guidance.

---

## **26.1 Structural Validation**

Structural validation shall verify:

* module boundaries;  
* layer responsibilities;  
* dependency direction;  
* absence of prohibited circular dependencies;  
* ownership of persistent data;  
* integration isolation;  
* consistency with the Modular Monolith.

---

## **26.2 Technology Validation**

Technology validation shall verify:

* compatibility between selected technologies;  
* lifecycle and support suitability;  
* deployment compatibility;  
* testing support;  
* security implications;  
* operational viability;  
* consistency with approved constraints.

---

## **26.3 Security Validation**

Security architecture validation shall verify:

* external input boundaries;  
* secret management;  
* transport security;  
* output safety;  
* integration credential handling;  
* least privilege;  
* dependency controls;  
* handling of user-submitted data.

Detailed security tests shall be defined by Testing and Acceptance documentation.

---

## **26.4 Deployment Validation**

Deployment architecture validation shall verify:

* environment separation;  
* configuration externalization;  
* reproducible deployment;  
* migration execution;  
* health verification;  
* backup integration;  
* recovery considerations;  
* controlled production access.

---

## **26.5 Traceability Validation**

Every `AR-*`, `AC-*`, and material architectural decision shall be traceable to approved upstream requirements.

Downstream Feature Specifications, contracts, tests, and implementation shall reference the architectural requirements they satisfy.

Missing or unverifiable traceability shall prevent architecture approval.

---

# **27\. Architecture Quality Gates**

The following quality gates are mandatory before this Architecture document or any future revision may be approved.

1. Source baseline validation.  
2. Requirement traceability validation.  
3. Architecture scope validation.  
4. Responsibility boundary validation.  
5. Architectural style validation.  
6. Module and layer validation.  
7. Data ownership validation.  
8. Integration boundary validation.  
9. Security architecture validation.  
10. Deployment viability validation.  
11. Operational viability validation.  
12. Constraint validation.  
13. Cross-document consistency review.  
14. Documentation Quality Assurance.  
15. Engineering completeness validation.  
16. Product Owner review.  
17. Product Owner approval.

Failure at any quality gate shall require revision before approval.

---

# **28\. Cross-Document Consistency**

This Architecture document shall remain consistent with all higher-authority approved baselines.

Architecture review shall verify consistency with:

* Engineering Generation Standard;  
* Project Governance;  
* Product Brief;  
* Technical Specification;  
* approved ADRs.

Downstream documents shall be reviewed for consistency with this Architecture, including:

* API and Data Contracts;  
* Testing and Acceptance;  
* Deployment and Operations;  
* Feature Specifications;  
* implementation documentation.

Any contradiction shall be resolved according to normative authority before implementation or release.

---

# **29\. Documentation Quality Assurance**

This Architecture document shall undergo Documentation Quality Assurance before every approval.

DQA shall verify:

* canonical terminology;  
* correct authority;  
* scope ownership;  
* explicit responsibility boundaries;  
* absence of requirement duplication;  
* absence of conflicting architecture statements;  
* verifiable identifiers;  
* requirement lineage;  
* decision traceability;  
* absence of implicit architectural decisions;  
* absence of undocumented assumptions;  
* implementation readiness.

DQA completion shall precede Product Owner review.

---

# **30\. Architecture Completeness Validation**

Before approval, this document shall be validated for:

* completeness;  
* correctness;  
* consistency;  
* maintainability;  
* scalability;  
* traceability;  
* governance compliance;  
* implementation readiness.

The architecture shall be considered implementation-ready only when downstream Feature Specifications and engineering teams can derive their responsibilities without inventing missing architectural decisions.

Detailed contracts, feature behavior, operational commands, and test cases are intentionally delegated to lower-authority documents and do not represent architectural incompleteness.

---

# **31\. Compliance Statement**

This Software Architecture demonstrates conformity with:

* Engineering Generation Standard;  
* Project Governance;  
* Specification-Driven Development;  
* approved Product Brief;  
* approved Technical Specification;  
* approved engineering baselines.

Future architecture revisions shall preserve compatibility with higher-authority documents and shall maintain explicit bidirectional traceability.

No implementation artifact may silently override an approved architectural decision.

---

# **32\. Architecture Requirement Index**

The following Architecture Requirements constitute the approved Architecture Baseline.

## **Architecture Requirements**

| Identifier | Description |
| ----- | ----- |
| AR-001 | Modular Monolith architecture. |
| AR-002 | Explicit module boundaries. |
| AR-003 | Layered responsibility separation. |
| AR-004 | Single deployable application. |
| AR-005 | PostgreSQL as the authoritative relational database. |
| AR-006 | Server-side rendering using Django Templates. |
| AR-007 | Progressive interaction through HTMX and minimal JavaScript. |
| AR-008 | Isolated external integrations. |
| AR-009 | Environment-based configuration. |
| AR-010 | Controlled architectural evolution. |

Architecture Requirement identifiers are canonical and shall remain immutable after approval.

---

## **Architecture Principles**

| Identifier | Description |
| ----- | ----- |
| AP-001 | Modular Monolith First |
| AP-002 | Separation of Concerns |
| AP-003 | High Cohesion |
| AP-004 | Low Coupling |
| AP-005 | Explicit Dependencies |
| AP-006 | Simplicity Before Distribution |
| AP-007 | Security by Design |
| AP-008 | Maintainability by Design |
| AP-009 | Progressive Evolution |
| AP-010 | Specification Before Implementation |

---

## **Architectural Constraints**

| Identifier | Description |
| ----- | ----- |
| AC-001 | Python as the primary implementation language. |
| AC-002 | Django as the primary web framework. |
| AC-003 | Django Templates as the primary rendering mechanism. |
| AC-004 | HTMX as the default progressive interaction mechanism. |
| AC-005 | Minimal client-side JavaScript. |
| AC-006 | PostgreSQL as the production database. |
| AC-007 | Hostinger Linux VPS as the initial deployment platform. |
| AC-008 | Modular Monolith architecture. |
| AC-009 | Single coordinated deployment unit. |
| AC-010 | Controlled architectural change. |
| AC-011 | Mandatory architectural traceability. |
| AC-012 | Architecture proportional to approved requirements. |

---

# **33\. Architecture Decision Traceability**

Every approved Architectural Decision Record (ADR) shall maintain explicit traceability to:

* originating Business Requirements (`BR-*`);  
* originating Technical Requirements (`TR-*`);  
* originating Architecture Requirements (`AR-*`);  
* affected Architecture Principles (`AP-*`);  
* affected Architectural Constraints (`AC-*`);  
* affected modules;  
* affected integrations;  
* affected deployment topology;  
* affected Feature Specifications (`SPEC-*`);  
* affected implementation components.

Decision traceability shall remain bidirectional.

No approved architectural decision shall become orphaned from its originating requirements.

---

# **34\. Document Reference Index**

This Architecture document governs or provides architectural guidance for the following engineering artifacts.

| Engineering Document | Relationship |
| ----- | ----- |
| 00-engineering-generation-standard.md | Governing engineering standard |
| 01-product-brief.md | Business baseline |
| 02-technical-specification.md | Technical baseline |
| ADR Repository | Architecture decisions |
| 04-api-and-data-contracts.md | Architecture input |
| 05-testing-and-acceptance.md | Architecture verification |
| 06-deployment-and-operations.md | Operational realization |
| SPEC Repository | Feature implementation guidance |

All downstream documents shall preserve explicit bidirectional traceability to this Architecture document.

---

# **35\. Document Maintenance**

This Architecture document shall remain synchronized with all approved engineering baselines.

A controlled revision shall be required whenever one or more of the following occurs.

* approval of new Architecture Requirements;  
* approval of a superseding ADR;  
* modification of approved technical requirements;  
* modification of approved business requirements affecting architecture;  
* introduction of new deployment topology;  
* introduction of new architectural style;  
* introduction of new persistent storage technology;  
* introduction of new runtime infrastructure;  
* approval of a revised Engineering Generation Standard.

Architecture modifications shall never occur solely through implementation activities.

---

# **36\. Revision History**

| Version | Status | Summary |
| ----- | ----- | ----- |
| 1.0.0 | Approved Baseline | Initial Software Architecture. |
| 2.0.0 | Approved Baseline | Complete revision aligned with the Engineering Generation Standard (EGS), incorporating normative governance, architecture requirements, architectural principles, canonical identifiers, explicit traceability, DQA, architecture validation, deployment architecture, operational architecture, architecture evolution, ADR governance, and controlled architectural lifecycle. |

Revision history shall preserve complete architectural change traceability.

---

# **37\. Approval**

## **Document Owner**

Architecture & Engineering Review

Responsible for:

* architecture ownership;  
* architecture consistency;  
* architecture governance;  
* engineering quality.

---

## **Architecture Review**

Architecture & Engineering Review

Responsible for:

* Documentation Quality Assurance;  
* architecture traceability verification;  
* cross-document consistency review;  
* architecture completeness validation.

---

## **Approval Authority**

Product Owner

The Product Owner is the sole approval authority for this Architecture document.

No lower-authority engineering document shall supersede this architecture baseline without an approved revision or an approved Architectural Decision Record explicitly modifying the affected architectural decision.

---

# **38\. Final Normative Provision**

This document establishes the official Software Architecture Baseline for the Site Portfolio project.

All downstream engineering artifacts shall preserve explicit traceability to the Architecture Requirements and Architectural Decisions defined herein.

Every engineering activity shall remain consistent with:

* the Engineering Generation Standard (EGS);  
* Project Governance;  
* the approved Product Brief;  
* the approved Technical Specification;  
* this Software Architecture;  
* approved Architectural Decision Records;  
* approved engineering baselines.

Future revisions shall preserve:

* architectural integrity;  
* engineering consistency;  
* responsibility separation;  
* requirement traceability;  
* governance compliance;  
* implementation independence;  
* controlled architectural evolution.

No implementation activity shall modify the approved architecture through source code changes alone.

Material architectural changes shall require:

* documented architectural justification;  
* impact analysis;  
* cross-document consistency review;  
* updated traceability;  
* Product Owner approval.

This document shall remain the authoritative architectural reference for the Site Portfolio project until formally superseded by an approved revision.

