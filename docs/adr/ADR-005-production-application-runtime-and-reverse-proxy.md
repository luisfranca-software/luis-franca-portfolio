\# ADR-005 — Production Application Runtime and Reverse Proxy

| Field | Value |  
|---|---|  
| \*\*Document ID\*\* | ADR-005 |  
| \*\*Decision ID\*\* | ARCH-DEC-005 |  
| \*\*Title\*\* | Production Application Runtime and Reverse Proxy |  
| \*\*Version\*\* | 1.0.0 |  
| \*\*Status\*\* | Approved Baseline |  
| \*\*Decision Status\*\* | Accepted |  
| \*\*Decision Classification\*\* | Production Runtime and Operational Architecture Decision |  
| \*\*Project\*\* | Site Portfolio |  
| \*\*Release\*\* | Release 1 — MVP |  
| \*\*Owner\*\* | Solution Architecture |  
| \*\*Approver\*\* | Product Owner |  
| \*\*Development Model\*\* | Specification-Driven Development (SDD) |  
| \*\*Created\*\* | 2026-08-14 |  
| \*\*Last Updated\*\* | 2026-08-14 |

\---

\# 1\. Purpose

This Architectural Decision Record establishes the production application runtime, process supervision, reverse proxy, static-file delivery, network exposure, and transport-termination architecture for the Site Portfolio Release 1 deployment.

This ADR closes the operational decision gap explicitly identified by ARCH-001 regarding:

\- production application server selection;  
\- application process management;  
\- reverse proxy selection;  
\- application-server network exposure;  
\- static-file delivery responsibility;  
\- HTTP and HTTPS ingress responsibility.

The decisions established herein govern:

\- production application execution;  
\- production process supervision;  
\- production reverse proxy configuration;  
\- static-file delivery;  
\- HTTP and HTTPS ingress;  
\- application-server binding;  
\- service startup and restart behavior;  
\- runtime failure recovery;  
\- operational validation.

This ADR complements ADR-002, ADR-003, ADR-004, ARCH-001, and OPS-001.

It shall not redefine the approved application architecture, business scope, database architecture, transactional-email provider, or Feature Specification behavior.

\---

\# 2\. Normative Authority

This ADR derives its authority from:

\- EGS-001 — Engineering Generation Standard;  
\- PB-001 — Product Brief;  
\- TS-001 — Technical Specification;  
\- ARCH-001 — Software Architecture;  
\- OPS-001 — Deployment and Operations;  
\- TST-001 — Testing and Acceptance;  
\- ADR-001 — Release Strategy;  
\- ADR-002 — Technology Stack;  
\- ADR-003 — Python Runtime and Development Toolchain;  
\- ADR-004 — Transactional Email Integration;  
\- BASELINE-001 — Engineering Documentation Baseline.

ARCH-001 explicitly leaves the production application server and process-management mechanism unresolved pending an approved operational decision.

ADR-005 resolves that decision gap.

No deployment artifact, service definition, reverse-proxy configuration, runtime command, or production procedure shall contradict the decisions established herein.

A material deviation from this ADR requires controlled engineering review and, where architectural consequences exist, an approved revision or superseding ADR.

\---

\# 3\. Context

The approved Release 1 architecture establishes:

\- Python as the backend language;  
\- Django as the web framework;  
\- PostgreSQL as the authoritative relational database;  
\- a Modular Monolith architecture;  
\- a Single Deployable Application;  
\- environment-based configuration;  
\- WSGI and ASGI application entry points;  
\- HTTPS as mandatory for production transport;  
\- controlled deployment and operational procedures.

ADR-003 additionally establishes:

\- Python 3.13 as the approved runtime release line;  
\- Django 5.2 as the approved framework release line;  
\- \`uv\` as the dependency and runtime management solution;  
\- \`pyproject.toml\` and \`uv.lock\` as authoritative dependency artifacts;  
\- reproducible production dependency installation.

The Release 1 deployment environment consists of a single OCI compute instance.

PostgreSQL is deployed locally on that instance and listens only on the loopback interface.

Django static assets are collected through the approved Django \`collectstatic\` mechanism into the configured production \`STATIC\_ROOT\`.

ARCH-001 does not approve a specific:

\- reverse proxy;  
\- WSGI application server;  
\- container runtime;  
\- process supervisor.

ARCH-001 further establishes that the specific application server and process-management mechanism require an approved operational decision.

These decisions shall not originate implicitly from deployment commands or server configuration.

\---

\# 4\. Problem Statement

Django's development server is not an approved production application server.

Release 1 requires an explicitly governed production execution path capable of:

\- running the Django WSGI application;  
\- supervising the application process;  
\- recovering from application-process failure;  
\- starting predictably during server boot;  
\- accepting requests through a controlled ingress layer;  
\- preventing direct public exposure of the application server;  
\- serving collected static assets efficiently;  
\- supporting HTTP-to-HTTPS transition;  
\- supporting TLS termination;  
\- preserving client and proxy protocol information required by Django;  
\- integrating with the existing single-server deployment topology;  
\- minimizing operational complexity.

Without an explicit decision, deployment implementation could introduce arbitrary application servers, process managers, reverse proxies, containers, or public network bindings.

Such implementation-time decisions would violate the project's requirements for:

\- architectural traceability;  
\- controlled evolution;  
\- operational simplicity;  
\- security;  
\- reproducibility;  
\- maintainability.

The production runtime architecture shall therefore conform to the decision established by this ADR.

\---

\# 5\. Decision Drivers

\#\# DD-001 — Architectural Compliance

The solution shall preserve:

\- Modular Monolith architecture;  
\- Single Deployable Application;  
\- Django WSGI compatibility;  
\- PostgreSQL relational persistence;  
\- environment-based configuration.

\#\# DD-002 — Operational Simplicity

Release 1 shall use the smallest operational topology that fully satisfies production requirements.

The solution shall not introduce:

\- orchestration platforms;  
\- distributed application services;  
\- unnecessary container infrastructure;  
\- redundant process managers;  
\- unnecessary network hops.

\#\# DD-003 — Security

The application server shall not be directly exposed to the public Internet.

Database connectivity shall remain private to the server.

TLS shall terminate at a controlled ingress boundary.

\#\# DD-004 — Reliability

The application process shall:

\- start predictably;  
\- restart after process failure;  
\- expose meaningful service status;  
\- integrate with operating-system logging and lifecycle management.

\#\# DD-005 — Maintainability

The production runtime shall use mature components with clearly separated responsibilities.

\#\# DD-006 — Reproducibility

Runtime dependencies and service definitions shall be reproducible and documented.

\#\# DD-007 — Static Asset Delivery

Collected static files shall be served without routing every static request through Django.

\#\# DD-008 — Cost Control

The runtime architecture shall not require additional managed infrastructure or paid platform services for Release 1\.

\---

\# 6\. Constraints

The decision is subject to the following constraints:

\- Release 1 uses Django 5.2;  
\- Release 1 uses Python 3.13;  
\- application dependencies are governed by \`uv\`;  
\- PostgreSQL is deployed locally;  
\- production deployment uses a single OCI compute instance;  
\- application configuration originates from environment-based configuration;  
\- production HTTPS is mandatory;  
\- the production domain and certificate may become available after initial runtime provisioning;  
\- implementation shall remain compatible with the approved Release 1 architecture;  
\- operational complexity shall remain proportional to a personal professional portfolio application.

\---

\# 7\. Alternatives Considered

\#\# 7.1 Alternative A — Django Development Server

\#\#\# Decision

Rejected.

\#\#\# Rationale

Django's development server is intended for development and verification, not as the production application runtime.

Using it in production would fail the project's reliability, security, and operational requirements.

\---

\#\# 7.2 Alternative B — Gunicorn \+ systemd \+ Nginx

\#\#\# Decision

Accepted.

\#\#\# Rationale

This topology provides clear responsibility boundaries:

\- Gunicorn executes the Django WSGI application;  
\- systemd supervises the Gunicorn process;  
\- Nginx provides public HTTP/HTTPS ingress;  
\- Nginx serves static assets;  
\- PostgreSQL remains local and private.

The topology satisfies Release 1 requirements without introducing unnecessary infrastructure.

\---

\#\# 7.3 Alternative C — Gunicorn Exposed Directly to the Internet

\#\#\# Decision

Rejected.

\#\#\# Rationale

Direct public exposure would collapse ingress and application-runtime responsibilities and unnecessarily expose the application server.

It would also complicate:

\- TLS management;  
\- static-file delivery;  
\- request filtering;  
\- transport configuration;  
\- future operational hardening.

\---

\#\# 7.4 Alternative D — Containerized Runtime

\#\#\# Decision

Rejected for Release 1\.

\#\#\# Rationale

Containerization could provide portability and environment isolation, but the current Release 1 deployment does not require container orchestration or image-based deployment.

Introducing Docker or another container runtime at this stage would add:

\- image lifecycle management;  
\- additional deployment artifacts;  
\- additional networking configuration;  
\- additional operational failure modes;  
\- additional maintenance overhead.

The benefit does not currently justify the complexity.

This rejection does not prohibit future adoption through controlled architectural review.

\---

\#\# 7.5 Alternative E — Alternative WSGI Servers

Alternative production-capable WSGI servers are technically possible.

\#\#\# Decision

Not selected.

\#\#\# Rationale

Release 1 requires one standardized runtime path.

Introducing multiple supported application-server options would increase operational variation without providing a demonstrated requirement.

\---

\#\# 7.6 Alternative F — Alternative Reverse Proxies

Alternative reverse proxies are technically possible.

\#\#\# Decision

Not selected.

\#\#\# Rationale

Release 1 requires a stable and minimal ingress architecture.

Maintaining multiple reverse-proxy alternatives would create unnecessary operational variation.

\---

\# 8. Architectural Decision

The Release 1 production request path shall be:

~~~text
Internet
   |
   v
Nginx
:80 / :443
   |
   +---- /static/ ----> STATIC_ROOT
   |
   +---- application requests
                     |
                     v
              127.0.0.1:8000
                     |
                     v
                  Gunicorn
                     |
                     v
               Django WSGI
                     |
                     v
                PostgreSQL
              127.0.0.1:5432
~~~

The approved responsibilities are:

| Component | Responsibility |
|---|---|
| Nginx | Public ingress, reverse proxy, static-file delivery, HTTP/HTTPS handling |
| Gunicorn | Production WSGI application server |
| systemd | Gunicorn process supervision and lifecycle management |
| Django | Application behavior |
| PostgreSQL | Relational persistence |
| `uv` | Python dependency and managed-runtime execution |

No component shall assume responsibilities assigned to another component without approved engineering review.

---

# 9. Gunicorn Application Server Policy

## **9.1 Approved Application Server**

Gunicorn shall be the approved production WSGI application server for Release 1\.

Gunicorn shall execute:

config.wsgi:application

or the equivalent repository-qualified WSGI application path required by the approved project layout.

## **9.2 Dependency Governance**

Gunicorn shall be declared as a project runtime dependency in `pyproject.toml`.

Its resolved version shall be recorded in `uv.lock`.

Gunicorn shall not be installed manually as an unmanaged global Python dependency.

Dependency introduction and future upgrades shall follow ADR-003.

## **9.3 Network Binding**

Gunicorn shall bind only to a loopback interface.

The Release 1 default binding shall be:

127.0.0.1:8000

Gunicorn shall not bind to:

0.0.0.0

or directly to a public network interface.

## **9.4 Public Exposure**

Public firewall or OCI ingress rules shall not expose Gunicorn's application port.

Port `8000` shall not constitute a public application endpoint.

## **9.5 Worker Configuration**

Worker count and timeout values shall be operational configuration.

They shall be selected conservatively according to:

* available compute resources;  
* memory;  
* expected Release 1 traffic;  
* application behavior;  
* observed runtime characteristics.

Release 1 shall not introduce speculative high-concurrency tuning.

## **9.6 Worker Model**

The default Gunicorn synchronous worker model shall be preferred unless measured application requirements justify an alternative.

An alternative worker model shall not be introduced solely for theoretical scalability.

---

# **10\. systemd Process Supervision Policy**

## **10.1 Approved Supervisor**

systemd shall supervise the Gunicorn application process.

A dedicated systemd service shall define the production application lifecycle.

## **10.2 Responsibilities**

systemd shall provide:

* service startup;  
* controlled shutdown;  
* restart behavior;  
* boot-time activation;  
* process status;  
* failure reporting;  
* journal integration.

## **10.3 Service Identity**

The application service shall execute under a non-root operating-system identity.

Gunicorn shall not execute as `root`.

## **10.4 Working Directory**

The service shall execute from the approved production repository/application directory.

The working directory shall be explicit in the service definition.

## **10.5 Environment Configuration**

Production configuration shall originate from the approved environment configuration mechanism.

Secrets shall not be embedded directly into the systemd unit file.

The existing project environment contract shall remain authoritative.

## **10.6 Restart Policy**

The application service shall use a bounded automatic restart policy suitable for recovering from unexpected application-process failure.

Restart behavior shall not create an uncontrolled rapid restart loop.

## **10.7 Boot Behavior**

The application service shall be enabled to start during normal server boot after its required system dependencies are available.

## **10.8 Service Changes**

Changes to the systemd unit shall be treated as deployment configuration changes and shall be validated before production activation.

---

# **11\. Nginx Reverse Proxy Policy**

## **11.1 Approved Reverse Proxy**

Nginx shall be the approved Release 1 public reverse proxy.

## **11.2 Public Ingress**

Nginx shall be the only application-layer service intended to receive public HTTP and HTTPS traffic.

The intended public ports are:

80/tcp  
443/tcp

Public exposure shall remain subject to approved host firewall and OCI network-security configuration.

## **11.3 Reverse Proxy**

Dynamic application requests shall be proxied to:

http://127.0.0.1:8000

## **11.4 Proxy Headers**

Nginx shall forward the request metadata required for correct Django operation behind a reverse proxy.

At minimum, proxy configuration shall preserve:

* original host;  
* client address information;  
* forwarding chain information;  
* original transport protocol.

Header configuration shall remain consistent with Django's approved production security settings.

## **11.5 Direct Application Access**

Nginx shall not proxy requests to a publicly exposed Gunicorn endpoint.

Communication between Nginx and Gunicorn shall remain local to the compute instance.

---

# **12\. Static File Delivery Policy**

## **12.1 Collection**

Django `collectstatic` shall remain responsible for producing the deployment static-file output.

## **12.2 Static Root**

The authoritative collected static directory shall remain the `STATIC_ROOT` defined by the approved Django settings.

For the current Release 1 repository, the deployment output resolves to:

/srv/luis-franca-portfolio/staticfiles/

## **12.3 Serving Responsibility**

Nginx shall serve requests under the configured static URL directly from the collected static directory.

Gunicorn and Django shall not be the primary static-file delivery mechanism in production.

## **12.4 Deployment Sequence**

Static collection shall occur before activation of a release that changes static assets.

A failed static collection shall prevent completion of the affected deployment.

---

# **13\. Media File Policy**

The approved Django configuration defines a media directory.

Release 1 shall not infer additional public media-upload behavior unless explicitly required by an approved Feature Specification.

If media delivery becomes operationally required, its Nginx exposure shall be reviewed against:

* approved product behavior;  
* security requirements;  
* data classification;  
* access requirements.

Static-file policy shall not automatically imply unrestricted media-file exposure.

---

# **14\. Transport Security Policy**

## **14.1 HTTPS**

Production traffic shall use HTTPS in accordance with ARCH-001.

## **14.2 TLS Termination**

Nginx shall terminate public TLS for Release 1\.

Gunicorn shall not independently manage the public TLS certificate.

## **14.3 HTTP Port**

Port `80` may be used for:

* initial HTTP reachability;  
* certificate validation;  
* redirecting HTTP requests to HTTPS.

After HTTPS activation, normal application traffic shall be redirected to HTTPS.

## **14.4 Certificate Activation**

TLS configuration shall be activated only after:

* the production domain resolves correctly;  
* DNS propagation is verified;  
* the server is reachable through the required public ingress;  
* certificate issuance succeeds;  
* HTTPS behavior is validated.

## **14.5 HSTS**

HTTP Strict Transport Security shall not be enabled before HTTPS is fully operational and validated.

After stable HTTPS validation, HSTS may be introduced through controlled hardening.

Initial HSTS activation shall use a deliberate value and shall not include subdomains or preload behavior unless separately justified.

## **14.6 Django Proxy Security**

Django's production proxy-security settings shall remain consistent with TLS termination at Nginx.

The existing approved configuration:

SECURE\_PROXY\_SSL\_HEADER \= ("HTTP\_X\_FORWARDED\_PROTO", "https")

requires Nginx to forward the corresponding protocol information correctly.

---

# **15\. Network Exposure Policy**

The Release 1 production network model shall preserve the following boundaries:

| Service | Binding / Exposure |
| ----- | ----- |
| SSH | Public only as operationally required and restricted by approved network controls |
| Nginx HTTP | Public `80/tcp` |
| Nginx HTTPS | Public `443/tcp` |
| Gunicorn | Loopback `127.0.0.1:8000` only |
| PostgreSQL | Loopback `127.0.0.1:5432` only |

No OCI ingress rule or host-firewall rule shall expose PostgreSQL or Gunicorn publicly.

---

# **16\. Database Boundary**

ADR-005 does not change PostgreSQL architecture.

PostgreSQL shall remain:

* the authoritative relational database;  
* locally reachable by the Django application;  
* unavailable through public ingress;  
* accessed through the dedicated application database role;  
* governed by ARCH-001, ADR-002, ADR-003, and OPS-001.

Nginx and Gunicorn shall not require direct database administration privileges.

---

# **17\. Environment and Secret Management**

Production configuration shall continue to follow AR-009 and ADR-003.

Secrets shall not be:

* committed to Git;  
* embedded in Nginx configuration;  
* embedded in systemd unit files;  
* hardcoded in Gunicorn commands;  
* written into application source code.

The production environment configuration shall remain outside version control.

Sensitive environment files shall use restrictive filesystem permissions.

Application runtime services shall receive only the configuration required to execute the application.

---

# **18\. Logging and Observability**

## **18.1 Application Process**

Gunicorn process output and errors shall be available through systemd journal integration unless an approved logging configuration establishes another destination.

## **18.2 Reverse Proxy**

Nginx shall maintain operational access and error logging using the operating system's approved Nginx logging mechanism.

## **18.3 Application Logging**

Django application logging shall remain governed by the approved application settings and OPS-001.

## **18.4 Sensitive Data**

Logs shall not intentionally contain:

* database passwords;  
* SMTP credentials;  
* Django secret keys;  
* complete secret environment values;  
* unnecessary sensitive contact content.

## **18.5 Validation**

Operational validation shall include the ability to inspect:

* Gunicorn service status;  
* Gunicorn service logs;  
* Nginx service status;  
* Nginx error logs;  
* HTTP response behavior.

---

# **19\. Service Startup and Dependency Order**

The production runtime shall support predictable startup after server reboot.

The intended lifecycle is:

Operating System  
     |  
     \+--\> PostgreSQL  
     |  
     \+--\> Nginx  
     |  
     \+--\> Gunicorn / Django

The systemd service definition shall express only dependencies required for correct runtime behavior.

Artificial ordering dependencies shall not be introduced where service readiness does not require them.

A server reboot shall not require manual application-process startup under normal operating conditions.

---

# **20\. Deployment Sequence**

A normal Release 1 application deployment shall follow a controlled sequence consistent with OPS-001.

The operational sequence shall include, where applicable:

1. verify deployment prerequisites;  
2. synchronize approved source revision;  
3. synchronize locked dependencies;  
4. validate environment configuration;  
5. run applicable Django checks;  
6. review and apply approved database migrations;  
7. collect static assets;  
8. restart or reload the application service;  
9. validate Gunicorn service health;  
10. validate Nginx configuration;  
11. validate reverse-proxy behavior;  
12. perform application smoke tests;  
13. verify logs;  
14. record deployment evidence.

A failed mandatory step shall stop progression until the failure is understood and resolved.

---

# **21\. Failure and Recovery Policy**

## **21.1 Gunicorn Failure**

Unexpected Gunicorn process failure shall be handled by the systemd restart policy.

Persistent failure shall require operational investigation.

## **21.2 Nginx Failure**

Nginx configuration shall be syntax-validated before reload or restart.

A configuration failing validation shall not replace a known-working active configuration.

## **21.3 Database Failure**

Database failure remains governed by OPS-001 and PostgreSQL operational procedures.

## **21.4 Deployment Failure**

Deployment failure shall not be masked by repeated uncontrolled restarts.

Logs and service status shall remain available for diagnosis.

---

# **22\. Security Requirements**

The production runtime shall satisfy the following mandatory requirements:

* Gunicorn shall not execute as root;  
* Gunicorn shall not be publicly exposed;  
* PostgreSQL shall not be publicly exposed;  
* secrets shall remain outside version control;  
* Nginx shall be the controlled public HTTP/HTTPS boundary;  
* HTTPS shall be mandatory for normal production traffic after certificate activation;  
* secure Django cookie settings shall remain enabled in production;  
* proxy headers shall be explicitly controlled;  
* HSTS shall not be enabled prematurely;  
* unnecessary public ports shall remain closed;  
* runtime dependencies shall remain governed by `pyproject.toml` and `uv.lock`;  
* deployment configuration changes shall remain reviewable;  
* service logs shall not intentionally expose secrets.

---

# **23\. Performance and Capacity Policy**

Release 1 shall favor conservative runtime configuration over speculative optimization.

Gunicorn worker count, request timeout, connection behavior, and Nginx limits shall be adjusted only when supported by:

* resource constraints;  
* observed traffic;  
* measured latency;  
* operational evidence;  
* security requirements.

Release 1 shall not introduce:

* horizontal application scaling;  
* external load balancing;  
* distributed caching;  
* asynchronous worker infrastructure;  
* application clustering

without an approved requirement and architecture review.

---

# **24\. Operational Simplicity**

The approved production runtime consists of:

* one OCI compute instance;  
* one Nginx reverse proxy;  
* one systemd-supervised Gunicorn application service;  
* one Django Modular Monolith;  
* one local PostgreSQL instance.

This topology is intentionally minimal.

Additional infrastructure shall not be introduced without a demonstrated requirement.

---

# **25\. Verification and Quality Gates**

Compliance with this ADR shall be objectively verifiable.

Applicable evidence shall include:

* Gunicorn declared in `pyproject.toml`;  
* Gunicorn resolved in `uv.lock`;  
* successful locked dependency synchronization;  
* Gunicorn binding only to loopback;  
* systemd service enabled and active;  
* Gunicorn running under a non-root identity;  
* Nginx configuration syntax validation;  
* Nginx active service status;  
* static files available through Nginx;  
* dynamic requests proxied successfully to Django;  
* PostgreSQL remaining bound to loopback;  
* Gunicorn application port unavailable through public ingress;  
* Django production system checks passing;  
* applicable deployment checks reviewed;  
* application smoke tests passing;  
* repository working tree remaining controlled;  
* HTTPS validation after certificate activation.

A mandatory failed verification shall prevent the affected deployment stage from being considered complete.

---

# **26\. Acceptance Criteria**

ADR-005 implementation shall be considered operationally accepted when all applicable criteria below are satisfied.

## **AC-001 — Application Server**

Gunicorn successfully executes the approved Django WSGI application.

## **AC-002 — Private Binding**

Gunicorn listens only on the approved loopback endpoint.

## **AC-003 — Process Supervision**

systemd successfully starts, stops, restarts, and reports the application service.

## **AC-004 — Boot Persistence**

The application service is enabled for normal system boot.

## **AC-005 — Reverse Proxy**

Nginx successfully proxies application requests to Gunicorn.

## **AC-006 — Static Files**

Nginx serves collected static assets from the approved `STATIC_ROOT`.

## **AC-007 — Database Isolation**

PostgreSQL remains unavailable through public network exposure.

## **AC-008 — Application Isolation**

Gunicorn remains unavailable through public network exposure.

## **AC-009 — Django Validation**

Production Django system checks complete successfully, except for explicitly documented staged hardening warnings that depend on later deployment milestones.

## **AC-010 — TLS**

After domain availability, valid HTTPS is established through Nginx.

## **AC-011 — HTTP Redirect**

After TLS activation, normal HTTP application requests redirect to HTTPS.

## **AC-012 — Runtime Recovery**

Unexpected Gunicorn process termination results in controlled systemd recovery according to the approved restart policy.

## **AC-013 — Repository Integrity**

Deployment-specific secrets and generated runtime artifacts do not become unintended Git changes.

---

# **27\. Consequences**

## **27.1 Positive Consequences**

The decision provides:

* explicit production-runtime governance;  
* separation between public ingress and application execution;  
* private application-server binding;  
* private database binding;  
* efficient static-file delivery;  
* operating-system-native process supervision;  
* predictable service lifecycle;  
* support for HTTPS termination;  
* straightforward operational diagnostics;  
* minimal infrastructure;  
* low operational cost;  
* compatibility with the existing Release 1 architecture.

## **27.2 Negative Consequences**

The decision introduces:

* Nginx configuration maintenance;  
* systemd service configuration maintenance;  
* Gunicorn as an additional runtime dependency;  
* additional operational logs;  
* explicit TLS configuration responsibilities;  
* an additional local network hop between Nginx and Gunicorn.

These consequences are accepted because they provide the required production reliability and security without disproportionate complexity.

---

# **28\. Requirement and Decision Traceability**

## **28.1 Business Requirements**

Applicable business requirements include those governing:

* production availability;  
* professional user experience;  
* maintainability;  
* future controlled evolution.

## **28.2 Technical Requirements**

Applicable technical requirements include those governing:

* engineering traceability;  
* architecture consistency;  
* environment-based configuration;  
* security by default;  
* maintainability;  
* portability;  
* deployment readiness;  
* automated verification where feasible.

## **28.3 Architecture Requirements**

Applicable architecture requirements include:

* AR-001 — Modular Monolith;  
* AR-004 — Single Deployable Application;  
* AR-005 — Relational Persistence;  
* AR-009 — Environment-Based Configuration;  
* AR-010 — Controlled Architectural Evolution.

## **28.4 Architectural Decisions**

ADR-005:

* preserves ADR-001;  
* preserves ADR-002;  
* implements runtime policies consistently with ADR-003;  
* does not modify ADR-004;  
* resolves the application-server and process-management decision gap explicitly retained by ARCH-001.

## **28.5 Downstream Artifacts**

The following artifacts shall conform to this ADR where applicable:

* `pyproject.toml`;  
* `uv.lock`;  
* production systemd service definition;  
* Nginx site configuration;  
* OCI ingress configuration;  
* host firewall configuration;  
* production deployment procedures;  
* TLS configuration;  
* operational validation evidence;  
* future CI/CD deployment automation.

---

# **29\. Cross-Document References**

This ADR shall be interpreted together with:

* EGS-001 — Engineering Generation Standard;  
* PB-001 — Product Brief;  
* TS-001 — Technical Specification;  
* ARCH-001 — Software Architecture;  
* ADC-001 — API and Data Contracts;  
* TST-001 — Testing and Acceptance;  
* OPS-001 — Deployment and Operations;  
* ADR-001 — Release Strategy;  
* ADR-002 — Technology Stack;  
* ADR-003 — Python Runtime and Development Toolchain;  
* ADR-004 — Transactional Email Integration;  
* SPEC-001 — MVP Foundation;  
* SPEC-002 — Contact & Communication;  
* SPEC-003 — Portfolio & Projects;  
* BASELINE-001 — Engineering Documentation Baseline.

No lower-authority deployment artifact shall redefine the architecture established herein.

---

# **30\. Implementation Boundaries**

ADR-005 authorizes implementation of the selected runtime topology.

It does not itself define final environment-specific values such as:

* production domain name;  
* certificate paths;  
* final worker count;  
* final timeout values;  
* OCI security-rule identifiers;  
* host-specific service usernames;  
* host-specific filesystem permissions beyond required security constraints.

Such values shall be determined during deployment according to:

* actual infrastructure state;  
* approved operational requirements;  
* least-privilege principles;  
* measured resource constraints.

Environment-specific implementation choices shall not contradict this ADR.

---

# **31\. Change-Control Policy**

The following changes are material and require Architecture & Engineering Review:

* replacement of Gunicorn;  
* replacement of Nginx;  
* replacement of systemd as application-process supervisor;  
* public exposure of Gunicorn;  
* public exposure of PostgreSQL;  
* introduction of containerized production execution;  
* introduction of an external load balancer;  
* introduction of multiple application instances;  
* migration to distributed application deployment;  
* relocation of TLS termination to another infrastructure layer.

Where a material change alters the approved architectural decision, an approved ADR revision or superseding ADR is required.

Operational tuning that preserves the approved architecture may proceed through controlled deployment maintenance.

---

# **32\. Future Review Triggers**

This ADR shall be reviewed when any of the following occurs:

* application traffic materially exceeds single-instance capacity;  
* OCI topology changes;  
* container deployment becomes an approved requirement;  
* external load balancing becomes necessary;  
* application-server replacement is proposed;  
* reverse-proxy replacement is proposed;  
* TLS termination moves outside Nginx;  
* horizontal scaling becomes necessary;  
* observability requirements exceed the current operating-system logging model;  
* a revised architecture invalidates assumptions in this ADR;  
* EGS-001 or another higher-authority baseline changes its normative requirements.

---

# **33\. Supersession Policy**

This ADR shall remain authoritative while its status is `Approved Baseline` and its decision status is `Accepted`.

It shall remain authoritative until:

* superseded by an approved Architectural Decision Record;  
* superseded by an approved revision of ADR-005;  
* formally retired through the controlled lifecycle established by EGS-001.

Implementation changes shall not implicitly supersede this ADR.

---

# **34\. Approval Statement**

ADR-005 version 1.0.0 constitutes the approved architectural decision governing the Release 1 production application runtime, process supervision, reverse proxy, static-file delivery, network exposure, and TLS termination architecture.

The Product Owner approval establishes that:

* Gunicorn is the approved Release 1 production WSGI application server;  
* systemd is the approved application process supervisor;  
* Nginx is the approved production reverse proxy and static-file server;  
* Gunicorn shall remain bound to the loopback interface;  
* PostgreSQL shall remain bound to the loopback interface;  
* Nginx shall constitute the controlled public HTTP/HTTPS ingress boundary;  
* public TLS shall terminate at Nginx;  
* HSTS shall remain deferred until stable HTTPS operation has been validated;  
* containerization and distributed runtime infrastructure remain outside the approved Release 1 deployment topology.

This approval closes the application-server, process-supervision, reverse-proxy, and public-ingress decision gaps retained by ARCH-001.

ADR-005 is incorporated into the Release 1 engineering governance as an approved architectural decision.

All Release 1 implementation, deployment, verification, production operation, and maintenance activities affected by this decision shall comply with ADR-005 while it remains authoritative.

---

# **35\. Document Status**

| Field | Value |
| ----- | ----- |
| Document ID | ADR-005 |
| Decision ID | ARCH-DEC-005 |
| Version | 1.0.0 |
| Status | **Approved Baseline** |
| Decision Status | **Accepted** |
| Classification | Architectural Decision Record |
| Authority | Product Owner Approved |
| Applies To | Release 1 — MVP |
| Effective Date | 2026-08-14 |
| Next Review | Upon a material production-runtime architecture change or an applicable governance trigger |

---

# **36\. Revision History**

| Version | Date | Status | Description |
| ----- | ----- | ----- | ----- |
| 1.0.0 | 2026-08-14 | Approved Baseline | Initial architectural decision approved by the Product Owner, establishing Gunicorn as the Release 1 production WSGI application server, systemd as the application process supervisor, Nginx as the reverse proxy and static-file server, loopback-only application and database bindings, Nginx TLS termination, operational verification requirements, and controlled runtime evolution. |

---

# **37\. Final Normative Provision**

ADR-005 version 1.0.0 establishes the authoritative Release 1 production application-runtime and reverse-proxy architecture.

All affected implementation, deployment, infrastructure, verification, operational, and maintenance artifacts shall remain consistent with this decision.

Application-server selection, process supervision, public ingress, static-file delivery, network exposure, and TLS termination shall not evolve through undocumented implementation or server changes.

Material changes shall follow:

**Requirement → Impact Analysis → Architecture Review → Decision → Implementation → Verification → Validation → Approval → Release**

No deviation from this ADR shall be considered approved unless processed through the controlled engineering governance established by EGS-001.

---

# **End of Document**

