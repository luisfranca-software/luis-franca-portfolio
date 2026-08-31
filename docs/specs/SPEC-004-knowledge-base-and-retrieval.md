# SPEC-004 — Knowledge Base and Retrieval

| Field | Value |
|---|---|
| **Document ID** | SPEC-004 |
| **Title** | Knowledge Base and Retrieval |
| **Version** | 1.0.0 |
| **Status** | Approved Baseline |
| **Project** | Site Portfolio |
| **Release** | Release 2 — Platform Evolution |
| **Owner** | Product Engineering |
| **Approver** | Product Owner |
| **Development Model** | Specification-Driven Development (SDD) |
| **Created** | 2026-08-31 |
| **Last Updated** | 2026-08-31 |

---

# 1. Purpose

This specification defines the functional, data, integration, administration, indexing, retrieval, security, testing, and acceptance requirements for the Release 2 Knowledge Base and semantic retrieval capability.

SPEC-004 operationalizes ADR-006.

The implementation shall provide a controlled pipeline:

Admin
→ KnowledgeDocument
→ Normalize
→ Chunk
→ Embed
→ KnowledgeChunk
→ PostgreSQL + pgvector
→ Metadata Filter
→ Vector Retrieval
→ Controlled Retrieval Result

This specification establishes the retrievable knowledge foundation consumed by the future IA Jujuju assistant.

It does not implement LLM answer generation or the public conversational interface.

---

# 2. Normative Authority

This specification shall comply with:

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
- ADR-006 — Knowledge Base, Embeddings and Vector Retrieval Architecture;
- approved Release 2 Product Owner decisions.

In case of conflict, higher-authority approved artifacts prevail.

Implementation evidence shall validate this specification but shall not redefine its requirements.

---

# 3. Scope

## 3.1 Included

SPEC-004 includes:

- Knowledge Base Django application boundary;
- administrator-managed knowledge documents;
- knowledge activation/deactivation;
- document language;
- controlled knowledge categories;
- normalization;
- deterministic chunking;
- embedding-provider abstraction;
- OpenAI embedding integration;
- PostgreSQL pgvector persistence;
- vector dimensionality;
- indexing lifecycle;
- reindexing;
- indexing failure handling;
- metadata-constrained retrieval;
- cosine similarity;
- exact vector search;
- retrieval result contract;
- Django Admin integration;
- management reindex capability;
- security requirements;
- observability requirements;
- unit and integration testing;
- retrieval acceptance validation;
- operational pgvector prerequisites.

## 3.2 Excluded

SPEC-004 does not include:

- public chat UI;
- interactive IA Jujuju launcher behavior;
- LLM answer generation;
- system-prompt implementation for conversational answers;
- conversation persistence;
- conversation history UI;
- streaming responses;
- intelligent public search UI;
- CRM;
- analytics dashboards;
- dedicated vector database;
- ANN indexes;
- Celery;
- Redis;
- asynchronous indexing workers;
- self-hosted embedding models;
- LangChain;
- LlamaIndex.

These capabilities require separate approved scope where applicable.

---

# 4. Product Objective

The Knowledge Base shall provide an explicit, administrator-controlled source of professional knowledge that can be retrieved semantically by Release 2 AI functionality.

The system shall allow approved content concerning subjects such as:

- professional profile;
- professional experience;
- skills;
- projects;
- engineering practices;
- software architecture;
- development processes;
- portfolio information;
- other explicitly approved professional knowledge.

The Knowledge Base shall not infer that arbitrary application data is authorized AI knowledge merely because the data exists in PostgreSQL.

---

# 5. Architectural Boundary

A dedicated Django application shall own Knowledge Base behavior.

The expected application responsibility is conceptually:

`backend/apps/knowledge`

The actual repository path shall follow the established project application structure discovered during implementation.

The Knowledge application shall own:

- KnowledgeDocument;
- KnowledgeChunk;
- normalization;
- chunking;
- embedding-provider contract;
- embedding-provider integration;
- indexing;
- reindexing;
- retrieval;
- related Django Admin behavior;
- related management commands.

External embedding-provider calls shall not originate directly from:

- templates;
- views;
- models;
- Django Admin classes;
- unrelated application modules.

They shall pass through the approved application/integration boundary.

---

# 6. Functional Requirements

## 6.1 Knowledge Administration

### KB-FR-001

An authorized Django Admin user shall be able to create a KnowledgeDocument.

### KB-FR-002

An authorized Django Admin user shall be able to edit a KnowledgeDocument.

