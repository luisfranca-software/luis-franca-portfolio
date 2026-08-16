# Production Recovery Runbook

| Field | Value |
|---|---|
| Document ID | RUNBOOK-001 |
| Title | Production Recovery Runbook |
| Version | 1.0.0 |
| Status | Approved Operational Procedure |
| Project | Site Portfolio |
| Release | Release 1 — MVP |
| Environment | Production |
| Owner | Operations Engineering |
| Development Model | Specification-Driven Development (SDD) |
| Governing Requirement | OPS-001 / OR-006 |
| Governing Decision | ADR-005 |
| Last Updated | 2026-08-16 |

---

# 1. Purpose

This runbook defines the approved minimum recovery procedures for the Site Portfolio Release 1 production environment.

It exists to satisfy OPS-001 OR-006 — Recovery procedures shall be documented.

This runbook shall not redefine architecture, feature behavior, database contracts, deployment topology, or security requirements.

Recovery activities shall preserve the approved engineering baseline and shall prefer restoration of the known-good production state over undocumented operational changes.

---

# 2. Scope

This runbook governs recovery for:

- Gunicorn / Django application-process failure;
- Nginx configuration or service failure;
- production environment-configuration failure;
- host-firewall configuration failure;
- TLS / certificate operational failure;
- PostgreSQL service failure;
- transactional-email integration failure;
- failed application deployment;
- production infrastructure replacement.

This runbook does not establish:

- database backup frequency;
- backup retention periods;
- Recovery Point Objective (RPO);
- Recovery Time Objective (RTO);
- unverified PostgreSQL restoration procedures;
- disaster-recovery infrastructure not implemented in Release 1.

Such capabilities require separate implementation and validation before they may be treated as operationally available.

---

# 3. Normative References

This runbook shall be interpreted together with:

- EGS-001 — Engineering Generation Standard;
- TS-001 — Technical Specification;
- ARCH-001 — Software Architecture;
- OPS-001 — Deployment and Operations;
- TST-001 — Testing and Acceptance;
- ADR-003 — Python Runtime and Development Toolchain;
- ADR-004 — Transactional Email Integration;
- ADR-005 — Production Application Runtime and Reverse Proxy;
- BASELINE-001 — Engineering Documentation Baseline.

Primary traceability:

OPS-001 / OR-006
→ OP-004 Recoverability
→ OA-005 Backup and Recovery
→ ADR-005 Failure and Recovery Policy
→ RUNBOOK-001
→ Operational Recovery Evidence

---

# 4. Approved Production Topology

The Release 1 production runtime is:

Internet
→ Nginx :80 / :443
→ Gunicorn 127.0.0.1:8000
→ Django WSGI
→ PostgreSQL 127.0.0.1:5432

Operational services include:

- `nginx.service`;
- `luis-franca-portfolio.service`;
- `postgresql.service`;
- `netfilter-persistent.service`;
- `certbot.timer`.

Gunicorn shall execute under the non-root `ubuntu` operating-system identity.

Production application configuration shall remain in:

`/srv/luis-franca-portfolio/.env`

The file shall remain outside Git and protected with restrictive filesystem permissions.

---

# 5. General Recovery Preconditions

Before performing recovery:

1. identify the failed component;
2. inspect service status and recent logs;
3. preserve the current failure evidence where practical;
4. avoid changing multiple components simultaneously;
5. validate configuration syntax before activation where supported;
6. prefer restart or rollback to a known-good configuration over speculative modification;
7. never expose Gunicorn or PostgreSQL publicly as a recovery shortcut;
8. never place production secrets in Git, command output, logs, or documentation;
9. record materially significant recovery actions.

Recovery shall stop and require engineering review when the failure cannot be explained by the approved architecture or known operational configuration.

---

# 6. Application Service Recovery

## 6.1 Detection

Inspect:

