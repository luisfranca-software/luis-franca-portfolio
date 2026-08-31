# ADR-006 — Knowledge Base, Embeddings and Vector Retrieval Architecture

| Field | Value |
|---|---|
| **Document ID** | ADR-006 |
| **Decision ID** | ARCH-DEC-006 |
| **Title** | Knowledge Base, Embeddings and Vector Retrieval Architecture |
| **Version** | 1.0.0 |
| **Status** | Approved Baseline |
| **Decision Status** | Accepted |
| **Decision Classification** | AI/RAG Data, Embedding and Retrieval Architecture Decision |
| **Project** | Site Portfolio |
| **Release** | Release 2 — Platform Evolution |
| **Owner** | Solution Architecture |
| **Approver** | Product Owner |
| **Development Model** | Specification-Driven Development (SDD) |
| **Created** | 2026-08-31 |
| **Last Updated** | 2026-08-31 |

---

# 1. Purpose

This Architectural Decision Record establishes the architecture for the Release 2 Knowledge Base, embedding generation, vector persistence, semantic retrieval, indexing lifecycle, metadata filtering, and external embedding-provider integration.

This ADR resolves the material architectural decisions required to introduce Retrieval-Augmented Generation (RAG) into the existing Site Portfolio architecture without creating a separate distributed data platform.

The decisions established herein govern:

- Knowledge Base ownership and persistence;
- document and chunk responsibility boundaries;
- embedding-provider selection;
- embedding-provider isolation;
- embedding dimensionality;
- vector-storage technology;
- similarity strategy;
- retrieval strategy;
- metadata-filtering strategy;
- indexing and reindexing lifecycle;
- database transaction boundaries;
- failure handling;
- operational provisioning of pgvector;
- security and secret-management boundaries;
- testing and validation expectations;
- future provider/model replacement.

This ADR does not define:

- the public AI assistant user interface;
- LLM answer-generation behavior;
- final conversational prompt design;
- conversation persistence;
- public chat endpoints;
- streaming behavior;
- production assistant UX.

Those responsibilities belong to subsequent Release 2 specifications and implementation scope.

---

# 2. Normative Authority

This ADR derives its authority from:

- EGS-001 — Engineering Generation Standard;
- PB-001 — Product Brief;
- TS-001 — Technical Specification;
- ARCH-001 — Software Architecture;
- ADC-001 — API and Data Contracts;
- TST-001 — Testing and Acceptance;
- OPS-001 — Deployment and Operations;
- ADR-001 — Release Strategy;
- ADR-002 — Technology Stack;
- ADR-003 — Python Runtime and Development Toolchain;
- ADR-004 — Transactional Email Integration;
- ADR-005 — Production Application Runtime and Reverse Proxy;
- approved Release 2 Product Owner decisions;
- existing approved engineering baselines.

ARCH-001 requires material technology decisions to evaluate functional fit, architectural consistency, security, maintainability, testability, performance, scalability, operational complexity, deployment impact, cost, vendor dependency, migration consequences, and technical debt. It also requires ADRs to preserve upstream authority and traceability. :contentReference[oaicite:1]{index=1}

ADR-002 establishes PostgreSQL and the Modular Monolith as part of the approved technology baseline and requires future Release 2 capabilities to evolve without unnecessary architectural redesign. :contentReference[oaicite:2]{index=2}

ADR-003 establishes `pyproject.toml` and `uv.lock` as the authoritative dependency-management artifacts and preserves PostgreSQL/Psycopg within the approved Python/Django engineering stack. :contentReference[oaicite:3]{index=3}

ADR-005 confirms the production application topology remains a single Django deployment backed by PostgreSQL and shall not be implicitly redefined by unrelated architecture changes. :contentReference[oaicite:4]{index=4}

---

# 3. Context

Release 2 introduces a controlled Knowledge Base and Retrieval-Augmented Generation capability for the Site Portfolio.

