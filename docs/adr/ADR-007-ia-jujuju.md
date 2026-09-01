# ADR-007 — IA Jujuju, LLM and Conversation Architecture

**Status:** Accepted
**Date:** 2026-08-31
**Decision Type:** Architecture
**Release:** Release 2 — Day 4
**Scope:** IA Jujuju, LLM generation, RAG orchestration, conversation persistence, public interaction, security, privacy, and operational controls

---

## 1. Context

Release 2 introduces IA Jujuju as the public AI assistant of the portfolio.

Release 2 Day 3 established the Knowledge Base and vector retrieval foundation defined by ADR-006 and SPEC-004.

The existing retrieval architecture provides:

- curated `KnowledgeDocument` content;
- derived `KnowledgeChunk` records;
- PostgreSQL with pgvector;
- 1024-dimensional embeddings;
- OpenAI embedding integration;
- provider isolation;
- deterministic chunking;
- metadata filtering;
- exact cosine similarity retrieval;
- initial `top_k = 5`;
- stale-valid-index preservation;
- administrative Knowledge Base management;
- retrieval source traceability.

Day 4 must consume this existing retrieval boundary rather than redesign or duplicate it.

IA Jujuju must provide a controlled public assistant capable of answering questions about the professional portfolio using approved Knowledge Base content.

The assistant is not intended to operate as a general-purpose autonomous agent.

The implementation must preserve the existing Django Modular Monolith and must not introduce unnecessary infrastructure such as a separate AI service, dedicated AI database, message broker, worker infrastructure, SPA framework, or independent authentication system.

---

## 2. Requirements

The architecture must support:

1. a public assistant identified as **IA Jujuju**;
2. anonymous visitor interaction;
3. English and Brazilian Portuguese;
4. retrieval-augmented generation using the existing Day 3 retrieval service;
5. controlled context construction;
6. controlled system instructions;
7. grounded LLM responses;
8. conversation persistence;
9. user and assistant message persistence;
10. retrieval/source traceability;
11. Django Admin inspection;
12. recoverable provider failures;
13. protection against prompt injection and untrusted content;
14. configurable operational limits;
15. server-side provider credentials;
16. bounded provider calls;
17. data minimization and configurable retention;
18. preservation of the existing Homepage responsive behavior;
19. accessibility of the public AI interaction;
20. testability without live provider access.

---

## 3. Constraints

The following constraints apply:

- Django remains the application platform.
- The system remains a Modular Monolith.
- PostgreSQL remains the application database.
- The existing Knowledge Base and retrieval implementation are authoritative for RAG.
- OpenAI is the approved AI provider.
- Provider SDK objects must not leak into application or domain contracts.
- Views and templates must not call the OpenAI SDK directly.
- Models must not call the OpenAI SDK directly.
- Provider network calls must not execute inside long database transactions.
- Secrets must be provided through environment-based configuration.
- Normal automated tests must not require live OpenAI access.
- Existing Homepage, Contact, Portfolio, Header, Footer, analytics, SEO, i18n, accessibility, and responsive behavior remain regression authorities.
- Release 2 must remain within the approved delivery schedule.
- Operational cost must remain proportional to the expected low initial traffic.

---

## 4. Decision Drivers

The primary decision drivers are, in order:

1. correctness;
2. grounded answers;
3. simplicity;
4. maintainability;
5. testability;
6. security;
7. predictable operational cost;
8. failure isolation;
9. provider replaceability;
10. future evolution.

The assistant must favor refusing or acknowledging missing portfolio knowledge over fabricating unsupported professional information.

---

## 5. Alternatives Considered

### 5.1 Direct OpenAI SDK calls from Django views

**Advantages**

- minimal initial code;
- low implementation effort.

**Disadvantages**

- couples presentation to provider infrastructure;
- weak test isolation;
- provider-specific response objects leak across boundaries;
- complicates retries and error handling;
- reduces provider replaceability;
- conflicts with the existing architecture.

**Decision:** Rejected.

---

### 5.2 Dedicated AI microservice

**Advantages**

- strong deployment isolation;
- independent scaling;
- independent runtime lifecycle.

**Disadvantages**