```bash
systemctl status luis-franca-portfolio.service --no-pager -l
journalctl -u luis-franca-portfolio.service -n 100 --no-pager

6.2 Automatic Recovery
The application service uses:
Restart=on-failure
RestartSec=5s
Unexpected Gunicorn master-process termination is expected to trigger controlled automatic recovery through systemd.
This behavior was validated in production by controlled unexpected termination:
original master PID: 10085;
process termination: SIGKILL;
failure result: signal;
restart counter: 0 → 1;
recovered master PID: 13417;
recovered state: active/running;
application socket restored at 127.0.0.1:8000;
HTTPS validation returned 200.
6.3 Manual Recovery
If automatic recovery does not restore service after diagnosis:
sudo systemctl restart luis-franca-portfolio.service
systemctl status luis-franca-portfolio.service --no-pager -l
Validate:
sudo ss -lntp | grep ':8000'
curl -I https://luisfranca.com.br/
Expected result:
Gunicorn listening only on 127.0.0.1:8000;
HTTPS application response successful.
Repeated uncontrolled restart attempts are prohibited.

7. Nginx Recovery
Inspect:
systemctl status nginx --no-pager -l
sudo nginx -t
sudo tail -n 100 /var/log/nginx/error.log
A configuration failing nginx -t shall not be reloaded.
Known configuration backups may be used to restore the last known-good state when applicable.
After correction:
sudo nginx -t
sudo systemctl reload nginx
Validate:
curl -I https://luisfranca.com.br/
curl -I https://www.luisfranca.com.br/
curl -I https://luisfranca.com.br/static/css/site.css
Unknown hosts shall continue to be rejected by the Nginx default-deny configuration.

8. Environment Configuration Recovery
Production configuration is externalized in:
/srv/luis-franca-portfolio/.env
A pre-Brevo operational backup currently exists as:
/srv/luis-franca-portfolio/.env.pre-brevo.bak
Configuration restoration shall preserve:
DJANGO_SECRET_KEY;
approved DJANGO_ALLOWED_HOSTS;
PostgreSQL connectivity;
Brevo SMTP credentials;
sender and notification addresses;
public professional-link configuration;
restrictive file permissions.
Validate permissions:
stat -c '%A %a %U %G %n' /srv/luis-franca-portfolio/.env
Expected:
600 ubuntu ubuntu
After configuration recovery:
DJANGO_SETTINGS_MODULE=config.settings.production \
uv run python backend/manage.py check

sudo systemctl restart luis-franca-portfolio.service
Secrets shall never be copied into version-controlled files.

9. Firewall Recovery
The authoritative persistent IPv4 rules are:
/etc/iptables/rules.v4
The required production ingress policy permits:
TCP 22;
TCP 80;
TCP 443;
before the terminal INPUT reject rule.
Gunicorn port 8000 and PostgreSQL port 5432 shall not be publicly opened.
Validate:
sudo iptables-restore --test < /etc/iptables/rules.v4
sudo iptables -L INPUT -n --line-numbers
systemctl is-active netfilter-persistent.service
The production firewall persistence was validated through a controlled server reboot.

10. TLS and Certificate Recovery
Inspect:
sudo nginx -t
sudo certbot certificates
systemctl status certbot.timer --no-pager
Validate external HTTPS:
curl -I https://luisfranca.com.br/
curl -I https://www.luisfranca.com.br/
Certificate renewal capability has been validated through:
sudo certbot renew --dry-run
A certificate or Nginx TLS failure shall be diagnosed before manually replacing certificate files.
Private keys under /etc/letsencrypt/ shall not be copied into the repository or operational documentation.

11. PostgreSQL Recovery
Inspect:
systemctl status postgresql --no-pager -l
sudo pg_lsclusters
sudo ss -lntp | grep ':5432'
The approved production database shall remain available only through loopback.
Service-level recovery may use:
sudo systemctl restart postgresql
followed by:
DJANGO_SETTINGS_MODULE=config.settings.production \
uv run python backend/manage.py check
11.1 Database Restore Limitation
Release 1 does not currently possess validated database-backup restoration evidence within this runbook.
No database backup shall be classified as operationally valid until restoration capability has been objectively verified in accordance with OPS-001.
Database corruption, data loss, or restoration requirements shall therefore trigger controlled engineering intervention rather than an unverified restore procedure.

12. Transactional Email Recovery
The production transactional-email provider is Brevo SMTP.
Approved runtime configuration includes:
SMTP host smtp-relay.brevo.com;
port 587;
TLS enabled;
authenticated SMTP login;
verified sender contato@luisfranca.com.br;
externalized SMTP key;
configured notification recipient.
If email delivery fails:
verify application logs;
verify Brevo service/account status;
validate DNS authentication records if relevant;
validate environment configuration without displaying credentials;
perform an isolated Django SMTP test before repeating a public contact submission.
External integration failure shall not be addressed by hardcoding credentials or bypassing the approved notifier integration.

13. Failed Deployment Recovery
If an application deployment fails:
stop progression;
identify the failed mandatory deployment stage;
preserve logs and failure evidence;
do not repeatedly restart services to mask the failure;
evaluate rollback versus forward recovery;
restore a known-good source revision when rollback is selected;
synchronize locked dependencies;
validate environment configuration;
review migration implications before changing database state;
run applicable Django checks;
collect static assets when required;
restart application service;
validate Nginx;
perform production smoke tests;
record recovery evidence.
A Git rollback shall not automatically imply a database rollback.
Database migrations shall be assessed independently before any schema reversal.

14. Infrastructure Replacement
If the OCI compute instance must be replaced, recovery shall reconstruct only the approved Release 1 topology:
one OCI compute instance;
Nginx public ingress;
systemd-supervised Gunicorn;
Django application;
local PostgreSQL;
persistent host firewall;
Certbot-managed TLS;
environment-based configuration.
Infrastructure replacement shall require restoration of approved source, dependencies, production configuration, DNS/network access, database state, TLS capability, and external integration configuration.
Because a complete infrastructure-replacement drill has not been executed, this procedure is documented but not classified as fully validated disaster recovery.

15. Recovery Validation
After any recovery affecting production runtime, validate as applicable:
DJANGO_SETTINGS_MODULE=config.settings.production \
uv run python backend/manage.py check

systemctl is-active postgresql
systemctl is-active luis-franca-portfolio
systemctl is-active nginx
systemctl is-active netfilter-persistent

sudo nginx -t
sudo ss -lntp | grep -E ':80|:443|:8000|:5432'

curl -I https://luisfranca.com.br/
curl -I https://www.luisfranca.com.br/
For contact/integration recovery, validate /contact/ and SMTP behavior as appropriate.
Recovery shall not be considered complete until the affected production capability is operationally validated.

16. Evidence Requirements
Material recovery actions shall record:
date and time;
affected release;
affected environment;
affected component;
failure condition;
recovery action;
validation performed;
final outcome;
residual risk, if any.
Critical operational incidents shall follow OPS-001 incident-management requirements.

17. Stop and Escalation Conditions
Stop recovery and require engineering review when:
an approved architecture boundary must be violated to restore service;
data integrity cannot be confirmed;
a database restore is required without validated restoration evidence;
secrets may have been exposed;
repeated service failures exceed the bounded restart policy;
TLS/private-key integrity is uncertain;
infrastructure replacement requires an architectural change;
recovery would require an undocumented production shortcut.

18. Known Limitations
The following limitations are explicitly acknowledged for Release 1:
no validated PostgreSQL backup/restore drill is recorded by this runbook;
no tested full OCI instance-replacement drill is recorded;
no automated multi-region or high-availability recovery exists;
no container or orchestration-based recovery exists;
Release 1 uses a single-instance production topology.
These limitations do not redefine the approved Release 1 architecture.
They shall be evaluated through future operational evolution according to actual risk and approved requirements.

19. Traceability Matrix
Requirement / Decision
Runbook Coverage
OPS-001 OR-006
Entire document
OPS-001 OP-004
Sections 5–18
OPS-001 OA-005
Sections 6–18
OPS-001 13.4 Rollback Readiness
Section 13
OPS-001 16 Backup Strategy
Sections 11 and 18
OPS-001 17 Recovery Strategy
Sections 5–18
OPS-001 21 Incident Management
Sections 16–17
OPS-001 23 Operational Documentation
Entire document
ADR-005 10.6 Restart Policy
Section 6
ADR-005 21 Failure and Recovery Policy
Sections 6–13
ADR-005 AC-012 Runtime Recovery
Section 6
ADR-004 Transactional Email Integration
Section 12


20. Operational Status
The following recovery capabilities have objective production evidence:
Capability
Status
Gunicorn automatic process recovery
Validated
Gunicorn manual service restart
Validated
Production reboot persistence
Validated
Nginx syntax validation and reload
Validated
Firewall persistence after reboot
Validated
TLS certificate issuance
Validated
TLS automatic-renewal simulation
Validated
Brevo SMTP delivery
Validated
Contact E2E delivery
Validated
PostgreSQL service restart
Documented; full data restoration not validated
Database backup restoration
Not validated
Complete OCI infrastructure replacement
Not validated


21. Approval and Maintenance
This runbook shall remain version controlled.
Changes affecting architecture shall require Architecture & Engineering Review.
Operational updates that preserve the approved architecture shall follow OPS-001 change governance.
The document shall be reviewed when:
production topology changes;
recovery procedures materially change;
a backup/restore capability is introduced or validated;
TLS management changes;
transactional-email provider changes;
a material incident identifies a recovery deficiency.

22. Revision History
Version
Date
Status
Description
1.0.0
2026-08-16
Approved Operational Procedure
Initial Release 1 production recovery runbook satisfying OPS-001 OR-006 and recording validated and non-validated recovery capabilities.


End of Document