The approved product direction requires:

- administrator-managed knowledge;
- persistent structured metadata;
- normalized and chunked knowledge;
- vector embeddings;
- PostgreSQL-based vector persistence;
- metadata-constrained semantic retrieval;
- controlled context supplied to the future AI assistant;
- EN and PT-BR support;
- provider isolation;
- no unnecessary dedicated vector infrastructure.

The existing architecture is a Django Modular Monolith using PostgreSQL as the authoritative database.

The repository discovery performed before this ADR found:

- no existing Knowledge Base application;
- no existing AI/RAG application module;
- no existing embedding provider;
- no installed vector Python dependency;
- no OpenAI dependency;
- no existing vector schema requiring migration compatibility;
- no conflicting legacy RAG implementation.

The discovery audit also confirmed that the repository was clean and synchronized before Release 2 Day 3 implementation work began. :contentReference[oaicite:5]{index=5}

Infrastructure verification subsequently established:

- local development uses PostgreSQL 18.6;
- production OCI uses PostgreSQL 16.15;
- the corresponding pgvector operating-system package is available for each PostgreSQL major version;
- local pgvector 0.8.1 has been installed and enabled successfully;
- the Django application connection can read and use the PostgreSQL `vector` type;
- production pgvector provisioning is operationally feasible but remains intentionally unapplied until controlled deployment.

Therefore, PostgreSQL + pgvector is technically feasible without introducing a second database platform.

---

# 4. Problem Statement

The system requires semantic retrieval over a small, curated professional Knowledge Base.

The architecture must satisfy the following simultaneously:

1. preserve the existing Django Modular Monolith;
2. reuse PostgreSQL where technically appropriate;
3. support vector similarity search;
4. support EN and PT-BR content;
5. constrain retrieval using relational metadata;
6. isolate third-party embedding-provider dependencies;
7. maintain low operating cost;
8. avoid unnecessary infrastructure;
9. allow deterministic testing;
10. preserve explicit failure states;
11. support future embedding-provider/model replacement;
12. prepare controlled context for the future IA Jujuju assistant.

A solution that introduces a dedicated vector database, asynchronous worker infrastructure, or self-hosted ML runtime without objective necessity would increase deployment, maintenance, testing, security, and operational complexity disproportionate to the expected corpus and traffic.

---

# 5. Affected Requirements

This ADR affects Release 2 requirements concerning:

- Knowledge Base administration;
- knowledge persistence;
- normalization and chunking;
- embedding generation;
- vector persistence;
- metadata filtering;
- semantic retrieval;
- controlled context;
- RAG;
- AI-provider isolation;
- multilingual retrieval;
- operational deployment;
- testing;
- security;
- observability;
- cost control.

Downstream requirements shall be refined in SPEC-004 — Knowledge Base and Retrieval.

---

# 6. Constraints

The decision is governed by the following constraints.

## 6.1 Architectural Constraints

The solution shall:

- remain within the Django Modular Monolith;
- preserve PostgreSQL as the primary persistent database;
- avoid direct presentation-layer calls to external AI SDKs;
- isolate external provider dependencies;
- avoid unnecessary distributed-system components;
- remain compatible with the existing production topology.

## 6.2 Product Constraints

The initial corpus is expected to be small and curated.

The initial access pattern is expected to be sporadic rather than high-volume.

The system shall support:

- English;
- Brazilian Portuguese;
- metadata-constrained retrieval;
- administrator-controlled activation and deactivation.

## 6.3 Operational Constraints

Development and production currently use different PostgreSQL major versions:

- development: PostgreSQL 18;
- production: PostgreSQL 16.

The vector implementation shall therefore use capabilities supported in both environments.

pgvector installation requires privileged database/operating-system provisioning and shall not require promoting the Django application user to PostgreSQL superuser.

## 6.4 Schedule Constraint

Release 1.1 and Release 2 are governed by a maximum five-working-day delivery window.

