# **ADR-002 — Technology Stack**

**Document ID:** ADR-002

**Decision ID:** ARCH-DEC-002

**Version:** 1.0.0

**Status:** Approved Baseline

**Decision Status:** Accepted

**Decision Classification:** Strategic Technology Decision

**Project:** Site Portfolio

**Owner:** Architecture & Engineering Review

**Approver:** Product Owner

**Development Model:** Specification-Driven Development (SDD)

---

# **1\. Purpose**

This Architectural Decision Record establishes the official Technology Stack governing the implementation, deployment, maintenance, and future evolution of the Site Portfolio platform.

The objective of this decision is to define a coherent, maintainable, production-ready technology baseline aligned with the project's business objectives, engineering principles, and long-term architectural vision.

---

# **2\. Decision Context**

The project requires a technology stack capable of:

* supporting rapid MVP delivery;  
* demonstrating professional Python engineering practices;  
* preserving architectural simplicity;  
* enabling long-term evolution;  
* minimizing operational complexity;  
* supporting future Artificial Intelligence capabilities.

Technology selection shall prioritize engineering suitability rather than technology popularity.

---

# **3\. Decision Drivers**

## **Business Drivers**

* Professional credibility.  
* Recruiter confidence.  
* Low operational cost.  
* Long-term sustainability.

## **Engineering Drivers**

* Python-first implementation.  
* Maintainable Modular Monolith.  
* High productivity.  
* Mature ecosystem.  
* Strong security model.  
* Production readiness.

## **Governance Drivers**

* Compliance with EGS-001.  
* Compliance with approved Architecture.  
* Controlled evolution.  
* Specification-Driven Development.

---

# **4\. Considered Alternatives**

## **Alternative A — Flask**

### **Advantages**

* Lightweight.  
* Minimal overhead.

### **Disadvantages**

* Requires additional architectural composition.  
* Larger integration effort.  
* More infrastructure decisions.

Result

Rejected.

---

## **Alternative B — FastAPI**

### **Advantages**

* Excellent API performance.  
* Modern asynchronous architecture.  
* Outstanding API development experience.

### **Disadvantages**

* Does not naturally satisfy the project's server-rendered website architecture.  
* Introduces unnecessary complexity for the MVP.

Result

Rejected.

---

## **Alternative C — Django**

### **Advantages**

* Complete web framework.  
* Mature ecosystem.  
* Excellent security.  
* Integrated authentication.  
* ORM.  
* Administration framework.  
* Native internationalization.  
* Long-term maintainability.

### **Disadvantages**

* Larger framework footprint.

Result

Approved.

---

# **5\. Architectural Decision**

The Site Portfolio platform shall adopt the following official technology stack.

## **Backend**

* Python  
* Django

---

## **Frontend**

* Django Templates  
* HTMX

JavaScript shall remain minimal and shall be introduced only where HTMX cannot adequately satisfy functional requirements.

---

## **Database**

Development

* PostgreSQL

Production

* PostgreSQL

Database portability shall be preserved through the Django ORM.

---

## **Architecture**

The application shall adopt:

* Modular Monolith Architecture.

Modules shall remain loosely coupled while sharing a unified deployment model.

---

## **Hosting**

Production environment:

* Hostinger VPS.

Infrastructure shall remain compatible with future migration to equivalent VPS providers if required.

---

## **Email Strategy**

The platform shall adopt:

* Transactional Email.

Email services shall be used for:

* contact requests;  
* quotation requests;  
* platform notifications.

Marketing automation remains outside the current architectural scope.

---

## **Internationalization**

The platform shall implement:

* Native Django Internationalization (i18n).

Supported languages:

* English (default)  
* Brazilian Portuguese

English shall remain the canonical source language.

---

## **File Storage**

Static and media files shall initially be stored within the hosting infrastructure.

The architecture shall preserve future migration capability to external object storage without architectural redesign.

---

# **6\. Decision Constraints**

The following constraints are mandatory.