- unnecessary network boundary;
- additional deployment and observability complexity;
- additional authentication and failure modes;
- increased operational cost;
- no demonstrated traffic or scaling requirement.

**Decision:** Rejected.

---

### 5.3 Asynchronous queue and worker infrastructure

Examples include Celery, Redis, or equivalent worker infrastructure.

**Advantages**

- asynchronous execution;
- useful for long-running or high-volume workloads.

**Disadvantages**

- additional infrastructure;
- additional operational failure modes;
- increased deployment complexity;
- unnecessary for the expected initial traffic and interaction latency.

**Decision:** Deferred.

---

### 5.4 Synchronous provider integration behind an application-owned abstraction

**Advantages**

- simple architecture;
- provider isolation;
- deterministic orchestration;
- straightforward testing;
- compatible with current expected traffic;
- no new infrastructure.

**Disadvantages**

- HTTP request latency includes provider latency;
- requires explicit timeout and failure handling.

**Decision:** Accepted.

---

## 6. Architecture Decision

IA Jujuju SHALL be implemented inside the existing Django Modular Monolith as an isolated application capability.

The conceptual request flow SHALL be:

```text
Public UI
    ↓
Django HTTP boundary
    ↓
IA Jujuju Application Service
    ↓
Input validation
    ↓
Conversation persistence
    ↓
Existing Retrieval Service
    ↓
Controlled Context Builder
    ↓
Prompt Builder
    ↓
LLM Provider abstraction
    ↓
OpenAI adapter
    ↓
Response validation
    ↓
Assistant message + retrieval traceability persistence
    ↓
Public response
```

The AI application layer SHALL coordinate the workflow.

Presentation code SHALL NOT contain provider-specific orchestration.

---

## 7. LLM Provider

OpenAI is selected as the initial LLM provider.

The application SHALL define an application-owned provider interface.

A conceptual provider contract SHALL accept structured application data rather than provider-specific SDK structures.

The contract SHALL support, at minimum:

* controlled system instructions;
* user question;
* controlled retrieved context;
* response language;
* bounded output configuration.

The provider SHALL return an application-owned result.

Provider-specific SDK objects SHALL remain confined to the OpenAI integration adapter.

A test-only fake provider MAY implement the same interface.

A fake provider MUST NOT be selectable as a production fallback.

---

## 8. OpenAI API Surface

The OpenAI **Responses API** is selected as the initial generation API surface.

The integration SHALL use the installed supported OpenAI Python SDK contract.

Provider calls SHALL:

* use explicit timeout configuration;
* use bounded retries only for transient failures;
* apply a bounded output limit;
* avoid enabling unnecessary provider tools;
* avoid internet browsing;
* avoid autonomous tool execution.

The application SHALL NOT depend on provider-managed conversation state as the authoritative conversation store.

PostgreSQL remains the application authority for conversation persistence.

---

## 9. Initial LLM Model

The initial generation model SHALL be:

`gpt-5.6-luna`

The model is selected for the initial portfolio workload because the assistant:

* operates over controlled RAG context;
* primarily answers professional portfolio questions;
* requires EN/PT-BR support;
* is expected to have low initial traffic;
* does not require high-complexity autonomous reasoning;
* benefits from low per-request operational cost.

The model identifier SHALL be environment-configurable.

Application architecture SHALL NOT depend on model-specific behavior that prevents model substitution.

A higher-capability compatible model MAY be evaluated if acceptance testing demonstrates insufficient response quality.

Changing the configured compatible model SHALL not by itself require an architectural redesign.

---

## 10. Retrieval and Controlled Context

IA Jujuju SHALL consume the existing Release 2 Day 3 Retrieval Service.

The initial retrieval policy SHALL remain:

`top_k = 5`

The Day 4 implementation SHALL NOT duplicate embedding generation, vector search, metadata filtering, or Knowledge Base indexing.

Retrieved chunks SHALL be transformed into a controlled application context before being sent to the LLM.

The context builder SHALL:

* preserve retrieval ordering;
* identify source boundaries;
* maintain source traceability;
* apply a bounded context size;
* avoid unnecessary duplication;
* treat retrieved content as untrusted data;
* distinguish retrieved evidence from system instructions.