Architecture sophistication shall therefore remain proportional to actual requirements.

---

# 7. Evaluated Alternatives

## 7.1 Dedicated Vector Database

Examples include:

- Pinecone;
- Qdrant;
- Weaviate;
- similar dedicated vector platforms.

### Benefits

- specialized vector-search features;
- high-scale ANN capabilities;
- independently scalable vector workload.

### Costs

- additional infrastructure;
- separate credentials;
- additional backup/recovery concerns;
- network dependency;
- operational monitoring;
- synchronization complexity;
- additional failure modes;
- possible recurring service cost;
- unnecessary architectural distribution.

### Assessment

Rejected for the initial Release 2 scope.

The expected corpus and traffic do not justify a dedicated vector database.

---

## 7.2 PostgreSQL Without pgvector

Potential representations include:

- JSON arrays;
- numeric arrays;
- serialized vectors;
- application-side similarity calculations.

### Benefits

- no database extension dependency.

### Costs

- weaker query semantics;
- custom similarity logic;
- reduced database optimization;
- greater application complexity;
- poor long-term maintainability;
- does not implement the approved vector-storage requirement appropriately.

### Assessment

Rejected.

---

## 7.3 PostgreSQL + pgvector

### Benefits

- reuses approved PostgreSQL infrastructure;
- native vector data type;
- native similarity operators;
- relational metadata and vector retrieval in one query path;
- transaction compatibility;
- no second database;
- low operational overhead;
- proven local feasibility;
- production package availability confirmed.

### Costs

- requires PostgreSQL extension provisioning;
- vector schema depends on embedding dimensions;
- model/dimension changes require controlled reindexing.

### Assessment

Accepted.

---

# 8. Embedding Provider Alternatives

The following provider categories were evaluated:

- OpenAI managed embeddings;
- Google managed embeddings;
- Voyage AI;
- Cohere;
- self-hosted/open-weight embedding models.

The evaluated criteria included:

- multilingual capability;
- integration complexity;
- operational cost;
- provider isolation;
- deployment impact;
- quality suitable for professional RAG;
- expected traffic;
- schedule;
- infrastructure burden.

Self-hosted embedding models were rejected for the initial release because they would introduce model-runtime, memory, CPU, package, deployment, security, and operational responsibilities disproportionate to the expected corpus and traffic.

Specialized external embedding providers remain viable future alternatives but would not materially improve the initial operational simplicity of the project.

---

# 9. Decision

## 9.1 Knowledge Base Architecture

The Knowledge Base shall be implemented as a dedicated Django application boundary within the existing Modular Monolith.

The initial persistent domain shall consist of two principal entities:

- `KnowledgeDocument`;
- `KnowledgeChunk`.

`KnowledgeDocument` shall represent administrator-controlled source knowledge.

`KnowledgeChunk` shall represent system-derived retrievable segments and their vector embeddings.

The system shall not introduce a separate Knowledge Base database.

---

## 9.2 Vector Storage

PostgreSQL with pgvector is the approved vector-storage technology.

The initial vector field shall use:

`vector(1024)`

The Python integration shall use the maintained `pgvector` package with Django support.

The implementation shall not introduce an unrelated `django-pgvector` dependency when the official `pgvector` package satisfies the requirement.

---

## 9.3 Embedding Provider

OpenAI is the approved initial managed embedding provider.

The approved initial embedding model is:

`text-embedding-3-small`

The approved embedding dimensionality is:

`1024`

The embedding provider shall be isolated behind an application-owned contract.

No model, view, Django Admin class, template, or retrieval consumer shall directly depend on the OpenAI SDK when that dependency can be isolated in the integration boundary.

A conceptual provider contract shall support at minimum:

- document embedding;
- query embedding.

Provider-specific authentication, retries, timeout handling, serialization, and error translation shall remain inside the concrete provider implementation.

---