### KB-FR-003

An authorized Django Admin user shall be able to activate or deactivate a KnowledgeDocument.

### KB-FR-004

An authorized Django Admin user shall be able to inspect the indexing status of a KnowledgeDocument.

### KB-FR-005

An authorized Django Admin user shall be able to request reindexing.

### KB-FR-006

KnowledgeChunk shall be system-derived data and shall not be treated as the primary administrator-authored content authority.

### KB-FR-007

Knowledge administration shall reuse native Django Admin authentication and authorization.

No separate Knowledge Base authentication system shall be introduced.

---

# 7. KnowledgeDocument Contract

The implementation shall introduce a persistent KnowledgeDocument entity.

The final Django field types may follow established repository conventions while preserving the following semantic contract.

| Field | Required | Responsibility |
|---|---:|---|
| `id` | Yes | Persistent primary identifier |
| `title` | Yes | Administrator-readable title |
| `slug` | Yes | Stable document identifier |
| `language` | Yes | Controlled content language |
| `category` | Yes | Controlled knowledge classification |
| `content` | Yes | Authoritative source content |
| `is_active` | Yes | Retrieval eligibility |
| `indexing_status` | Yes | Index lifecycle state |
| `index_version` | Yes | Processing/index compatibility version |
| `embedding_model` | Conditional | Model associated with successful indexing |
| `indexed_at` | Conditional | Last successful indexing timestamp |
| `last_index_error` | No | Sanitized last indexing failure |
| `created_at` | Yes | Creation timestamp |
| `updated_at` | Yes | Modification timestamp |

---

# 8. KnowledgeDocument Validation

### KB-VAL-001

`title` shall not be empty.

### KB-VAL-002

`content` shall not be empty.

### KB-VAL-003

`language` shall use a controlled supported value.

Initial supported values shall include:

- `en`;
- `pt-br`.

### KB-VAL-004

`category` shall use a controlled value rather than unrestricted administrator-authored category text.

Initial categories shall support the approved professional knowledge domain.

The initial category set shall include:

- `PROFILE`;
- `EXPERIENCE`;
- `SKILL`;
- `PROJECT`;
- `ENGINEERING`;
- `PROCESS`;
- `PORTFOLIO`;
- `GENERAL`.

### KB-VAL-005

`slug` shall be unique according to the final model contract.

### KB-VAL-006

Invalid document state shall not silently enter the indexing pipeline.

---

# 9. Active-State Contract

`is_active` controls retrieval eligibility.

When:

`is_active = true`

the document may participate in retrieval if it is otherwise successfully indexed.

When:

`is_active = false`

the document shall be excluded from retrieval.

Deactivation shall not require destructive deletion of the source document.

Deactivation shall preserve administrative history represented by the persistent record.

---

# 10. KnowledgeChunk Contract

The implementation shall introduce KnowledgeChunk as system-derived persistent retrieval data.

| Field | Required | Responsibility |
|---|---:|---|
| `id` | Yes | Persistent primary identifier |
| `document` | Yes | Foreign key to KnowledgeDocument |
| `sequence` | Yes | Deterministic order within document |
| `content` | Yes | Derived chunk text |
| `embedding` | Yes for valid indexed chunks | pgvector embedding |
| `created_at` | Yes | Persistence timestamp |

The implementation may introduce additional narrowly justified technical fields when required to satisfy this specification without changing its domain semantics.

---

# 11. KnowledgeDocument–KnowledgeChunk Relationship

The relationship shall be:

KnowledgeDocument 1 → N KnowledgeChunk

A KnowledgeChunk shall belong to exactly one KnowledgeDocument.

A document may have zero chunks before successful initial indexing.

A successfully indexed, non-empty document shall have one or more valid chunks.

The pair:

`document + sequence`

shall be unique.

Deletion of a KnowledgeDocument shall not leave orphan KnowledgeChunk records.

---

# 12. Vector Contract

KnowledgeChunk shall persist its embedding using PostgreSQL pgvector.

The approved initial dimensionality is:

`1024`

Conceptually:

`vector(1024)`

The Python/Django integration shall use the approved `pgvector` package.

The application shall reject provider results whose vector dimensionality does not match the configured and persisted schema contract.

Dimension mismatch shall not be silently truncated, padded, or persisted.

---

# 13. Embedding Provider Contract

The application shall define an application-owned embedding-provider abstraction.

The contract shall support, at minimum:

- embedding document/chunk text;
- embedding query text.

Conceptually:

```python
class EmbeddingProvider(Protocol):
    def embed_documents(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        ...

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        ...

The exact Python signature may follow project conventions while preserving these responsibilities.

---

# **14. OpenAI Provider**

The initial production implementation shall use:

Provider:

`OpenAI`

Model:

`text-embedding-3-small`

Dimensions:

`1024`

The OpenAI SDK shall remain isolated inside the concrete integration implementation.

Provider-specific exceptions shall not leak uncontrolled throughout the application.

They shall be translated into application-owned error semantics where appropriate.

---

# **15. Provider Configuration**

The provider shall use environment-based configuration.

Required secret:

`OPENAI_API_KEY`

The implementation shall also define controlled configuration for:

* embedding model;
* embedding dimensions;
* provider timeout;
* provider batch size where supported and justified.

The application shall not expose the OpenAI API key through:

* Git;
* templates;
* HTML;
* JavaScript;
* Django Admin;
* logs;
* exception pages in production.

The configured embedding dimensions shall be validated against the schema-level approved dimension.

---

# **16. Normalization**

Before chunking, source content shall undergo deterministic normalization.

Normalization shall preserve semantic content.

It may include:

* newline normalization;
* removal of unnecessary repeated whitespace;
* normalization of paragraph separation;
* trimming of leading/trailing whitespace.

Normalization shall not:

* rewrite factual meaning;
* translate content;
* summarize content through an LLM;
* invent content;
* remove meaningful semantic structure.

---

# **17. Chunking**

Chunking shall be deterministic.

The initial implementation shall be:

* paragraph-aware;
* sentence-boundary-aware where practical;
* provider-independent;
* compatible with EN and PT-BR;
* testable without network access.

The implementation shall use a bounded target size.

The initial target shall be approximately:

`1200 characters`

The initial overlap target shall be approximately:

`150 characters`

These values may be adjusted during Gate B only if repository content and focused retrieval tests provide objective evidence for a better value.

Any material change shall be reflected in validation evidence.

---

# **18. Chunking Invariants**

### **KB-CHK-001**

Equal normalized input under equal configuration shall generate equal chunks.

### **KB-CHK-002**

Chunk sequence shall be deterministic.

### **KB-CHK-003**

The chunker shall avoid mid-sentence boundaries where reasonably possible.

### **KB-CHK-004**

The chunker shall avoid unnecessary empty chunks.

### **KB-CHK-005**

Whitespace-only chunks shall not be persisted.

### **KB-CHK-006**

Overlap shall not cause nondeterministic ordering.

### **KB-CHK-007**

Chunking shall not require live OpenAI access.

---

# **19. Indexing Lifecycle**

KnowledgeDocument indexing shall use the following states:

* `PENDING`;
* `INDEXING`;
* `INDEXED`;
* `FAILED`.

---

# **20. PENDING State**

A document requiring initial indexing or reindexing shall be representable as `PENDING`.

A material source-content change shall make the current indexing state detectable as requiring reindexing.

The implementation shall not represent modified content as successfully indexed when the persisted chunks still correspond to a previous source version.

---

# **21. INDEXING State**

`INDEXING` indicates that an indexing operation is in progress.

For the initial release, indexing is synchronous.

The state shall not imply successful completion.

---

# **22. INDEXED State**

A document shall enter `INDEXED` only after:

1. source validation succeeds;
2. normalization succeeds;
3. chunking succeeds;
4. embedding generation succeeds;
5. embedding count is valid;
6. every embedding dimension is valid;
7. derived chunks are persisted consistently;
8. indexing metadata is updated successfully.

`indexed_at` shall reflect the successful indexing completion time.

`embedding_model` shall reflect the model responsible for the valid persisted index.

---

# **23. FAILED State**

A document shall enter or expose an appropriate failure state when an indexing operation cannot complete successfully.

The system shall retain a sanitized operational failure description where useful.

A failed initial indexing operation shall not produce a false `INDEXED` state.

---

# **24. Reindexing**

Reindexing shall regenerate derived KnowledgeChunk data from the current authoritative KnowledgeDocument content.

Reindexing shall be required when applicable after changes to:

* source content;
* indexing algorithm compatibility;
* embedding model;
* embedding dimensions;
* provider semantics;
* other retrieval-affecting configuration.

The initial `index_version` shall be:

`1`

---

# **25. Safe Reindex Replacement**

For an already indexed document, the implementation shall prefer preserving the last valid chunk set until replacement data is ready.

The intended sequence is:

1. read and validate source content;
2. normalize;
3. generate replacement chunks;
4. request replacement embeddings;
5. validate all embeddings;
6. begin short database transaction;
7. remove/replace old derived chunks;
8. persist the complete new set;
9. update document indexing metadata;
10. commit.

A provider network request shall not be executed inside the short replacement transaction.

Partial replacement shall not become the visible valid index.

---

# **26. Indexing Failure Preservation**

When reindexing an already valid document fails before atomic replacement:

* the existing valid chunk set shall not be unnecessarily destroyed;
* the failure shall be observable;
* the system shall not falsely claim that the new source content has been successfully indexed.

The exact representation of “last valid index versus current source requiring reindex” shall remain explicit and testable.

---

# **27. Retry Contract**

Provider retries shall be bounded.

The initial implementation may use a maximum of three attempts for explicitly classified transient failures.

Potential transient failures include:

* timeout;
* temporary service unavailability;
* supported rate-limit scenarios.

Permanent failures shall not be blindly retried.

Examples include:

* invalid API key;
* invalid request;
* dimension mismatch;
* invalid provider response;
* invalid local configuration.

Retry logic shall not hold a database transaction open.

---

# **28. Retrieval Service**

The Knowledge application shall provide an application-owned retrieval service.

The service shall conceptually accept:

* query text;
* language;
* optional controlled metadata filters;
* `top_k`.

The service shall return structured retrieval results.

The retrieval service shall not generate the final IA Jujuju natural-language answer.

---

# **29. Retrieval Result Contract**

A retrieval result shall provide sufficient information for downstream controlled-context construction.

The contract shall include or allow resolution of:

* chunk identifier;
* document identifier;
* chunk content;
* similarity/distance value;
* language;
* category;
* source/document identity.

The result shall not expose unnecessary internal database or provider implementation details.

---

# **30. Query Embedding**

The retrieval query shall be embedded through the approved EmbeddingProvider abstraction.

The query embedding shall use embedding semantics compatible with the persisted document embeddings.

The application shall validate the returned query vector before executing vector retrieval.

---

# **31. Similarity Strategy**

Cosine similarity is the approved initial semantic similarity strategy.

Retrieval shall use pgvector cosine-distance semantics.

Conceptually:

`ORDER BY embedding <=> query_embedding`

The exact Django ORM implementation shall use the supported pgvector Django integration rather than unsafe handcrafted SQL when the ORM integration satisfies the requirement.

---

# **32. Exact Search**

Initial retrieval shall use exact vector search.

The implementation shall not create:

* HNSW indexes;
* IVFFlat indexes;

for the initial Release 2 Knowledge Base.

No ANN-specific tuning shall be introduced.

---

# **33. Top-K**

The initial default retrieval result count shall be:

`top_k = 5`

The service shall permit a controlled value where required.

Unbounded result counts shall not be accepted from untrusted callers.

A material change to the default shall be supported by retrieval-quality evidence.

---

# **34. Similarity Threshold**

No mandatory hard similarity threshold shall be introduced initially.

Retrieval quality shall first be evaluated against known questions and expected source chunks.

A threshold may be introduced later only with evidence demonstrating improved retrieval behavior.

---

# **35. Metadata Filtering**

Retrieval shall exclude documents where:

`is_active = false`

Retrieval shall support language filtering.

Initial supported language behavior:

* EN query/context → `en`;
* PT-BR query/context → `pt-br`.

Category filtering shall be supported as controlled metadata where requested by the retrieval consumer.

Metadata filtering and vector similarity shall remain composable in the same retrieval path.

---

# **36. Retrieval Eligibility**

A chunk is eligible for normal retrieval only when:

* its parent document is active;
* its parent document is in a valid retrievable indexing state;
* language constraints are satisfied;
* requested metadata constraints are satisfied;
* its embedding is valid.

A record shall not become retrievable solely because an embedding exists.

---

# **37. Knowledge Base Security Boundary**

Knowledge Base ingestion is explicit.

The implementation shall not automatically index:

* ContactRequest records;
* AnalyticsEvent records;
* visitor data;
* authentication credentials;
* passwords;
* API keys;
* environment variables;
* application logs;
* private operational information;
* arbitrary Django model content.

Knowledge becomes RAG-authorized only through an approved Knowledge Base ingestion path.

---

# **38. Django Admin Requirements**

KnowledgeDocument shall be registered in Django Admin.

The Admin interface shall provide useful visibility into at least:

* title;
* language;
* category;
* active state;
* indexing status;
* last successful indexing time.

Appropriate filtering shall include controlled fields such as:

* language;
* category;
* active state;
* indexing status.

Appropriate search shall include administrator-readable identity fields.

---

# **39. Admin Reindex Action**

The Admin shall provide a controlled way to request reindexing for authorized documents.

The action shall:

* use the application indexing service;
* not call the OpenAI SDK directly from Admin implementation logic;
* provide useful success/failure feedback;
* respect Django Admin authorization.

Bulk behavior shall remain bounded and appropriate for the small corpus.

---

# **40. KnowledgeChunk Administration**

KnowledgeChunk is derived data.

The normal administrator workflow shall not encourage manual editing of:

* chunk text;
* embedding vector;
* sequence.

If exposed in Admin for diagnostics, derived fields shall be read-only or otherwise protected from normal content-authoring behavior.

KnowledgeDocument remains the source authority.

---

# **41. Management Command**

The implementation shall provide an operator-oriented management command for controlled reindexing.

The command shall support the operational need to rebuild Knowledge Base vector data without requiring manual database manipulation.

The command shall use the same indexing application service as Admin-triggered indexing.

Duplicated indexing implementations are prohibited.

The exact command name shall follow repository conventions.

---

# **42. Dependency Requirements**

The implementation shall add only dependencies required by the approved architecture.

Expected direct dependencies:

* `pgvector`;
* `openai`.

Dependencies shall be declared in:

`pyproject.toml`

and resolved through:

`uv.lock`.

The implementation shall not introduce LangChain, LlamaIndex, Celery, Redis, or a dedicated vector database client.

---

# **43. Database Extension Requirement**

The target PostgreSQL database shall provide:

`vector`

through pgvector before vector-dependent application migrations execute.

Local validated baseline:

* PostgreSQL 18.6;
* pgvector 0.8.1;
* `vector` extension enabled;
* Django connection verified to use the vector type.

Production validated discovery:

* PostgreSQL 16.15;
* `postgresql-16-pgvector` available through the target operating-system package repository;
* privileged installation capability available;
* production extension installation intentionally deferred until controlled deployment.

---

# **44. Migration Requirements**

Migrations shall create the Knowledge Base relational/vector schema.

Migration design shall not require the ordinary Django application database user to become PostgreSQL superuser.

pgvector provisioning shall be treated as an operational prerequisite.

The migration sequence shall be compatible with:

* PostgreSQL 18 development;
* PostgreSQL 16 production.

`makemigrations --check --dry-run` shall report no unintended migration drift after implementation.

---

# **45. Transaction Requirements**

External embedding-provider network calls shall execute outside long database transactions.

Database transactions shall be used where necessary to preserve atomic derived-data replacement and indexing-state consistency.

The implementation shall not keep PostgreSQL locks open while waiting for external provider responses unless an independently justified requirement makes it unavoidable.

---

# **46. Concurrency**

The initial implementation does not require distributed locking infrastructure.

The indexing design shall nevertheless avoid knowingly exposing partial chunk replacement.

If concurrent indexing of the same document creates an objective correctness problem during implementation testing, the smallest database-native coordination mechanism sufficient to preserve correctness shall be preferred.

No Redis-based distributed lock shall be introduced for this scope.

---

# **47. Observability Requirements**

Indexing shall provide operationally useful logs or equivalent evidence including:

* document identifier;
* operation start;
* operation completion;
* indexing status;
* chunk count;
* embedding provider/model identity;
* elapsed duration;
* sanitized error category where applicable.

Retrieval may record:

* execution duration;
* result count;
* requested top-k;
* non-sensitive filters.

---

# **48. Logging Restrictions**

Logs shall not contain:

* `OPENAI_API_KEY`;
* authorization headers;
* complete embedding vectors;
* unnecessary complete Knowledge Base source content;
* passwords;
* secrets.

Provider exceptions shall be sanitized before persistence or administrator display when necessary.

---

# **49. Performance Requirements**

The implementation is optimized for a small curated corpus and sporadic access.

Exact retrieval shall be considered acceptable unless measurement demonstrates otherwise.

The implementation shall not introduce performance infrastructure based only on hypothetical future scale.

Performance evidence shall focus on:

* indexing completion;
* retrieval correctness;
* reasonable local retrieval latency;
* absence of obvious query explosion;
* absence of unnecessary external requests.

---

# **50. Cost Requirements**

Embedding calls shall be limited to operations that require embedding generation.

A retrieval query shall generate only the query embedding required by the retrieval operation.

Existing document embeddings shall be reused.

Documents shall not be re-embedded on every retrieval.

Unchanged Knowledge Base content shall not be unnecessarily reindexed.

The architecture shall not introduce a separately billed vector database.

---

# **51. Test Doubles**

Automated tests shall use deterministic provider doubles where live provider behavior is not the subject under test.

A FakeEmbeddingProvider shall:

* generate deterministic output;
* respect the configured dimensional contract;
* permit controlled failure simulation;
* never be selected as the production provider by accident.

Tests shall not depend on internet connectivity.

---

# **52. Unit Test Requirements**

Unit tests shall cover at minimum:

### **KB-UT-001**

Normalization is deterministic.

### **KB-UT-002**

Chunking is deterministic.

### **KB-UT-003**

Empty chunks are not generated.

### **KB-UT-004**

Chunk sequence is stable.

### **KB-UT-005**

EN content can be chunked.

### **KB-UT-006**

PT-BR content can be chunked.

### **KB-UT-007**

Provider response count is validated.

### **KB-UT-008**

Embedding dimensions are validated.

### **KB-UT-009**

Transient provider failure can be classified.

### **KB-UT-010**

Permanent configuration failure is not blindly retried.

### **KB-UT-011**

Index lifecycle transitions are validated.

---

# **53. Integration Test Requirements**

Integration tests using PostgreSQL + pgvector shall cover at minimum:

### **KB-IT-001**

KnowledgeDocument persistence.

### **KB-IT-002**

KnowledgeChunk persistence.

### **KB-IT-003**

`vector(1024)` persistence.

### **KB-IT-004**

Document-to-chunk relationship.

### **KB-IT-005**

Unique document/sequence constraint.

### **KB-IT-006**

Cosine-distance ordering.

### **KB-IT-007**

Active-document filtering.

### **KB-IT-008**

Inactive-document exclusion.

### **KB-IT-009**

Language filtering.

### **KB-IT-010**

Category filtering.

### **KB-IT-011**

Top-k limitation.

### **KB-IT-012**

Successful indexing produces INDEXED state.

### **KB-IT-013**

Failed initial indexing does not produce false INDEXED state.

### **KB-IT-014**

Successful reindex atomically replaces derived chunks.

### **KB-IT-015**

Failed reindex preserves the last valid chunk set where required by the safe-replacement contract.

---

# **54. Django Admin Test Requirements**

Tests shall verify:

### **KB-ADM-001**

Anonymous users cannot access Knowledge administration.

### **KB-ADM-002**

Unauthorized authenticated users cannot perform privileged Knowledge administration.

### **KB-ADM-003**

Authorized staff can access KnowledgeDocument administration according to assigned permissions.

### **KB-ADM-004**

Authorized users can create valid KnowledgeDocument records.

### **KB-ADM-005**

Authorized users can edit valid KnowledgeDocument records.

### **KB-ADM-006**

Authorized users can activate/deactivate documents.

### **KB-ADM-007**

Indexing state is visible.

### **KB-ADM-008**

Reindex action uses the indexing service.

### **KB-ADM-009**

Derived chunk/vector data is protected from inappropriate normal editing.

---

# **55. Retrieval Acceptance Dataset**

Gate B validation shall create a small controlled test corpus representing the intended professional domain.

The corpus shall include at minimum:

* EN knowledge;
* PT-BR knowledge;
* at least two categories;
* at least one inactive document;
* semantically related but lexically different query/content pairs.

Acceptance queries shall define the expected source document or chunk.

This dataset is validation data and shall not be confused with production Knowledge Base content.

---

# **56. Retrieval Acceptance Criteria**

### **KB-AC-001**

A valid KnowledgeDocument can be created through the approved administrative path.

### **KB-AC-002**

A valid document can be indexed successfully.

### **KB-AC-003**

Indexing produces deterministic chunks.

### **KB-AC-004**

Every valid persisted indexed chunk contains a 1024-dimensional embedding.

### **KB-AC-005**

A known semantic query retrieves the expected relevant source within the configured top-k.

### **KB-AC-006**

PT-BR filtering excludes EN-only results when PT-BR retrieval is explicitly required.

### **KB-AC-007**

EN filtering excludes PT-BR-only results when EN retrieval is explicitly required.

### **KB-AC-008**

Inactive documents do not participate in retrieval.

### **KB-AC-009**

Category filtering restricts eligible results.

### **KB-AC-010**

Provider failure does not generate fake or partial valid indexing state.

### **KB-AC-011**

Failed reindexing does not unnecessarily destroy the previously valid index.

### **KB-AC-012**

Exact cosine retrieval operates through PostgreSQL + pgvector.

### **KB-AC-013**

No dedicated vector database is required.

### **KB-AC-014**

No live OpenAI request is required by the normal automated test suite.

### **KB-AC-015**

Knowledge Base functionality does not regress approved Release 1, Release 1.1, or Release 2 Administration behavior.

---

# **57. Regression Requirements**

The implementation shall preserve existing behavior for:

* Homepage;
* Contact;
* Portfolio;
* Header;
* Footer;
* Django Admin;
* native authentication/authorization;
* ContactRequest administration;
* analytics;
* SEO;
* i18n;
* accessibility;
* responsive behavior.

No Knowledge Base implementation shall redefine previously approved UI without an approved requirement.

---

# **58. Quality Gates**

Before Gate B acceptance, the implementation shall pass the project's applicable quality gates, including:

* focused Knowledge unit tests;
* Knowledge integration tests;
* Django Admin Knowledge tests;
* existing Admin regression tests;
* full test suite;
* Ruff lint for affected scope;
* Ruff format validation for affected scope;
* MyPy;
* Django system check;
* migration consistency validation;
* PostgreSQL readiness;
* pgvector functional validation;
* Git diff integrity validation.

Repository-wide historical formatting debt outside the implementation scope shall not be silently rewritten solely to satisfy this feature.

---

# **59. Security Acceptance**

The implementation shall demonstrate:

* no API key committed to Git;
* no API key rendered client-side;
* no application DB superuser requirement;
* native Django Admin authorization;
* explicit Knowledge Base ingestion;
* inactive knowledge exclusion;
* no automatic indexing of ContactRequest;
* no automatic indexing of analytics;
* sanitized failure reporting;
* no full embedding-vector logging.

---

# **60. Operational Acceptance**

Before production migration, operations shall verify:

1. target PostgreSQL major version;
2. corresponding pgvector OS package;
3. package installation;
4. `CREATE EXTENSION vector`;
5. extension visibility in the application database;
6. application user's ability to use vector data without superuser privilege;
7. environment provider configuration;
8. application migrations;
9. post-migration checks;
10. rollback/recovery readiness.

Production pgvector provisioning shall be a controlled deployment operation.

---

# **61. Production Deployment Sequence**

The expected production sequence is:

1. backup/recovery readiness verification;
2. install PostgreSQL-major-compatible pgvector package;
3. enable `vector` in the application database using privileged database administration;
4. verify extension;
5. deploy application dependency changes;
6. apply Django migrations;
7. run Django system checks;
8. verify Knowledge schema;
9. configure embedding-provider secret;
10. execute controlled smoke indexing/retrieval validation;
11. validate existing application behavior.

Exact operational commands shall be maintained in the appropriate deployment/runbook artifact.

---

# **62. Rollback Considerations**

Application rollback shall account for the presence of Knowledge Base migrations.

The pgvector operating-system package and PostgreSQL extension need not be destructively removed merely because an application deployment is rolled back, unless an approved recovery procedure explicitly requires removal.

Rollback shall prioritize preservation of database integrity over unnecessary infrastructure reversal.

---

# **63. Implementation Sequence**

Gate B should proceed in the following order unless repository evidence requires a justified adjustment:

1. add approved dependencies;
2. create Knowledge application boundary;
3. define models and migrations;
4. implement normalization;
5. implement deterministic chunking;
6. implement EmbeddingProvider contract;
7. implement deterministic FakeEmbeddingProvider;
8. implement OpenAI provider adapter;
9. implement indexing service;
10. implement retrieval service;
11. integrate Django Admin;
12. implement management reindex command;
13. implement focused tests;
14. execute pgvector integration validation;
15. execute full regression suite;
16. audit Git diff;
17. produce acceptance evidence.

---

# **64. Traceability Matrix**

| Requirement Area | Decision Authority | Implementation Evidence | Validation |
| ----- | ----- | ----- | ----- |
| Knowledge persistence | ADR-006 / SPEC-004 | KnowledgeDocument | Model/integration tests |
| Chunk persistence | ADR-006 / SPEC-004 | KnowledgeChunk | Model/integration tests |
| Vector persistence | ADR-006 | `vector(1024)` | pgvector integration tests |
| Embeddings | ADR-006 | EmbeddingProvider/OpenAI adapter | Unit/provider tests |
| Chunking | SPEC-004 | Chunking service | Determinism tests |
| Index lifecycle | SPEC-004 | Indexing service | State/failure tests |
| Safe reindex | ADR-006 / SPEC-004 | Atomic replacement | Integration tests |
| Metadata filtering | ADR-006 / SPEC-004 | Retrieval service | Retrieval tests |
| Cosine search | ADR-006 | pgvector retrieval | Semantic retrieval tests |
| Admin | U-02/U-03 / SPEC-004 | Django Admin | Admin tests |
| Security | ARCH-001 / SPEC-004 | Config/authz/boundaries | Security validation |
| Operations | ADR-006 / OPS-001 | pgvector provisioning | Deployment evidence |
| Regression | TST-001 | Existing application | Full suite |

---

# **65. Definition of Done**

SPEC-004 is implemented when:

* KnowledgeDocument exists and is administrable;
* KnowledgeChunk exists as derived data;
* pgvector persists valid 1024-dimensional embeddings;
* OpenAI embedding integration is isolated;
* deterministic test embeddings exist;
* normalization and chunking are implemented;
* indexing and reindexing are implemented;
* indexing states are explicit;
* failed indexing is safely represented;
* exact cosine retrieval works;
* metadata filtering works;
* inactive knowledge is excluded;
* EN/PT-BR filtering works;
* Admin reindexing works;
* operator reindex capability exists;
* focused tests pass;
* PostgreSQL/pgvector tests pass;
* full regression suite passes;
* required quality gates pass;
* deployment prerequisites are documented;
* acceptance evidence demonstrates the critical RAG retrieval gate.

---

# **66. Critical Release 2 Gate**

The following end-to-end capability is mandatory before Day 3 can be considered complete:

Admin
 → KnowledgeDocument
 → Normalize
 → Chunk
 → Embed
 → PostgreSQL pgvector
 → Metadata Filter
 → Semantic Retrieval
 → Expected KnowledgeChunk

The gate shall demonstrate:

* real PostgreSQL vector persistence;
* deterministic application behavior;
* metadata-constrained retrieval;
* semantic retrieval correctness.

LLM answer generation is not required for this Day 3 gate.

---

# **67. Risks and Mitigations**

| Risk | Impact | Mitigation |
| ----- | ----- | ----- |
| pgvector unavailable in target environment | High | pre-deployment package/extension verification |
| embedding provider unavailable | Medium | explicit FAILED state, bounded retry |
| provider/model configuration mismatch | High | startup/service validation and dimension checks |
| dimension mismatch | High | reject before persistence |
| poor chunking | Medium | deterministic tests + retrieval acceptance corpus |
| poor semantic retrieval | High | golden-query evaluation before acceptance |
| stale index after source edit | High | explicit lifecycle/reindex contract |
| partial reindex | High | prepare externally, atomically replace |
| accidental sensitive ingestion | High | explicit Knowledge Base authority |
| unnecessary infrastructure growth | Medium | no ANN/queue/vector DB absent evidence |
| vendor dependency | Medium | application-owned provider abstraction |
| regression of existing product | High | mandatory full regression gates |

---

# **68. Deferred Evolution**

Future approved specifications may introduce:

* alternative embedding providers;
* model upgrades;
* ANN indexing;
* automated content synchronization;
* richer source metadata;
* source citations in AI answers;
* adjacent-chunk expansion;
* hybrid lexical/vector retrieval;
* asynchronous indexing;
* larger corpora;
* retrieval evaluation automation.

None of these are requirements for SPEC-004 v1.0.0.

---

# **69. Approval Statement**

SPEC-004 version 1.0.0 establishes the approved implementation contract for the Release 2 Knowledge Base and semantic retrieval capability.

Approval authorizes implementation only within the boundaries established by ADR-006 and this specification.

Implementation shall not introduce:

* a dedicated vector database;
* ANN indexing;
* worker infrastructure;
* self-hosted embedding runtime;
* an AI orchestration framework;
* public LLM/chat behavior;

without an approved requirement and architectural decision.

Day 3 acceptance requires the Knowledge Base retrieval pipeline to be operational and validated before Release 2 proceeds to IA Jujuju answer-generation behavior.

---

# **70. Revision History**

| Version | Date | Authority | Description |
| ----- | ----- | ----- | ----- |
| 1.0.0 | 2026-08-31 | Product Engineering | Initial Release 2 Knowledge Base and Retrieval specification derived from ADR-006. |
| 1.0.0 | 2026-08-31 | Product Owner | Approved Baseline for Day 3 implementation. |

---

# **End of Document**
