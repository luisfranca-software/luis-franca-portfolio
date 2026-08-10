\# ADR-004 — Transactional Email Integration (Brevo SMTP)

| Field | Value |  
|-------|-------|  
| \*\*Document ID\*\* | ADR-004 |  
| \*\*Title\*\* | Transactional Email Integration (Brevo SMTP) |  
| \*\*Version\*\* | 1.0.0 |  
| \*\*Status\*\* | Approved Baseline |
| \*\*Owner\*\* | Solution Architecture |  
| \*\*Approver\*\* | Product Owner |  
| \*\*Project\*\* | Site Portfolio |  
| \*\*Release\*\* | Release 1 — MVP |  
| \*\*Engineering Process\*\* | Specification-Driven Development (SDD) |  
| \*\*Classification\*\* | Architectural Decision Record |  
| \*\*Created\*\* | 2026-08-10 |  
| \*\*Last Updated\*\* | 2026-08-10 |

\---

\# 1\. Purpose

This Architectural Decision Record (ADR) formally establishes the official transactional email strategy for the Site Portfolio platform, the approved integration provider, the isolation model applied to external communication services, the environment-based configuration model, and the contact request data handling policy.

The objective of this document is to complete the architectural decision required by \*\*SPEC-002 — Contact & Communication\*\* before the implementation of the Contact module proceeds, in full compliance with the approved engineering governance.

This ADR complements \*\*ADR-002 — Technology Stack\*\* and shall govern the implementation of the Contact module defined in \*\*SPEC-002 — Contact & Communication\*\*.

It does not replace or modify the approved technology stack.

\---

\# 2\. Context

The approved engineering documentation defines:

\- Product objectives;  
\- Technical requirements;  
\- Software architecture;  
\- API and data contracts;  
\- Testing strategy;  
\- Deployment model;  
\- Release strategy;  
\- Technology stack.

\*\*ADR-002 — Technology Stack\*\* establishes that the platform shall adopt transactional email for:

\- contact requests;  
\- quotation requests;  
\- platform notifications;

and that marketing automation remains outside the current architectural scope.

\*\*ARCH-001 — Software Architecture\*\* establishes the integration constraints that govern external communication services:

\- §14.4 — the Contact module may own contact form processing, contact request validation, contact request persistence, contact notification workflows and submission status handling, while transactional email provider behavior shall remain in the Integrations Layer;  
\- §16.1 — application workflows shall depend on internal integration contracts rather than provider-specific client behavior when provider replaceability or isolated testing is required;  
\- §16.2 — the transactional email integration shall account for provider configuration, sender identity, destination configuration, timeout behavior, delivery failure, provider unavailability, logging without exposing sensitive content and test substitution, and the specific provider shall be documented through an ADR or integration contract before implementation;  
\- §15.7 — detailed privacy and retention rules for personally identifiable information require explicit project policy or lower-level specification.

\*\*SPEC-002 — Contact & Communication\*\* establishes that:

\- §5 SPEC-002-REQ-005 — successful submissions shall generate transactional email notifications to the platform owner;  
\- §7 — the communication workflow shall persist the request, send the transactional email and then display a success confirmation, and failures shall present user-friendly messages without exposing internal implementation details;  
\- §14 — no implementation shall introduce external communication services without an approved Architectural Decision Record.

An architectural gap was identified during the implementation planning of SPEC-002.

Although the approved documentation establishes the transactional email strategy and its isolation constraints, no approved document names the concrete transactional email provider, defines the environment-based configuration contract, or defines the contact request data retention policy.

This omission is intentional.

ARCH-001 §16.2 explicitly defers the provider selection to an Architectural Decision Record or integration contract.

ARCH-001 §15.7 explicitly defers retention rules to project policy or lower-level specification.

\---

\# 3\. Problem Statement

The Contact module of SPEC-002 must generate transactional email notifications for contact and quotation requests without:

\- introducing external communication services without an approved Architectural Decision Record;  
\- coupling application workflows to a provider-specific client;  
\- committing credentials or sensitive configuration to source control;  
\- defining retention or purge behavior for contact request data without explicit project policy.

This ADR resolves the provider selection, the integration isolation model, the configuration contract and the data retention policy in a single controlled decision.