# 10. Provider Replaceability

The initial OpenAI selection shall not establish OpenAI as a permanent domain dependency.

The architecture shall permit future replacement by another compatible provider without redesigning:

- KnowledgeDocument;
- KnowledgeChunk ownership;
- retrieval consumers;
- IA Jujuju domain behavior.

Changing embedding model, provider, dimensionality, or semantically incompatible embedding configuration shall require:

1. explicit configuration/architecture review;
2. schema compatibility assessment;
3. controlled reindexing;
4. retrieval validation;
5. deployment planning.

Fake or deterministic embeddings may be used in automated tests only.

Fake embeddings shall never be persisted or represented as production embeddings.

---

# 11. Similarity and Retrieval Strategy

Cosine similarity is the approved initial similarity strategy.

Retrieval shall use exact vector search.

ANN indexes such as:

- HNSW;
- IVFFlat;

shall not be introduced initially.

The expected corpus does not justify ANN complexity.

ANN adoption requires measured evidence showing that exact search no longer meets approved performance requirements.

The initial retrieval result count shall default to a small controlled `top_k`, initially targeted at approximately five results, subject to SPEC-004 acceptance testing.

A hard semantic-distance threshold shall not be adopted without retrieval-quality evidence.

---

# 12. Metadata Filtering

Semantic similarity shall not replace domain filtering.

Retrieval shall support relational filtering before or together with vector ordering.

Initial mandatory metadata constraints include:

- document active state;
- language.

Additional controlled metadata such as category may be used where required by SPEC-004.

Known domain attributes shall use typed relational columns rather than an unrestricted JSON structure when their meaning and filtering requirements are known.

The architecture shall preserve the principle:

> presence in PostgreSQL does not imply authorization for RAG retrieval.

Operational, private, or unrelated application data shall not become Knowledge Base content automatically.

---

# 13. Knowledge Data Model Responsibilities

## 13.1 KnowledgeDocument

`KnowledgeDocument` shall own administrator-authored source knowledge and operational indexing metadata.

The model is expected to include responsibility for:

- title;
- stable identifier/slug where required;
- language;
- category;
- source content;
- active state;
- indexing status;
- index version;
- embedding model identity;
- indexed timestamp;
- sanitized last indexing error;
- creation timestamp;
- update timestamp.

The exact schema and constraints shall be defined by SPEC-004.

## 13.2 KnowledgeChunk

`KnowledgeChunk` shall own derived retrieval data.

Its responsibilities include:

- parent document reference;
- deterministic sequence;
- chunk content;
- vector embedding;
- persistence metadata required by SPEC-004.

Chunks are system-derived data.

They shall not become the primary administrator-authored content authority.

---

# 14. Indexing Lifecycle

The initial indexing lifecycle shall use explicit states:

- `PENDING`;
- `INDEXING`;
- `INDEXED`;
- `FAILED`.

Indexing shall be synchronous for the initial Release 2 corpus.

No Celery, Redis queue, distributed worker, or broker shall be introduced for the initial implementation.

A reindex operation shall conceptually perform:

1. obtain approved document content;
2. normalize content;
3. generate deterministic chunks;
4. request embeddings from the external provider;
5. validate provider response;
6. begin a short database transaction;
7. atomically replace the derived chunk set;
8. update indexing metadata;
9. commit;
10. expose the new index as valid.

External network calls shall not be performed inside a long-running database transaction.

---

# 15. Existing-Index Preservation

When reindexing an already indexed document, provider or preprocessing failure shall not unnecessarily destroy the last valid index.

The architecture shall prefer:

1. preparation of new chunks;
2. successful generation and validation of new embeddings;
3. atomic replacement of the old chunk set.

The final implementation shall ensure that failed reindexing does not silently expose partially updated vector data.

---

# 16. Chunking Strategy

Chunking shall initially be:

- deterministic;
- provider-independent;
- paragraph-aware;
- sentence-boundary-aware where practical;
- suitable for EN and PT-BR;
- independently testable.

The initial algorithm may use bounded character-oriented sizing rather than provider-specific tokenization.

Provider-specific tokenizer dependencies shall not be introduced unless retrieval evaluation demonstrates a concrete need.

Exact target and overlap values shall be specified and validated in SPEC-004.

The chunking design shall avoid systematic:

- mid-sentence truncation;
- extremely small fragments;
- unnecessarily large chunks;
- nondeterministic output.

---

# 17. Configuration

Provider credentials and operational configuration shall be environment-based.

The implementation shall support configuration equivalent to:

- `OPENAI_API_KEY`;
- embedding model;
- embedding dimensions;
- provider timeout;
- bounded provider batch size where applicable.

Secrets shall not be:

- committed to Git;
- stored in source files;
- displayed in Django Admin;
- emitted in application logs;
- exposed to templates or client-side code.

The embedding dimension is a schema-level architectural constraint.

Environment configuration shall not be permitted to silently select a dimension incompatible with the persisted vector schema.

---

# 18. Failure Handling

The embedding integration shall distinguish transient and permanent failures.

Relevant failure categories include:

- provider timeout;
- temporary provider unavailability;
- rate limiting;
- authentication failure;
- invalid provider response;
- incorrect embedding count;
- incorrect vector dimensions;
- configuration error;
- database persistence failure.

Retries shall be:

- bounded;
- applied only to appropriate transient failures;
- implemented outside long database transactions.

Permanent configuration or validation failures shall not be retried blindly.

Failure reporting shall be operationally useful while sanitizing provider and security details.

---

# 19. Security and Privacy

Knowledge Base content shall be explicitly curated.

The following application data shall not be automatically indexed merely because it exists in PostgreSQL:

- contact requests;
- visitor analytics;
- credentials;
- secrets;
- environment configuration;
- operational logs;
- unrelated administrative data;
- private internal records.

External embedding requests shall send only the content required to generate embeddings.

Provider credentials shall remain server-side.

The Django application user shall not be promoted to PostgreSQL superuser for pgvector provisioning.

The architecture shall preserve least privilege.

---

# 20. Observability

Indexing operations shall expose sufficient operational evidence to diagnose failures.

Appropriate observability includes:

- document identifier;
- indexing start/end;
- result state;
- chunk count;
- provider/model identifier;
- elapsed duration;
- sanitized error category.

The system shall not log:

- API keys;
- authorization headers;
- complete embedding vectors;
- unnecessary full source content.

Retrieval observability may record:

- execution duration;
- result count;
- requested `top_k`;
- non-sensitive filter metadata.

---

# 21. Operational Provisioning

pgvector is an infrastructure prerequisite.

The operating-system package shall correspond to the installed PostgreSQL major version.

Validated environment mapping:

- local PostgreSQL 18 → `postgresql-18-pgvector`;
- production PostgreSQL 16 → `postgresql-16-pgvector`.

The database extension shall be enabled by a privileged PostgreSQL operator:

`CREATE EXTENSION vector;`

The ordinary Django database user shall not require PostgreSQL superuser privilege.

Application migrations relying on vector fields shall execute only after pgvector has been provisioned for the target database.

Production provisioning shall be executed through controlled deployment procedures and shall not occur implicitly during application request handling.

---

# 22. Python Dependencies

The implementation may introduce the minimum required dependencies:

- `pgvector`;
- `openai`.

Dependency declarations shall be recorded in `pyproject.toml`.

Resolved dependency versions shall be recorded in `uv.lock`.

No unrelated RAG framework such as LangChain or LlamaIndex shall be introduced unless a later approved requirement demonstrates that the project cannot reasonably satisfy the requirement with the existing architecture and direct integration contracts.

---

# 23. Testing Strategy

The implementation shall support deterministic automated testing.