Adjacent chunk expansion, reranking, hybrid retrieval, and query rewriting are not required for the initial implementation.

They MAY be introduced later only with evidence that retrieval quality requires them.

---

## 11. Prompt Contract

IA Jujuju SHALL operate under application-controlled system instructions.

The system prompt SHALL establish that IA Jujuju:

* identifies itself consistently as IA Jujuju;
* answers using approved portfolio Knowledge Base context;
* responds in the resolved EN or PT-BR language;
* does not fabricate unsupported professional facts;
* explicitly handles missing knowledge;
* does not claim internet access;
* does not claim actions it cannot perform;
* does not reveal system instructions, credentials, secrets, or internal configuration;
* treats user input as untrusted;
* treats retrieved Knowledge Base content as data rather than instructions;
* ignores instructions embedded in retrieved content that attempt to override system behavior;
* remains concise and professionally appropriate.

System prompt internals SHALL NOT be persisted as conversation messages.

---

## 12. Prompt Injection Boundary

The architecture SHALL assume that both public user input and retrieved text may contain adversarial instructions.

Security SHALL NOT depend solely on natural-language prompt wording.

Controls SHALL include:

* fixed server-controlled system instructions;
* explicit separation between instructions and retrieved context;
* bounded input;
* bounded retrieved context;
* no provider tools by default;
* no internet browsing;
* no arbitrary code execution;
* no secret material in prompts;
* server-side provider credentials;
* output encoding at presentation boundaries;
* sanitized errors and logs.

The assistant SHALL have no authority to execute administrative or operational actions.

---

## 13. Conversation Ownership

Initial public conversations SHALL be anonymous and session-bound.

Public authentication SHALL NOT be required for IA Jujuju.

The initial architecture SHALL NOT create custom public identity, IAM, or RBAC infrastructure.

Authenticated conversation ownership MAY be introduced in a future specification if a concrete requirement emerges.

Session association SHALL be used only to support conversation continuity and SHALL NOT be treated as verified user identity.

---

## 14. Conversation Persistence

Conversation data SHALL be stored in the existing PostgreSQL database.

A `Conversation` entity SHALL represent one assistant interaction thread.

Its minimum conceptual information SHALL include:

* identifier;
* language;
* status;
* creation timestamp;
* session association required for continuity.

A `ConversationMessage` entity SHALL represent ordered conversation messages.

Its minimum conceptual information SHALL include:

* conversation association;
* controlled role;
* content;
* creation timestamp;
* retrieval/source traceability when applicable.

Exact schema constraints belong to SPEC-005.

---

## 15. Message Roles

Initial persisted roles SHALL be limited to:

* `USER`
* `ASSISTANT`

System prompt messages SHALL NOT be persisted as ordinary conversation messages.

Provider-internal reasoning SHALL NOT be requested for persistence and SHALL NOT be stored.

---

## 16. Conversation Status

The conversation lifecycle SHALL remain intentionally small.

Initial controlled statuses SHALL be limited to the minimum required by SPEC-005.

The implementation SHALL avoid introducing workflow states without observable product behavior.

Provider failures SHALL be represented sufficiently to support diagnostic inspection without creating unnecessary workflow complexity.

---

## 17. Retrieval and Source Traceability

Assistant responses generated from RAG SHALL preserve sufficient retrieval evidence for operational diagnosis and future source presentation.

Traceability SHALL preserve the relationship between an assistant response and the Knowledge Base evidence used to produce it.

The persisted representation SHOULD include the minimum information necessary to determine:

* source document;
* retrieved chunk;
* retrieval rank;
* similarity/distance information where useful;
* relevant source metadata;
* retrieval time or response association.

The implementation SHALL avoid unnecessary duplication of full Knowledge Base content.

The exact relational/snapshot representation SHALL be defined by SPEC-005.

---

## 18. Transaction Boundaries

External LLM provider calls SHALL NOT execute inside long-running PostgreSQL transactions.

The orchestration SHALL follow this general sequence:

resolve/create conversation
    ↓
persist user message
    ↓
retrieve Knowledge Base evidence
    ↓
build controlled context
    ↓
build controlled prompt
    ↓
call LLM provider outside DB transaction
    ↓
validate provider result
    ↓