\---

\# 4\. Decision Drivers

\#\# DD-001 — Compliance with Engineering Governance

The selected strategy shall remain fully compliant with:

\- EGS-001 — Engineering Generation Standard;  
\- Approved Engineering Baseline;  
\- Approved Architectural Decisions;  
\- SPEC-002 — Contact & Communication.

\---

\#\# DD-002 — Provider Replaceability

The integration shall preserve the ability to substitute the transactional email provider without architectural redesign, as required by ARCH-001 §16.1 and §13.3.

\---

\#\# DD-003 — Security

Configuration shall remain environment-based.

Secrets and email provider credentials shall never be committed to source control.

\---

\#\# DD-004 — Maintainability

The integration shall minimize implementation surface area and operational complexity while fully satisfying SPEC-002 requirements.

\---

\#\# DD-005 — Reliability

Delivery failure and provider unavailability shall not produce uncontrolled application failure, in compliance with ARCH-001 §16.4 and §22.3.

Submitted requests shall be retained for later processing when notification delivery fails.

\---

\#\# DD-006 — Testability

The integration shall support isolated testing through test substitution, as required by ARCH-001 §16.2.

\---

\#\# DD-007 — Data Protection

Contact request data constitutes personally identifiable information and shall be subject to:

\- data minimization;  
\- limited logging;  
\- defined retention;  
\- controlled deletion.

\---

\# 5\. Alternatives Considered

The following alternatives were evaluated.

\#\# 5\.1 Option A — Brevo SMTP Relay

Deliver transactional email through the Brevo (formerly Sendinblue) SMTP relay using Django's built-in SMTP email backend.

Advantages:

\- uses the approved Django technology stack without additional runtime dependencies;  
\- provider-specific behavior is confined to configuration and a thin integration adapter;  
\- standard STARTTLS transport;  
\- provider replaceability preserved because the application depends on an internal contract;  
\- minimal integration surface and operational complexity.

Disadvantages:

\- depends on an external provider for deliverability;  
\- sender reputation management remains external.

\---

\#\# 5\.2 Option B — Brevo Transactional API (HTTP)

Deliver transactional email through the Brevo Transactional Email HTTP API using the provider SDK.

Advantages:

\- richer provider capabilities (templates, tracking, webhooks).

Disadvantages:

\- introduces a provider-specific SDK runtime dependency;  
\- requires a custom email backend or direct client integration, increasing coupling;  
\- increases integration surface and maintenance burden;  
\- reduces provider replaceability;  
\- exceeds the current SPEC-002 scope.

\---

\#\# 5\.3 Option C — Generic SMTP without a defined provider

Deliver transactional email through Django's SMTP backend without defining a concrete provider.

Disadvantages:

\- violates ARCH-001 §16.2, which requires the specific provider to be documented before implementation;  
\- leaves sender identity, deliverability and operational configuration undefined.

\---

\# 6\. Decision

The platform shall adopt the following architectural decisions for transactional email and contact data handling.

\---

\#\# 6\.1 Decision — Transactional Email Provider

The official transactional email provider shall be \*\*Brevo\*\*, delivered through the Brevo SMTP relay using Django's built-in SMTP email backend.

Provider facts:

\- provider: Brevo (formerly Sendinblue);  
\- transport: SMTP;  
\- host: \`smtp-relay.brevo.com\`;  
\- port: \`587\` with STARTTLS;  
\- authentication: SMTP login and SMTP key supplied exclusively through environment configuration.

Transactional email shall be used for contact requests and quotation requests as approved by SPEC-002.

\---

\#\# 6\.2 Decision — Integration Isolation

Transactional email provider behavior shall remain in the Integrations Layer, isolated behind an internal integration contract, in compliance with ARCH-001 §14.4, §16.1 and AR-008.

The Contact module shall define the integration contract as a protocol with a single notification operation.

Application workflows shall depend only on that contract.

The concrete SMTP adapter shall:

\- construct the notification from the persisted contact request;  
\- map provider and transport failures to a controlled integration error;  
\- log failures without exposing sensitive content or request content;  
\- never expose provider credentials to application code or presentation.

\---

\#\# 6\.3 Decision — Environment-Based Configuration

Transactional email and contact configuration shall be environment-based.

The following environment variables are established without default secrets:

\- \`EMAIL_BACKEND\` — the Django email backend class;  
\- \`EMAIL_HOST\` — the SMTP relay host (Brevo);  
\- \`EMAIL_PORT\` — the SMTP relay port;  
\- \`EMAIL_HOST_USER\` — the SMTP login;  
\- \`EMAIL_HOST_PASSWORD\` — the SMTP key;  
\- \`EMAIL_USE_TLS\` — enable STARTTLS;  
\- \`DEFAULT_FROM_EMAIL\` — the sender identity;  
\- \`CONTACT_NOTIFICATION_EMAIL\` — the platform owner notification recipient;  
\- \`CONTACT_RETENTION_DAYS\` — the contact request retention period in days.

Credentials shall never be committed to source control.

\---

\#\# 6\.4 Decision — Contact Request Data Retention

Contact requests constitute personally identifiable information and shall be retained for \*\*90 days\*\* by default.

Retention behavior:

\- retention begins at the submission timestamp;  
\- retention is configurable through \`CONTACT_RETENTION_DAYS\`;  
\- expired contact requests shall be deleted by the approved purge mechanism;  
\- purge execution shall be explicit and operator-triggered through a management command;  
\- purge shall be deterministic and idempotent.

This decision establishes the explicit project policy required by ARCH-001 §15.7.

\---

\#\# 6\.5 Decision — Communication Model

The Contact module shall persist each submission with:

\- communication type — \*\*CONTACT\*\* (general contact) or \*\*QUOTATION\*\* (budget request);  
\- processing status — \*\*RECEIVED\*\*, \*\*NOTIFIED\*\* or \*\*NOTIFICATION_FAILED\*\*.

Status semantics:

\- \*\*RECEIVED\*\* — the request has been persisted;  
\- \*\*NOTIFIED\*\* — the transactional email notification was delivered successfully;  
\- \*\*NOTIFICATION_FAILED\*\* — the request is persisted but the notification could not be delivered; the request remains retained for later processing.

\---

\# 7\. Consequences

Positive consequences:

\- SPEC-002 §14 constraint is satisfied through a formally approved Architectural Decision Record;  
\- application workflows remain provider-agnostic, preserving replaceability;  
\- credentials remain outside version control;  
\- delivery failures degrade gracefully without uncontrolled application failure;  
\- contact request data is subject to defined retention and controlled deletion;  
\- provider-specific behavior is confined to the Integrations Layer.

Negative consequences:

\- Brevo becomes an operational dependency for notification delivery;  
\- deliverability depends on external sender reputation;  
\- contact request data is deleted after the retention period, requiring operator-initiated purge;  
\- retention and purge behavior require operational discipline to remain effective.

\---

\# 8\. Traceability

\#\#\# Business Requirements

\- PB/BR-004 — The product shall facilitate professional contact.

\#\#\# Technical Requirements

\- TS-001 TC-001 — Support multilingual content;  
\- TS-001 TC-004 — Support persistent data management;  
\- TS-001 TC-005 — Support external service integrations;  
\- TS-001 NFR-003 — Maintainability;  
\- TS-001 NFR-009 — Extensibility;  
\- TS-001 SEC-001 — Input validation;  
\- TS-001 SEC-002 — Output encoding;  
\- TS-001 SEC-003 — Protection of sensitive configuration through environment-based configuration;  
\- TS-001 SEC-008 — Secure handling of user-supplied information;  
\- TS-001 ES-005 — Configuration shall be environment-based.

\#\#\# Architectural Requirements

\- ARCH-DEC-001 — Incremental Release Strategy;  
\- ARCH-DEC-002 — Official Technology Stack;  
\- ARCH-001 §14.4 — Contact module responsibilities;  
\- ARCH-001 §15.7 — Personally identifiable information handling;  
\- ARCH-001 §16.1 — Integration boundary;  
\- ARCH-001 §16.2 — Transactional email integration;  
\- ARCH-001 §16.4 — Integration failure handling;  
\- ARCH-001 §22.3 — Graceful degradation;  
\- AR-008 — Isolated external integrations.

\#\#\# Feature Specifications

\- SPEC-002-REQ-001 — public contact form;  
\- SPEC-002-REQ-003 — quotation request option;  
\- SPEC-002-REQ-005 — transactional email notifications;  
\- SPEC-002-REQ-006 — contact request persistence;  
\- SPEC-002-REQ-007 — persistent floating WhatsApp entry point;  
\- SPEC-002-REQ-008 — LinkedIn and GitHub navigation;  
\- SPEC-002-REQ-009 — resume download;  
\- SPEC-002 §7 — communication workflow;  
\- SPEC-002 §8 — data requirements;  
\- SPEC-002 §9 — security requirements;  
\- SPEC-002 §14 — implementation constraints.

\#\#\# Architectural Decision Records

\- ADR-002 §5 — Email Strategy;  
\- ADR-002 §5 — Internationalization.

Decision traceability shall remain bidirectional.

\---

\# 9\. Cross-Document References

This ADR relates to:

\- EGS-001 — Engineering Generation Standard;  
\- PB-001 — Product Brief;  
\- TS-001 — Technical Specification;  
\- ARCH-001 — Software Architecture;  
\- ADC-001 — API and Data Contracts;  
\- TST-001 — Testing and Acceptance;  
\- OPS-001 — Deployment and Operations;  
\- ADR-001 — Release Strategy;  
\- ADR-002 — Technology Stack;  
\- ADR-003 — Python Runtime and Development Toolchain;  
\- SPEC-001 — MVP Foundation;  
\- SPEC-002 — Contact & Communication;  
\- SPEC-003 — Portfolio & Projects;  
\- BASELINE-001 — Engineering Documentation Baseline.

\---

\# 10\. Compliance

This Architectural Decision Record has been produced in accordance with:

\- Engineering Generation Standard (EGS-001);  
\- Specification-Driven Development (SDD);  
\- Documentation Quality Assurance (DQA);  
\- Engineering Compliance Verification (ECV);  
\- Cross-Document Review;  
\- Engineering Completeness Validation (ECV-2);  
\- Engineering Quality Gates;  
\- Product Owner Review;  
\- Product Owner Approval.

\#\# SPEC-002 Compliance

The email provider decision satisfies the mandatory constraint of SPEC-002 §14:

\- "No implementation shall introduce external communication services without an approved Architectural Decision Record."

\#\# ARCH-001 Compliance

The integration isolation decision satisfies the mandatory constraint of ARCH-001 §16.2:

\- "The specific provider shall be documented through an ADR or integration contract before implementation."

The data retention decision provides the explicit project policy required by ARCH-001 §15.7.

No conflict with approved engineering baselines has been identified.

\---

\# 11\. Approval Statement

This Architectural Decision Record has been approved by the Product Owner according to the Engineering Generation Standard.

The Product Owner approval records the following:

\- Brevo is the approved transactional email provider for Release 1;  
\- the integration shall be isolated behind an internal integration contract;  
\- configuration shall remain environment-based with no credentials committed;  
\- contact request data shall be retained for 90 days by default and purged through the approved purge mechanism.

This document is an approved architectural decision governing Release 1 and constitutes part of the official engineering baseline defined in BASELINE-001.

Implementation activities shall comply with the decisions established herein.

No implementation shall intentionally deviate from this Architectural Decision Record without prior architectural approval.

\---

\# 12\. Document Status

| Field | Value |  
|--------|-------|  
| Document ID | ADR-004 |  
| Version | 1.0.0 |  
| Status | \*\*Approved Baseline\*\* |
| Classification | Architectural Decision Record |  
| Authority | Engineering Baseline |  
| Applies To | Release 1 — MVP |  
| Next Review | Upon architectural change affecting email delivery, integration isolation, configuration or data retention |

\---

\# 13\. Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0.0 | 2026-08-10 | Solution Architecture | Initial issue of the Architectural Decision Record (Proposed). |
| 1.0.0 | 2026-08-10 | Product Owner | Approved Baseline status granted; Brevo SMTP transactional email integration, integration isolation, environment-based configuration and 90-day contact request retention approved; approval recorded and inclusion in BASELINE-001 confirmed. |

\---

\# End of Document