## 23.1 Unit Testing

Tests shall cover:

- normalization;
- deterministic chunking;
- indexing state transitions;
- provider abstraction;
- embedding-response validation;
- dimension validation;
- failure classification.

## 23.2 Integration Testing

PostgreSQL + pgvector integration tests shall cover:

- vector persistence;
- vector retrieval;
- cosine ordering;
- metadata filtering;
- document/chunk relationships;
- atomic replacement;
- failure preservation behavior.

## 23.3 Provider Testing

Normal automated test suites shall not require live OpenAI API access.

A fake/test implementation shall provide deterministic embeddings.

Real-provider smoke validation may be executed separately using explicitly configured credentials.

## 23.4 Acceptance Testing

Acceptance shall demonstrate at minimum:

1. an administrator can create approved knowledge;
2. the document can be indexed;
3. chunks are persisted;
4. valid embeddings are persisted;
5. a known semantic query retrieves an expected chunk;
6. language filtering restricts the result set;
7. inactive knowledge is excluded;
8. reindexing replaces derived data consistently;
9. provider failure does not silently produce false indexed state;
10. existing Homepage, Contact, Portfolio, Administration, analytics, SEO, i18n, responsive, and accessibility behavior remains regression-protected.

---

# 24. Performance and Scalability

The initial architecture is optimized for a small curated corpus and sporadic access.

Exact vector search is expected to be sufficient.

The architecture shall not introduce premature ANN indexing, caching, queue infrastructure, or horizontal service decomposition.

A scalability change requires objective evidence such as:

- unacceptable retrieval latency;
- materially larger corpus;
- significantly higher traffic;
- operational contention;
- measured database pressure.

---

# 25. Cost

The approved architecture minimizes new recurring infrastructure cost.

pgvector adds no separate hosted vector-database service.

The expected embedding volume for the initial Knowledge Base is small.

Managed embedding cost is expected to remain materially lower than the operational cost of introducing a self-hosted ML runtime.

Cost shall remain observable and subject to future review if corpus size or access volume changes materially.

---

# 26. Consequences

## 26.1 Positive Consequences

This decision:

- preserves the Modular Monolith;
- reuses PostgreSQL;
- avoids a second database;
- avoids unnecessary queue infrastructure;
- supports semantic retrieval;
- supports typed metadata filtering;
- provides explicit provider isolation;
- minimizes operating cost;
- enables deterministic testing;
- creates a controlled path to RAG;
- allows future provider replacement;
- keeps AI infrastructure proportional to project scale.

## 26.2 Negative Consequences

This decision introduces:

- pgvector as an operational database prerequisite;
- external embedding-provider dependency;
- embedding-provider cost, although expected to be very small;
- schema coupling to vector dimensionality;
- required reindexing when embedding semantics materially change;
- explicit production provisioning before vector migrations.

## 26.3 Accepted Trade-offs

The project accepts:

- managed-provider dependency in exchange for reduced operational complexity;
- exact search instead of ANN in exchange for implementation simplicity;
- synchronous indexing instead of workers in exchange for lower infrastructure complexity;
- explicit reindexing during embedding-model migration in exchange for simple persistent design.

---

# 27. Rejected / Deferred Capabilities

The following are not part of the initial decision:

- dedicated vector database;
- HNSW;
- IVFFlat;
- Celery;
- Redis queue;
- asynchronous indexing workers;
- self-hosted embedding model;
- LangChain;
- LlamaIndex;
- unrestricted JSON metadata model;
- automatic indexing of all application data;
- public RAG endpoint;
- LLM response generation;
- chat UI;
- conversation persistence.

These capabilities require independent evidence and approval if later proposed.

---

# 28. Requirement Traceability

The decision establishes the following traceability chain:

Release 2 Knowledge/RAG requirement
→ ARCH-DEC-006
→ ADR-006
→ SPEC-004
→ Knowledge implementation
→ indexing/retrieval tests
→ PostgreSQL/pgvector validation
→ acceptance evidence.