short atomic persistence of:
    assistant message
    retrieval traceability
    conversation state

Provider failure SHALL NOT roll back an already accepted user message merely because the external provider is unavailable.

The application SHALL return a sanitized recoverable failure state.

A failed provider response SHALL NOT be replaced by fabricated assistant content.

---

## 19. Public Interaction Architecture

The initial public interaction SHALL use the existing Django presentation architecture.

The preferred implementation is:

* Django endpoint;
* Django Templates;
* HTMX interaction;
* minimal JavaScript only where necessary.

A SPA or frontend framework SHALL NOT be introduced.

Streaming responses are not required for the initial release.

The public interaction SHALL support:

* question submission;
* loading state;
* assistant response;
* recoverable error state;
* conversation continuity.

---

## 20. Homepage Integration

The existing Homepage AI/RAG visual element SHALL evolve from a decorative reserved element into an accessible IA Jujuju interaction entry point.

The existing responsive composition SHALL remain authoritative.

The implementation SHALL minimize visual blast radius and preserve:

* existing Homepage composition;
* responsive behavior;
* Header behavior;
* Footer clearance;
* Contact navigation;
* accessibility;
* existing approved assets and layout unless interaction requires a minimal change.

The existing noninteractive semantics SHALL be intentionally replaced by appropriate interactive and accessible semantics.

This semantic change is an approved Release 2 evolution and SHALL NOT be treated as a Release 1.1 regression.

---

## 21. Django Admin

Conversation information SHALL be inspectable through authenticated Django Admin.

The initial Admin behavior SHALL be diagnostic/read-oriented.

Administrators SHALL be able to inspect conversations, messages, status, language, timestamps, and relevant retrieval/source evidence.

The initial release SHALL NOT introduce:

* conversation editing;
* assistant response editing;
* CRM functionality;
* analytics dashboards;
* exports;
* operator chat.

Existing Django authentication and authorization remain authoritative.

---

## 22. Privacy and Data Minimization

Visitor questions SHALL be treated as potentially containing personal or sensitive information.

The system SHALL:

* collect only data necessary for assistant operation;
* avoid unnecessary identity collection;
* avoid persisting system prompts or provider internals;
* avoid storing credentials or secrets in conversations;
* sanitize operational logs;
* restrict conversation inspection through Django Admin authorization.

No legal retention requirement is inferred by this ADR.

---

## 23. Retention

Conversation retention SHALL be configurable.

The initial operational default SHALL be:

`90 days`

This value is a product and operational decision, not a legal conclusion.

The retention mechanism SHALL permit future adjustment without schema redesign.

A proportional purge mechanism MAY reuse existing project operational patterns.

---

## 24. Cost and Consumption Control

IA Jujuju SHALL be designed for bounded and observable AI consumption.

Cost control SHALL rely primarily on technical limits rather than on a large prepaid balance.

Controls SHALL include:

* bounded user input;
* bounded retrieval context;
* initial `top_k = 5`;
* bounded model output;
* provider timeout;
* bounded retries;
* no unnecessary provider tools;
* configurable model;
* configurable operational limits;
* proportional abuse protection.

The initial expected workload is low-volume public portfolio interaction.

An initial OpenAI operational funding amount of approximately **US$ 5** is considered sufficient for development, validation, and initial low-volume production usage, subject to actual provider billing conditions and observed consumption.

The funding amount is an operational starting point and SHALL NOT be treated as an architectural dependency.

Additional funding SHALL be based on measured consumption rather than speculative traffic.

---

## 25. Abuse Protection

The public assistant creates a provider-backed cost surface and therefore requires proportional abuse protection.

The initial implementation SHALL avoid heavyweight distributed rate-limiting infrastructure unless actual traffic requires it.

At minimum the implementation SHALL provide:

* bounded request size;
* bounded output;
* request validation;
* provider timeout;
* bounded retry behavior;
* session/request-level protection appropriate to the current architecture.

More advanced distributed rate limiting MAY be introduced if production evidence demonstrates need.

---

## 26. Failure Model

Provider and orchestration failures SHALL be classified into application-owned categories.

At minimum the design SHALL distinguish:

* invalid application input;
* retrieval failure;
* provider timeout;
* transient provider failure;
* provider rejection or invalid request;
* malformed or unusable provider response;
* internal persistence failure.

Public error responses SHALL be sanitized.

Provider credentials, raw exception internals, system prompts, and sensitive configuration SHALL NOT be exposed to visitors.

Operational logs SHALL contain sufficient diagnostic information without unnecessarily recording visitor content.

---

## 27. Configuration

AI configuration SHALL be environment-based.

Configuration SHALL include, as applicable:

* OpenAI API key;
* generation model;
* provider timeout;
* output limit;
* retrieval/context limits;
* retention period;
* retry policy;
* operational protection limits.

Secrets SHALL NOT be committed to Git.

Production configuration SHALL fail safely when required provider credentials are unavailable.

---

## 28. Testing Strategy

The architecture SHALL support automated testing without live OpenAI access.

Tests SHALL include proportional coverage of:

### Unit

* context construction;
* prompt construction;
* language behavior;
* provider abstraction;
* provider response normalization;
* provider failure classification;
* input/output limits;
* source traceability transformation.

### Integration

* conversation persistence;
* message ordering and persistence;
* retrieval integration;
* source metadata persistence;
* orchestration;
* provider failure behavior;
* transaction boundaries.

### Admin

* authorization;
* conversation inspection;
* message inspection;
* read-oriented behavior.

### Public

* endpoint behavior;
* CSRF;
* invalid input;
* EN;
* PT-BR;
* conversation continuity;
* success response;
* recoverable failure.

### Regression

* Homepage;
* responsive behavior;
* Header;
* Footer;
* Contact;
* Portfolio;
* Django Admin;
* analytics;
* SEO;
* i18n;
* accessibility.

Live OpenAI calls SHALL NOT be part of the normal automated test suite.

Controlled manual provider smoke tests MAY be executed separately when explicitly authorized.

---

## 29. Observability

Initial observability SHALL remain proportional to the application scale.

The system SHOULD make it possible to diagnose:

* provider failures;
* retrieval failures;
* response latency;
* conversation failures;
* indexing/retrieval relationship;
* unexpected consumption patterns.

Logs SHALL NOT expose:

* API keys;
* system prompts;
* raw provider credentials;
* unnecessary visitor content.

Advanced AI observability platforms are not required for the initial release.

---

## 30. Decision Matrix

### D1 — LLM Provider

**Decision:** OpenAI.

**Rationale:** Existing provider relationship and SDK integration, current embedding integration, suitable generation models, and reduced integration complexity.

---

### D2 — Initial LLM Model

**Decision:** `gpt-5.6-luna`.

**Rationale:** Appropriate cost/quality profile for controlled portfolio RAG with expected low initial traffic.

The model SHALL remain configurable.

---

### D3 — Provider API Surface

**Decision:** OpenAI Responses API.

**Rationale:** Current provider generation interface appropriate for the new implementation.

---

### D4 — Provider Abstraction

**Decision:** Application-owned `LLMProvider` abstraction.

**Rationale:** Testability, provider isolation, failure normalization, and future model/provider evolution.

---

### D5 — Controlled Context

**Decision:** Reuse the Day 3 Retrieval Service with initial `top_k = 5`, bounded context, source boundaries, and no initial reranking/hybrid retrieval.

---

### D6 — Prompt Contract

**Decision:** Server-controlled system instructions with grounded-answer rules, EN/PT-BR behavior, explicit missing-knowledge behavior, and prompt-injection boundaries.

---

### D7 — Conversation Persistence

**Decision:** PostgreSQL-backed anonymous, session-bound conversations.

Public authentication is not required.

---

### D8 — Conversation Messages

**Decision:** Persist controlled `USER` and `ASSISTANT` messages.

System prompt internals and provider reasoning SHALL NOT be persisted as conversation messages.

---

### D9 — Source Traceability

**Decision:** Persist structured retrieval evidence associated with assistant responses using the minimum representation required for audit, debugging, and future source presentation.

Exact schema is delegated to SPEC-005.

---

### D10 — Public HTTP Interaction

**Decision:** Django endpoint using the existing server-rendered application architecture.

---

### D11 — UI Interaction

**Decision:** Django Templates + HTMX with minimal JavaScript where necessary.