* Python is the exclusive backend language.  
* Django shall remain the primary web framework.  
* Django Templates and HTMX shall constitute the presentation layer.  
* PostgreSQL shall remain the official database platform.  
* The architecture shall remain a Modular Monolith.  
* Infrastructure shall target Hostinger VPS.

Technology substitutions require a new approved Architectural Decision Record.

---

# **7\. Engineering Assumptions**

The following assumptions support this decision.

* MVP delivery remains the primary short-term objective.  
* Hosting requirements remain compatible with a VPS environment.  
* Expected traffic does not justify distributed architecture.  
* Django satisfies present and planned functional requirements.

If these assumptions become invalid, this ADR shall be reviewed.

---

# **8\. Impact Assessment**

## **Business Impact**

Positive.

The selected stack reinforces the professional image of the platform while reducing operational risk.

---

## **Architecture Impact**

Positive.

The selected technologies fully support the approved Modular Monolith Architecture.

---

## **Documentation Impact**

Positive.

Technology decisions remain centralized within this ADR, avoiding duplication across engineering documents.

---

## **Implementation Impact**

Positive.

The selected stack provides rapid development, mature tooling, and simplified maintenance.

---

## **Operations Impact**

Positive.

Deployment, monitoring, backup, and maintenance remain compatible with a single VPS environment.

---

# **9\. Success Criteria**

This decision shall be considered successful when:

* Release 1 is implemented without technology replacement.  
* The approved architecture remains stable.  
* No framework migration is required during Releases 1 or 1.1.  
* Future Release 2 capabilities can be incorporated without architectural redesign.

---

# **10\. Consequences**

This decision establishes the official technology baseline.

All future engineering documentation, Feature Specifications, implementation activities, deployment procedures, and operational processes shall conform to the technology stack defined herein.

Technology deviations shall require explicit architectural approval.

---

# **11\. Requirement Traceability**

## **Originating Business Requirements**

* PB-OBJ-001 — Professional positioning.  
* PB-SCP-001 — MVP implementation.

## **Originating Technical Requirements**

* TS-NFR-001 — Maintainability.  
* TS-NFR-002 — Scalability.  
* TS-NFR-003 — Security.  
* TS-NFR-004 — Extensibility.

## **Originating Architectural Decisions**

* ARCH-DEC-002 — Official Technology Stack.

---

# **12\. Cross-Document References**

This decision is governed by:

* EGS-001 — Engineering Generation Standard.  
* PB-001 — Product Brief.  
* TS-001 — Technical Specification.  
* ARCH-001 — Software Architecture.

This decision shall be referenced by:

* SPEC-001 — MVP Foundation.  
* SPEC-002 — Contact & Communication.  
* SPEC-003 — Portfolio & Projects.

Future Feature Specifications shall inherit this technology baseline unless superseded by an approved ADR.

---

# **13\. Compliance**

This document has been produced in accordance with:

* Engineering Generation Standard (EGS-001);  
* Documentation Quality Assurance (DQA);  
* Engineering Compliance Verification (ECV);  
* Cross-Document Review;  
* Engineering Completeness Validation (ECV-2);  
* Engineering Quality Gates;  
* Specification-Driven Development (SDD).

No conflict with approved engineering baselines has been identified.

---

# **14\. Future Review Triggers**

This ADR shall be reviewed whenever one or more of the following conditions occur:

* replacement of the primary web framework;  
* replacement of the database platform;  
* migration to a distributed architecture;  
* replacement of the hosting strategy;  
* adoption of a different frontend architecture;  
* introduction of new infrastructure constraints.

---

# **15\. Supersession Policy**

This ADR remains authoritative until:

* superseded by another approved Architectural Decision Record;  
* formally retired through the controlled document lifecycle defined by EGS-001.

No engineering document may define or recommend technologies that conflict with this ADR while it remains in Approved Baseline status.

---

# **16\. Approval Statement**

This Architectural Decision Record establishes the official Technology Stack baseline for the Site Portfolio project.

All future engineering documentation, Feature Specifications, implementation activities, testing procedures, deployment workflows, operational processes, and architectural evolution shall comply with this decision unless formally superseded through the approved engineering governance process.