Implementation shall validate this decision but shall not redefine it.

---

# 29. Affected Documents

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
- ADR-003 — Python Runtime and Development Toolchain;
- ADR-004 — Transactional Email Integration;
- ADR-005 — Production Application Runtime and Reverse Proxy.

This ADR shall govern:

- SPEC-004 — Knowledge Base and Retrieval;
- Release 2 Knowledge Base implementation;
- Release 2 embedding integration;
- Release 2 vector persistence;
- Release 2 retrieval implementation;
- related deployment/runbook changes;
- downstream IA Jujuju RAG consumption.

No lower-authority implementation artifact shall redefine these architectural decisions.

---

# 30. Superseded Decisions

ADR-006 does not supersede ADR-001 through ADR-005.

It refines the Release 2 architecture by resolving previously deferred AI/RAG technology and persistence decisions.

No Release 1 or Release 1.1 architectural decision is invalidated.

---

# 31. Future Review Triggers

This ADR shall be reviewed if any of the following occurs:

- replacement of PostgreSQL;
- replacement of pgvector;
- introduction of a dedicated vector database;
- material corpus-scale increase;
- unacceptable exact-search performance;
- introduction of ANN indexing;
- embedding-provider replacement;
- embedding-model replacement;
- vector-dimension change;
- migration to self-hosted embeddings;
- introduction of asynchronous indexing infrastructure;
- material privacy or security-policy change;
- revised AI/RAG requirements invalidating the assumptions herein.

---

# 32. Compliance

This ADR complies with:

- EGS-001;
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
- ADR-003;
- ADR-004;
- ADR-005.

The decision has been evaluated for:

- functional fit;
- architecture consistency;
- security;
- maintainability;
- testability;
- performance;
- scalability;
- deployment compatibility;
- operational complexity;
- cost;
- vendor dependency;
- migration impact;
- technical debt;
- controlled evolution.

No architectural conflict with the existing approved Modular Monolith baseline has been identified.

---

# 33. Approval Statement

ADR-006 version 1.0.0 constitutes the approved architectural decision governing the Site Portfolio Release 2 Knowledge Base, embedding integration, vector persistence, indexing lifecycle, and semantic retrieval architecture.

Product Owner approval establishes that:

- PostgreSQL + pgvector is the approved vector-storage architecture;
- no dedicated vector database shall be introduced initially;
- OpenAI is the approved initial embedding provider;
- `text-embedding-3-small` is the approved initial embedding model;
- the approved vector dimensionality is 1024;
- cosine similarity is the approved similarity strategy;
- exact vector retrieval is the approved initial search strategy;
- provider isolation is mandatory;
- metadata filtering shall remain relational and explicit;
- indexing shall initially be synchronous;
- network provider calls shall remain outside long database transactions;
- derived chunks shall be atomically replaced after successful embedding generation;
- pgvector shall be provisioned as an infrastructure prerequisite;
- the Django application database user shall not require superuser privileges;
- ANN indexes, dedicated vector databases, worker infrastructure, and local embedding runtimes are deferred absent objective need.

All Release 2 Knowledge Base and retrieval specifications, implementation, testing, deployment, and validation activities shall comply with this ADR unless formally superseded through the approved engineering-governance process.

---

# 34. Revision History

| Version | Date | Author / Authority | Description |
|---|---|---|---|
| 1.0.0 | 2026-08-31 | Solution Architecture | Initial ADR consolidating Release 2 Knowledge Base, pgvector, embedding-provider and retrieval architecture. |
| 1.0.0 | 2026-08-31 | Product Owner | Approved Baseline status granted; PostgreSQL + pgvector, OpenAI `text-embedding-3-small`, 1024 dimensions, cosine exact retrieval, provider isolation and synchronous indexing accepted. |

---

# End of Document