The existing Homepage AI visual becomes the accessible IA Jujuju launcher without a Homepage redesign.

---

### D12 — Provider Failure

**Decision:** Sanitized recoverable error.

Previously persisted user input is preserved.

No fabricated assistant answer is stored or returned.

---

### D13 — Retention

**Decision:** Configurable retention with an initial default of 90 days.

The value is operational/product policy and may be changed without architectural redesign.

---

### D14 — Abuse Protection

**Decision:** Proportional application-level controls initially.

No Redis or distributed rate-limit infrastructure without demonstrated need.

---

### D15 — Operational Configuration

**Decision:** Provider credentials, model, timeout, output/context limits, retries, retention, and relevant operational limits are environment-configurable.

Initial OpenAI funding may start at approximately US$ 5 and increase according to measured usage.

---

## 31. Consequences

### Positive

* preserves the Modular Monolith;
* reuses the completed Day 3 RAG foundation;
* isolates provider dependencies;
* supports deterministic automated testing;
* maintains low operational complexity;
* maintains low initial AI cost;
* supports EN/PT-BR;
* preserves conversation traceability;
* supports future model substitution;
* provides controlled failure behavior;
* avoids unnecessary infrastructure.

### Negative

* synchronous provider calls increase request latency;
* anonymous session ownership is not durable verified identity;
* application-level abuse protection is less powerful than distributed infrastructure;
* response quality depends on Knowledge Base quality, retrieval quality, prompt quality, and selected model;
* conversation persistence creates a new privacy and retention responsibility.

### Accepted Trade-offs

These limitations are accepted because they match the current portfolio scale and Release 2 delivery constraints.

Architecture SHALL evolve only when production evidence demonstrates a concrete requirement.

---

## 32. Deferred Decisions

The following are explicitly deferred:

* streaming generation;
* WebSockets;
* autonomous agents;
* arbitrary tool calling;
* internet search;
* dedicated AI microservice;
* dedicated vector database;
* Celery;
* Redis;
* distributed rate limiting;
* reranking;
* hybrid retrieval;
* query rewriting;
* authenticated visitor conversations;
* conversation export;
* CRM functionality;
* operator chat;
* AI analytics dashboard;
* advanced external AI observability platform;
* multi-provider production routing.

These items require separate requirements and impact analysis before implementation.

---

## 33. Implementation Impact

Expected implementation areas include:

* new IA Jujuju Django application capability;
* conversation models and migrations;
* LLM provider abstraction;
* OpenAI provider adapter;
* controlled context builder;
* prompt builder;
* orchestration/application service;
* public HTTP interaction;
* Homepage launcher evolution;
* Django Admin conversation inspection;
* environment configuration;
* automated tests;
* SPEC-005.

Exact files and implementation contracts SHALL be defined from repository evidence and SPEC-005.

---

## 34. Acceptance of Architecture

ADR-007 is accepted when:

1. the architecture preserves the Django Modular Monolith;
2. the existing Day 3 retrieval boundary remains authoritative;
3. OpenAI access is isolated behind an application-owned provider;
4. `gpt-5.6-luna` is configurable rather than architecturally hardcoded;
5. controlled context and prompt boundaries are explicit;
6. conversation persistence is separated from provider state;
7. provider calls remain outside long database transactions;
8. source traceability is preserved;
9. public interaction remains accessible and server-oriented;
10. privacy, retention, cost, failure, and abuse controls are explicit;
11. automated testing does not depend on live OpenAI access;
12. deferred functionality does not enter Day 4 without a new requirement.

---

## 35. Traceability

This ADR refines the approved Release 2 IA/RAG evolution and depends on the Knowledge Base and vector retrieval architecture established by ADR-006 and SPEC-004.

Detailed functional contracts, data constraints, HTTP behavior, UI states, source metadata representation, validation rules, and acceptance tests SHALL be specified by SPEC-005 — IA Jujuju Assistant and Conversation.

Traceability chain:

Requirement
 → ADR-006 / SPEC-004 retrieval foundation
 → ADR-007 IA Jujuju architecture
 → SPEC-005 assistant and conversation specification
 → implementation
 → automated tests
 → validation evidence
 → Product Owner acceptance
