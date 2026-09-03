# KNOWLEDGE-CONTENT-BASELINE-001

Document-ID: KNOWLEDGE-CONTENT-BASELINE-001
Version: 1.0.0
Status: HUMAN APPROVED
Scope: Waves 1–5 — Approved Editorial Corpus
Knowledge Concepts: 29
KnowledgeDocuments: 58

Editorial corpus cardinality:

- 29 Knowledge Concepts
- 58 KnowledgeDocument language variants

This cardinality certifies approved editorial corpus scope only. It does not certify Django materialization, persistence, chunking, embeddings, pgvector population, indexing, retrieval validation, grounded-answer validation, PCS-002 documentary consolidation, or Release 2 Production Deployment closure.

Languages:

- pt-br
- en

Operational state:

Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

## 1. Purpose

KNOWLEDGE-CONTENT-BASELINE-001 is the authoritative, version-controlled editorial baseline for the approved Wave 1 through Wave 5 Knowledge Content of IA Jujuju.

Editorial approval is not equivalent to database persistence, chunk generation, embedding generation, vector indexing, retrieval validation, or grounded-answer validation.

This document is the source authority from which approved content may later be materialized as Django `KnowledgeDocument` records.

## 2. Knowledge Governance

### 2.1 Evidence Authority

Evidence authority levels:

- A — Production Evidence
- B — Implemented Evidence
- C — Designed / Specified
- D — Historical / Legacy

Evidence authority is assigned at claim granularity.

When evidence conflicts, use this precedence principle:

`current approved artifact > historical review > roadmap > informational README`

and:

`implemented + tested evidence > architectural intention`

Temporal context must be preserved.

### 2.2 Maturity Language Rule

Normative rule:

Never use tense or wording that elevates the proven maturity level of a project, capability, or feature.

Maturity vocabulary:

| Intention | Vocabulary |
| --- | --- |
| future intention | planned |
| technical design | designed |
| specification | specified |
| construction | implemented |
| verification | validated |
| operation | deployed to production |

Apply maturity at feature/claim granularity. PT-BR and EN must preserve equivalent maturity.

Pipeline:

`Evidence → Maturity → Claim → PT-BR / EN`

### 2.3 Bilingual Factual Equivalence

Normative rule:

`1 Knowledge Concept → 2 KnowledgeDocuments → 2 languages → 1 factual truth`

PT-BR and EN are first-class Knowledge Base languages. The two language versions do not need to be literal translations, but must preserve:

- the same evidence;
- the same factual claims;
- the same maturity;
- the same limitations;
- the same authority;
- the same professional meaning.

No language may contain a stronger claim than its counterpart.

### 2.4 Capability Evidence Rule — CER-01

Professional capabilities and specialties should, whenever available, be supported not only by approved professional declarations but also by project-level specification, implementation, testing, validation, and production evidence.

The maturity of each claim must not exceed the strongest evidence available for that specific capability.

A technology appearing in an approved skill dataset does not automatically prove implementation or production experience.

### 2.5 Capability Evidence Ladder

| Level | Name | Evidence | Permitted meaning |
| --- | --- | --- | --- |
| E1 | Declared | approved professional profile or skill dataset | declared/approved professional capability |
| E2 | Specified | specification, ADR, architecture, or equivalent design authority | specified or designed capability |
| E3 | Implemented | implementation/code/implementation closure | implemented capability |
| E4 | Validated | tests, quality gates, validation evidence | implemented and validated capability |
| E5 | Production | deployment plus production validation | capability demonstrated in production |

Normative rule:

The wording of a professional capability must never exceed the highest evidence level established for that specific claim.

E5 does NOT represent an abstract proficiency certification. It means that evidence for the specific capability reached production.

### 2.6 Traceability

Traceability model:

`Source → Evidence Authority → Knowledge Concept → Factual Claim → Maturity → Language → KnowledgeDocument → KnowledgeChunk → Vector → Retrieval → Answer → Evidence`

At the current baseline stage, the chain stops at approved KnowledgeDocument editorial content.

KnowledgeChunk, Vector, Retrieval, and Answer validation are future lifecycle stages and must not be marked complete.

### 2.7 Sensitive Information Exclusion

Knowledge content must not expose unnecessary operationally sensitive information.

Do not add:

- credentials;
- secrets;
- API keys;
- passwords;
- private session identifiers;
- internal authentication data;
- unnecessary infrastructure identifiers;
- sensitive environment values;
- private operational incident details.

Technical evidence may be described at the level necessary to demonstrate engineering capability without exposing sensitive data.

## 3. KnowledgeDocument Contract

Supported languages:

- en
- pt-br

Wave 1 uses categories:

- PROFILE
- EXPERIENCE
- SKILL

Each Knowledge Concept must have exactly one PT-BR and one EN KnowledgeDocument in this baseline.

Each KnowledgeDocument entry records:

- Knowledge Concept ID
- title
- slug
- language
- category
- approved editorial body
- editorial version
- approval status

## 4. Wave 1 — Core Professional Authority

### KB-PRF-001 — Professional Profile

#### Metadata

Category: PROFILE
Editorial Status: APPROVED
Editorial Version: 1.0

#### PT-BR

Title: Perfil Profissional — Luís França
Slug: professional-profile-pt-br
Language: pt-br

##### Approved Content

Luís França é Engenheiro de Software com especialização em desenvolvimento backend Python, automação e aplicações de Inteligência Artificial e Large Language Models (LLMs). Seu trabalho é orientado à construção de software manutenível, testável e preparado para operação em produção.

Sua abordagem de engenharia conecta requisitos, especificação, arquitetura, implementação, testes automatizados, validação e entrega. Em projetos estruturados, utiliza Specification-Driven Development (SDD) para manter rastreabilidade entre decisões de produto e engenharia, implementação, testes e evidências de aceitação.

Suas competências incluem engenharia backend com Python, arquitetura de software, APIs e integrações, bancos de dados relacionais, automação, testes e qualidade de software, além da integração de aplicações com IA e LLMs. Seu trabalho recente também demonstra implementação de Retrieval-Augmented Generation (RAG), embeddings e busca vetorial em uma aplicação implantada em produção.

Luís adota uma abordagem pragmática para arquitetura e seleção tecnológica: busca soluções proporcionais aos requisitos reais, priorizando correção, simplicidade, manutenibilidade, testabilidade, segurança e viabilidade operacional. Tecnologias e padrões são selecionados de acordo com o problema e suas restrições, evitando complexidade desnecessária.

Seu portfólio é utilizado não apenas para apresentar projetos, mas também para demonstrar o processo de engenharia aplicado à construção de software, incluindo especificação, decisões arquiteturais, implementação, validação, documentação e entrega em produção.

#### EN

Title: Professional Profile — Luís França
Slug: professional-profile-en
Language: en

##### Approved Content

Luís França is a Software Engineer specializing in Python backend development, automation, and Artificial Intelligence and Large Language Model (LLM) applications. His work focuses on building maintainable, testable software designed for production operation.

His engineering approach connects requirements, specification, architecture, implementation, automated testing, validation, and delivery. In structured projects, he uses Specification-Driven Development (SDD) to maintain traceability between product and engineering decisions, implementation, testing, and acceptance evidence.

His skills include Python backend engineering, software architecture, APIs and integrations, relational databases, automation, software testing and quality engineering, and the integration of applications with AI and LLMs. His recent work also demonstrates the implementation of Retrieval-Augmented Generation (RAG), embeddings, and vector retrieval in a production-deployed application.

Luís takes a pragmatic approach to architecture and technology selection, seeking solutions proportional to actual requirements and prioritizing correctness, simplicity, maintainability, testability, security, and operational viability. Technologies and patterns are selected according to the problem and its constraints, avoiding unnecessary complexity.

His portfolio is used not only to present projects but also to demonstrate the engineering process applied to software development, including specification, architectural decisions, implementation, validation, documentation, and production delivery.

#### Evidence / Maturity Notes

Professional Profile is supported by approved professional declarations together with historical and current project evidence. Specific capabilities span different evidence levels, including designed, implemented, validated, and production-demonstrated work, and each claim must retain the maturity established by its own supporting evidence under CER-01.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRF-002 — Multidisciplinary Background

#### Metadata

Category: PROFILE
Editorial Status: APPROVED
Editorial Version: 1.1

#### PT-BR

Title: Formação e Trajetória Multidisciplinar — Luís França
Slug: multidisciplinary-background-pt-br
Language: pt-br

##### Approved Content

A trajetória profissional de Luís França é multidisciplinar e reúne experiências em tecnologia, arquitetura, Building Information Modeling (BIM), construção e gestão. Essa formação antecede e complementa sua atuação atual em Engenharia de Software.

Ainda no início de sua trajetória profissional com projetos arquitetônicos, Luís desenvolveu código em AutoLISP para AutoCAD com o objetivo de automatizar a produção de desenhos técnicos de projetos arquitetônicos. Essa experiência representa uma aplicação inicial de programação e automação dentro de seu contexto profissional anterior à sua atuação atual em Engenharia de Software.

Sua experiência em diferentes disciplinas proporciona uma perspectiva que considera não apenas a implementação técnica, mas também requisitos, organização de sistemas, processos, restrições, documentação, validação e entrega. Na Engenharia de Software, essa visão multidisciplinar é aplicada de forma estruturada, respeitando as práticas e evidências próprias da disciplina.

Atualmente, sua atuação está concentrada em Engenharia de Software, com especialização em desenvolvimento backend Python, automação e aplicações de Inteligência Artificial e Large Language Models (LLMs). Sua trajetória anterior permanece relevante como contexto profissional e contribui para uma abordagem orientada à análise de problemas, estruturação de soluções e integração entre requisitos técnicos e objetivos do produto.

Seu portfólio reflete também essa evolução profissional: projetos históricos registram etapas anteriores de desenvolvimento de software, enquanto projetos mais recentes demonstram uma abordagem progressivamente mais estruturada em especificação, arquitetura, testes, validação e entrega em produção.

#### EN

Title: Multidisciplinary Background — Luís França
Slug: multidisciplinary-background-en
Language: en

##### Approved Content

Luís França has a multidisciplinary professional background spanning technology, architecture, Building Information Modeling (BIM), construction, and management. This background predates and complements his current work in Software Engineering.

Early in his professional work with architectural projects, Luís developed AutoLISP code for AutoCAD to automate the production of technical drawings for architectural projects. This experience represents an early application of programming and automation within his professional context prior to his current work in Software Engineering.

His experience across different disciplines provides a perspective that considers not only technical implementation but also requirements, system organization, processes, constraints, documentation, validation, and delivery. In Software Engineering, this multidisciplinary perspective is applied in a structured manner while respecting the practices and evidence specific to the discipline.

His current work is focused on Software Engineering, specializing in Python backend development, automation, and Artificial Intelligence and Large Language Model (LLM) applications. His previous professional background remains relevant as context and contributes to an approach centered on problem analysis, solution structuring, and the integration of technical requirements with product objectives.

His portfolio also reflects this professional evolution: historical projects document earlier stages of software development, while more recent projects demonstrate a progressively more structured approach to specification, architecture, testing, validation, and production delivery.

#### Evidence / Maturity Notes

Multidisciplinary background approved as professional and historical context. The AutoLISP/AutoCAD experience is historical evidence and must not be retrospectively characterized with the engineering maturity of current Software Engineering projects.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-EXP-001 — Professional Experience

#### Metadata

Category: EXPERIENCE
Editorial Status: APPROVED
Editorial Version: 1.0

#### PT-BR

Title: Experiência Profissional — Luís França
Slug: professional-experience-pt-br
Language: pt-br

##### Approved Content

A experiência profissional de Luís França combina uma trajetória multidisciplinar anterior com sua atuação atual em Engenharia de Software. Seu histórico inclui atividades relacionadas a projetos arquitetônicos, Building Information Modeling (BIM), construção, gestão e tecnologia, seguidas por uma evolução progressiva de sua atuação em programação, automação e desenvolvimento de software.

A aplicação de programação a problemas profissionais aparece desde o início de sua trajetória com projetos arquitetônicos. Nesse período, Luís desenvolveu código em AutoLISP para AutoCAD para automatizar a produção de desenhos técnicos de projetos arquitetônicos. Essa experiência introduziu programação e automação como instrumentos para resolver um problema concreto de trabalho, antes de sua atuação atual em Engenharia de Software.

Sua evolução em desenvolvimento de software também é registrada por projetos históricos construídos com Python e diferentes abordagens de aplicação. Esses projetos documentam etapas anteriores de aprendizado e desenvolvimento, incluindo automação, consumo de APIs, interfaces desktop e aplicações web. Eles são preservados como evidência histórica de evolução e não são apresentados como se tivessem sido desenvolvidos com a mesma maturidade de engenharia de seus projetos atuais.

Em sua atuação atual em Engenharia de Software, Luís concentra-se principalmente em desenvolvimento backend Python, arquitetura de software, automação, APIs e integrações, bancos de dados relacionais, testes e qualidade de software e aplicações que integram Inteligência Artificial e Large Language Models (LLMs).

O Site Portfólio constitui uma das principais evidências atuais dessa atuação. O projeto evoluiu por meio de requisitos, especificações, decisões arquiteturais, implementação, testes automatizados, validação, documentação e implantação em produção. Sua evolução inclui backend Django e PostgreSQL, administração, comunicação, uma Knowledge Base vetorial e a IA Jujuju, que utiliza Retrieval-Augmented Generation (RAG), embeddings e recuperação vetorial.

Outros projetos representam diferentes níveis de maturidade. A Enterprise Platform possui uma extensa baseline de especificação e arquitetura e permanece em desenvolvimento. A Intelligent Currency Platform encontra-se em estágio inicial de implementação, com capacidades futuras de Machine Learning e Inteligência Artificial mantidas como roadmap. Projetos anteriores de cotação de moedas e gerenciamento de tarefas permanecem como registros históricos da evolução de sua prática de desenvolvimento de software.

Dessa forma, sua experiência é apresentada no portfólio com distinção explícita entre trajetória profissional, projetos históricos, capacidades atualmente demonstradas, sistemas em desenvolvimento e funcionalidades apenas planejadas.

#### EN

Title: Professional Experience — Luís França
Slug: professional-experience-en
Language: en

##### Approved Content

Luís França's professional experience combines an earlier multidisciplinary background with his current work in Software Engineering. His background includes activities related to architectural projects, Building Information Modeling (BIM), construction, management, and technology, followed by a progressive evolution of his work in programming, automation, and software development.

The application of programming to professional problems appears early in his work with architectural projects. During this period, Luís developed AutoLISP code for AutoCAD to automate the production of technical drawings for architectural projects. This experience introduced programming and automation as tools for solving a concrete work-related problem before his current work in Software Engineering.

His evolution in software development is also documented through historical projects built with Python and different application approaches. These projects record earlier stages of learning and development, including automation, API consumption, desktop interfaces, and web applications. They are preserved as historical evidence of evolution and are not presented as if they had been developed with the same engineering maturity as his current projects.

In his current Software Engineering work, Luís focuses primarily on Python backend development, software architecture, automation, APIs and integrations, relational databases, software testing and quality engineering, and applications integrating Artificial Intelligence and Large Language Models (LLMs).

The Site Portfolio is one of the primary current examples of this work. The project evolved through requirements, specifications, architectural decisions, implementation, automated testing, validation, documentation, and production deployment. Its evolution includes a Django and PostgreSQL backend, administration, communication capabilities, a vector-based Knowledge Base, and IA Jujuju, which uses Retrieval-Augmented Generation (RAG), embeddings, and vector retrieval.

Other projects represent different maturity levels. The Enterprise Platform has an extensive specification and architecture baseline and remains under development. The Intelligent Currency Platform is at an early implementation stage, with future Machine Learning and Artificial Intelligence capabilities maintained as roadmap items. Earlier currency quotation and task management projects remain historical records of the evolution of his software development practice.

His experience is therefore presented in the portfolio with an explicit distinction between professional background, historical projects, currently demonstrated capabilities, systems under development, and planned functionality.

#### Evidence / Maturity Notes

Professional experience combines approved professional background with project evidence at different maturity levels. Historical, planned, in-development, validated, and production claims must retain their respective evidence-based maturity.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-SKL-001 — Python & Backend Engineering

#### Metadata

Category: SKILL
Editorial Status: APPROVED
Editorial Version: 1.0

#### PT-BR

Title: Python e Engenharia Backend — Luís França
Slug: python-backend-engineering-pt-br
Language: pt-br

##### Approved Content

Python é uma das principais especialidades técnicas de Luís França e constitui a base de diferentes etapas de sua evolução em desenvolvimento de software, desde projetos históricos de automação e aplicações desktop e web até sistemas atuais estruturados por requisitos, arquitetura, testes e validação.

Em sua atuação atual, Luís utiliza Python principalmente em engenharia backend, automação, integrações e aplicações que incorporam Inteligência Artificial. Seu trabalho backend envolve responsabilidades como modelagem e persistência de dados, regras de aplicação, processamento de requisições HTTP, validação de entradas, integrações com serviços externos, tratamento de falhas, configuração por ambiente e construção de componentes projetados para serem testáveis e operáveis.

O Site Portfólio fornece uma evidência concreta dessa capacidade em produção. A aplicação utiliza Django em uma arquitetura de monólito modular e PostgreSQL para persistência. Seu backend sustenta funcionalidades como comunicação pelo formulário de contato, administração, gerenciamento da Knowledge Base e a infraestrutura da IA Jujuju. A aplicação foi submetida a testes automatizados e quality gates e implantada em ambiente de produção utilizando Gunicorn, Nginx e PostgreSQL.

A evolução do Site Portfólio também demonstra a extensão do backend para aplicações de IA. A Knowledge Base utiliza modelos relacionais e vetoriais no PostgreSQL, com pgvector para armazenamento e recuperação de embeddings. O backend integra providers externos por interfaces controladas e coordena recuperação semântica, construção de contexto e geração de respostas para a IA Jujuju.

Além do Django, o histórico e o conjunto profissional de Luís incluem contato com outras tecnologias e abordagens do ecossistema Python, como Flask, FastAPI, Pydantic e SQLAlchemy. Essas tecnologias representam experiências e níveis de maturidade distintos e não são apresentadas como equivalentes à evidência de implementação e operação em produção atualmente disponível para Django no Site Portfólio.

Sua abordagem de engenharia backend prioriza soluções proporcionais aos requisitos reais. Em vez de adicionar infraestrutura ou abstrações sem necessidade comprovada, busca manter responsabilidades claras, dependências externas isoladas, configuração segura por ambiente, persistência adequada ao problema e uma arquitetura que possa ser testada, implantada e evoluída de forma controlada.

#### EN

Title: Python & Backend Engineering — Luís França
Slug: python-backend-engineering-en
Language: en

##### Approved Content

Python is one of Luís França's primary technical specialties and provides the foundation for different stages of his software development evolution, from historical automation, desktop, and web projects to current systems structured through requirements, architecture, testing, and validation.

In his current work, Luís uses Python primarily for backend engineering, automation, integrations, and applications incorporating Artificial Intelligence. His backend work includes responsibilities such as data modeling and persistence, application rules, HTTP request processing, input validation, external service integrations, failure handling, environment-based configuration, and the development of components designed for testability and operation.

The Site Portfolio provides concrete production evidence of this capability. The application uses Django within a modular monolith architecture and PostgreSQL for persistence. Its backend supports capabilities including contact communication, administration, Knowledge Base management, and the infrastructure behind IA Jujuju. The application has been subjected to automated testing and quality gates and deployed to a production environment using Gunicorn, Nginx, and PostgreSQL.

The evolution of the Site Portfolio also demonstrates the extension of backend engineering into AI applications. Its Knowledge Base uses relational and vector data models in PostgreSQL, with pgvector for embedding storage and retrieval. The backend integrates external providers through controlled interfaces and coordinates semantic retrieval, context construction, and response generation for IA Jujuju.

In addition to Django, Luís's background and approved professional skill set include other technologies and approaches from the Python ecosystem, such as Flask, FastAPI, Pydantic, and SQLAlchemy. These technologies represent different experiences and maturity levels and are not presented as equivalent to the implementation and production-operation evidence currently available for Django in the Site Portfolio.

His backend engineering approach prioritizes solutions proportional to actual requirements. Rather than adding infrastructure or abstractions without demonstrated need, he seeks clear responsibilities, isolated external dependencies, secure environment-based configuration, persistence appropriate to the problem, and an architecture that can be tested, deployed, and evolved in a controlled manner.

#### Evidence / Maturity Notes

Python and backend engineering are approved professional capabilities. Django backend engineering in the Site Portfolio has production evidence; other technologies and experiences must retain only the maturity supported by their specific evidence under CER-01.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-SKL-002 — Software Architecture & Specification-Driven Development

#### Metadata

Category: SKILL
Editorial Status: APPROVED
Editorial Version: 1.0

#### PT-BR

Title: Arquitetura de Software e Specification-Driven Development — Luís França
Slug: software-architecture-sdd-pt-br
Language: pt-br

##### Approved Content

Arquitetura de Software e Specification-Driven Development (SDD) fazem parte da abordagem de engenharia utilizada por Luís França para transformar requisitos em software implementável, testável, documentado e operável. Em vez de tratar arquitetura como uma escolha isolada de tecnologias, seu processo relaciona requisitos, restrições, decisões técnicas, implementação, validação e evolução do sistema.

Em projetos estruturados, Luís utiliza SDD para estabelecer uma cadeia explícita de rastreabilidade entre requisito, decisão, especificação, implementação, teste, evidência e aceitação. Especificações e decisões arquiteturais funcionam como contratos de engenharia para orientar a implementação e fornecer critérios objetivos para verificar se o comportamento entregue corresponde ao que foi aprovado.

O Site Portfólio fornece uma evidência concreta da aplicação desse processo. Sua engenharia foi estruturada por artefatos que incluem Product Brief, Technical Specification, Architecture, API and Data Contracts, Testing and Acceptance, Deployment and Operations, Architecture Decision Records (ADRs), especificações de funcionalidades e baselines formais. Esses artefatos foram utilizados em conjunto com implementação, testes e evidências de validação durante a evolução do produto.

A arquitetura resultante prioriza proporcionalidade entre solução e problema. No Site Portfólio, isso levou à adoção de um monólito modular com Django e PostgreSQL em vez da introdução prematura de serviços distribuídos. Quando o produto evoluiu para incorporar uma Knowledge Base vetorial e Retrieval-Augmented Generation (RAG), a arquitetura reutilizou PostgreSQL com pgvector, evitando um banco vetorial separado sem necessidade comprovada.

Decisões arquiteturais relevantes são avaliadas considerando requisitos e restrições, alternativas possíveis e seus trade-offs, além de consequências para manutenção, testabilidade, segurança, desempenho, escalabilidade, complexidade operacional, custo e dívida técnica. Tecnologias e padrões são tratados como meios para atender ao problema, e não como objetivos independentes.

O processo também é aplicado de forma incremental. Mudanças em um sistema existente começam pela inspeção da baseline real, análise do impacto e preservação do comportamento aprovado sempre que possível. A implementação é então submetida a testes e validação antes de se tornar uma nova baseline. Essa abordagem permite evoluir o software sem perder a rastreabilidade entre intenção, decisão, código e evidência.

#### EN

Title: Software Architecture & Specification-Driven Development — Luís França
Slug: software-architecture-sdd-en
Language: en

##### Approved Content

Software Architecture and Specification-Driven Development (SDD) are part of the engineering approach Luís França uses to transform requirements into implementable, testable, documented, and operable software. Rather than treating architecture as an isolated choice of technologies, his process connects requirements, constraints, technical decisions, implementation, validation, and system evolution.

In structured projects, Luís uses SDD to establish an explicit traceability chain between requirement, decision, specification, implementation, test, evidence, and acceptance. Specifications and architectural decisions serve as engineering contracts that guide implementation and provide objective criteria for verifying whether the delivered behavior corresponds to what was approved.

The Site Portfolio provides concrete evidence of this process in practice. Its engineering was structured through artifacts including a Product Brief, Technical Specification, Architecture, API and Data Contracts, Testing and Acceptance, Deployment and Operations, Architecture Decision Records (ADRs), feature specifications, and formal baselines. These artifacts were used together with implementation, testing, and validation evidence throughout the evolution of the product.

The resulting architecture prioritizes proportionality between the solution and the problem. In the Site Portfolio, this led to the adoption of a Django and PostgreSQL modular monolith rather than the premature introduction of distributed services. When the product evolved to incorporate a vector-based Knowledge Base and Retrieval-Augmented Generation (RAG), the architecture reused PostgreSQL with pgvector, avoiding a separate vector database without a demonstrated need.

Relevant architectural decisions are evaluated by considering requirements and constraints, realistic alternatives and their trade-offs, and consequences for maintainability, testability, security, performance, scalability, operational complexity, cost, and technical debt. Technologies and patterns are treated as means to address the problem rather than as independent objectives.

The process is also applied incrementally. Changes to an existing system begin with inspection of the actual baseline, impact analysis, and preservation of approved behavior whenever possible. Implementation is then subjected to testing and validation before becoming a new baseline. This approach allows software to evolve without losing traceability between intent, decision, code, and evidence.

#### Evidence / Maturity Notes

Software Architecture and SDD are approved professional capabilities supported across multiple projects at different maturity levels. The Site Portfolio demonstrates specification, architectural decision-making, implementation, validation, and production delivery. Enterprise Platform and Intelligent Currency Platform provide additional specification and architecture evidence within their respective maturity levels, while the historical Currency Quotation System provides evidence of architectural evolution including MVC. Each architectural claim must retain its project-specific maturity under CER-01.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-SKL-003 — Testing, Quality & Delivery

#### Metadata

Category: SKILL
Editorial Status: APPROVED
Editorial Version: 1.0

#### PT-BR

Title: Testes, Qualidade e Entrega de Software — Luís França
Slug: testing-quality-delivery-pt-br
Language: pt-br

##### Approved Content

Testes, qualidade e entrega fazem parte do ciclo de engenharia utilizado por Luís França para transformar uma implementação em software verificável e operável. Sua abordagem relaciona critérios de aceitação, testes automatizados, análise estática, validações estruturais, inspeção das alterações, evidências de execução e validação antes da entrega.

Em projetos estruturados, os testes são derivados do comportamento esperado e das especificações aplicáveis, em vez de serem tratados apenas como uma etapa posterior à implementação. A estratégia combina testes adequados ao risco e à responsabilidade do componente, incluindo testes de comportamento e integração, regressão e verificações específicas das fronteiras entre aplicação, banco de dados e integrações externas.

O Site Portfólio fornece evidência concreta dessa prática. Durante sua evolução, funcionalidades de homepage, contato, administração, Knowledge Base, recuperação semântica e IA Jujuju foram submetidas a testes automatizados e validações de regressão. No fechamento de engenharia do Release 2, a suíte completa executada continha 577 testes aprovados, complementados por verificações de lint, tipagem estática, configuração Django, migrations, arquivos estáticos e integridade do diff.

A qualidade não é tratada apenas como execução de testes. Conforme o escopo da alteração, o processo utiliza ferramentas e verificações como pytest, Ruff, MyPy, Django system checks e `git diff --check`, além de inspeção do estado do repositório e das alterações efetivamente produzidas. O objetivo é detectar problemas de comportamento, integração, tipagem, configuração, consistência e regressão antes que uma mudança seja aceita.

A validação também é separada da implementação sempre que essa separação aumenta a confiabilidade da evidência. Alterações podem ser auditadas por Git e submetidas novamente aos quality gates em um ambiente de validação independente do agente ou ferramenta que realizou a implementação. O resultado técnico é então combinado com revisão e aceitação humana antes da progressão para a próxima baseline ou para uma implantação controlada.

No Site Portfólio, esse processo se estende até produção. A entrega inclui preparação e verificação do ambiente, dependências, banco de dados, migrations, arquivos estáticos, serviços de aplicação e proxy, seguida por validações operacionais e smoke tests do comportamento implantado. Funcionalidades críticas são consideradas concluídas somente de acordo com o nível de evidência exigido para seu escopo.

Essa abordagem não pressupõe que todos os projetos necessitem da mesma quantidade de testes, ferramentas ou gates. O nível de validação deve ser proporcional ao risco, à maturidade e às responsabilidades do sistema, preservando correção e confiança sem adicionar processo ou infraestrutura sem benefício comprovado.

#### EN

Title: Software Testing, Quality & Delivery — Luís França
Slug: testing-quality-delivery-en
Language: en

##### Approved Content

Testing, quality, and delivery are part of the engineering cycle Luís França uses to transform an implementation into verifiable and operable software. His approach connects acceptance criteria, automated testing, static analysis, structural checks, inspection of changes, execution evidence, and validation before delivery.

In structured projects, tests are derived from expected behavior and applicable specifications rather than being treated only as a stage following implementation. The strategy combines testing appropriate to the risk and responsibility of each component, including behavioral and integration testing, regression testing, and checks focused on boundaries between the application, database, and external integrations.

The Site Portfolio provides concrete evidence of this practice. Throughout its evolution, homepage, contact, administration, Knowledge Base, semantic retrieval, and IA Jujuju capabilities were subjected to automated testing and regression validation. At the Release 2 engineering closure, the complete executed suite contained 577 passing tests, complemented by linting, static type checking, Django configuration checks, migration checks, static-file validation, and diff-integrity checks.

Quality is not treated solely as test execution. Depending on the scope of a change, the process uses tools and checks such as pytest, Ruff, MyPy, Django system checks, and `git diff --check`, together with inspection of repository state and the changes actually produced. The objective is to detect behavioral, integration, typing, configuration, consistency, and regression problems before a change is accepted.

Validation is also separated from implementation whenever that separation increases confidence in the evidence. Changes can be audited through Git and submitted again to quality gates in a validation environment independent of the agent or tool that performed the implementation. The technical result is then combined with human review and acceptance before progressing to the next baseline or to a controlled deployment.

In the Site Portfolio, this process extends through production. Delivery includes preparation and verification of the environment, dependencies, database, migrations, static assets, application services, and proxy, followed by operational validation and smoke testing of the deployed behavior. Critical capabilities are considered complete only according to the level of evidence required for their scope.

This approach does not assume that every project requires the same number of tests, tools, or gates. The level of validation should be proportional to the system's risk, maturity, and responsibilities, preserving correctness and confidence without adding process or infrastructure without demonstrated benefit.

#### Evidence / Maturity Notes

Testing, quality, and delivery are approved professional capabilities. The Site Portfolio provides implementation, validation, quality-gate, and production-delivery evidence; maturity must remain proportional to the evidence available for each specific claim.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-SKL-004 — AI, LLM & RAG Engineering

#### Metadata

Category: SKILL
Editorial Status: APPROVED
Editorial Version: 1.0

#### PT-BR

Title: Engenharia de IA, LLM e RAG — Luís França
Slug: ai-llm-rag-engineering-pt-br
Language: pt-br

##### Approved Content

Luís França possui experiência prática na integração de Inteligência Artificial e Large Language Models (LLMs) a aplicações de software, com foco na construção de funcionalidades controladas, rastreáveis e integradas à arquitetura da aplicação. Sua experiência demonstrada inclui integração com providers de IA, Retrieval-Augmented Generation (RAG), embeddings, recuperação vetorial, construção de contexto, persistência de conversações e rastreabilidade das fontes utilizadas para gerar respostas.

O Site Portfólio fornece a principal evidência atual dessa capacidade por meio da IA Jujuju, uma assistente virtual integrada à aplicação Django. A Jujuju utiliza uma Knowledge Base curada para recuperar informações relevantes antes da geração da resposta, permitindo que afirmações factuais sobre o portfólio sejam fundamentadas no conhecimento aprovado em vez de depender apenas do conhecimento geral do modelo.

O pipeline de RAG implementado começa com documentos de conhecimento administrados pela aplicação. O conteúdo é normalizado e dividido de forma determinística em chunks semanticamente adequados. Esses chunks são transformados em embeddings e armazenados no PostgreSQL utilizando pgvector. Durante uma consulta, a aplicação gera o embedding da pergunta, executa recuperação semântica por similaridade vetorial e utiliza os resultados relevantes para construir o contexto enviado ao LLM.

A implementação utiliza PostgreSQL tanto para os dados relacionais quanto para a persistência vetorial. A recuperação utiliza distância cosseno e aplica o idioma como filtro obrigatório, com categoria disponível como filtro adicional. Essa decisão mantém a solução proporcional à escala e aos requisitos do produto e evita introduzir um banco vetorial dedicado sem necessidade demonstrada.

A integração com serviços de IA é isolada por abstrações de provider, reduzindo o acoplamento entre a lógica da aplicação e um fornecedor externo específico. Na implementação atual, embeddings e geração utilizam serviços da OpenAI. O pipeline valida propriedades relevantes das respostas externas, trata falhas do provider e preserva as fronteiras entre chamadas externas e operações transacionais da aplicação.

A IA Jujuju também mantém conversações e evidências das fontes recuperadas. O objetivo não é operar como um agente autônomo de propósito geral, mas como uma assistente especializada no portfólio profissional de Luís. Quando o conhecimento recuperado não oferece suporte suficiente para uma afirmação factual, o comportamento esperado é reconhecer essa insuficiência em vez de fabricar informação.

Essa capacidade foi além da especificação arquitetural: o pipeline de Knowledge Base, embeddings, recuperação vetorial e geração de respostas foi implementado e submetido a testes automatizados. Em produção, o fluxo foi validado com serviços reais de embeddings e LLM, incluindo indexação de conhecimento, recuperação semântica e uma resposta da IA Jujuju fundamentada no conteúdo recuperado.

Outros projetos do portfólio possuem níveis diferentes de maturidade em Inteligência Artificial. Capacidades de Machine Learning e IA presentes no roadmap da Intelligent Currency Platform permanecem planejadas e não são utilizadas como evidência de implementação. A experiência prática descrita neste documento é sustentada principalmente pelas capacidades efetivamente implementadas e validadas no Site Portfólio.

#### EN

Title: AI, LLM & RAG Engineering — Luís França
Slug: ai-llm-rag-engineering-en
Language: en

##### Approved Content

Luís França has practical experience integrating Artificial Intelligence and Large Language Models (LLMs) into software applications, with a focus on building controlled, traceable capabilities integrated with the application's architecture. His demonstrated experience includes AI provider integration, Retrieval-Augmented Generation (RAG), embeddings, vector retrieval, context construction, conversation persistence, and traceability of the sources used to generate responses.

The Site Portfolio provides the primary current evidence of this capability through IA Jujuju, a virtual assistant integrated with the Django application. Jujuju uses a curated Knowledge Base to retrieve relevant information before response generation, allowing factual claims about the portfolio to be grounded in approved knowledge rather than relying solely on the model's general knowledge.

The implemented RAG pipeline begins with knowledge documents managed by the application. Content is normalized and deterministically divided into semantically appropriate chunks. These chunks are transformed into embeddings and stored in PostgreSQL using pgvector. During a query, the application generates an embedding for the question, performs semantic retrieval through vector similarity, and uses the relevant results to construct the context provided to the LLM.

The implementation uses PostgreSQL for both relational data and vector persistence. Retrieval uses cosine distance and applies language as a mandatory filter, with category available as an additional filter. This decision keeps the solution proportional to the product's scale and requirements and avoids introducing a dedicated vector database without a demonstrated need.

Integration with AI services is isolated through provider abstractions, reducing coupling between application logic and a specific external vendor. In the current implementation, embedding and generation capabilities use OpenAI services. The pipeline validates relevant properties of external responses, handles provider failures, and preserves boundaries between external calls and the application's transactional operations.

IA Jujuju also maintains conversations and evidence of retrieved sources. Its purpose is not to operate as a general-purpose autonomous agent but as an assistant specialized in Luís's professional portfolio. When retrieved knowledge does not provide sufficient support for a factual claim, the expected behavior is to acknowledge that insufficiency rather than fabricate information.

This capability progressed beyond architectural specification: the Knowledge Base, embedding, vector retrieval, and response-generation pipeline was implemented and subjected to automated testing. In production, the flow was validated with real embedding and LLM services, including knowledge indexing, semantic retrieval, and an IA Jujuju response grounded in retrieved content.

Other portfolio projects have different levels of Artificial Intelligence maturity. Machine Learning and AI capabilities included in the Intelligent Currency Platform roadmap remain planned and are not used as evidence of implementation. The practical experience described in this document is supported primarily by capabilities actually implemented and validated in the Site Portfolio.

#### Evidence / Maturity Notes

AI, LLM, and RAG engineering are supported by implemented, validated, and production evidence in the Site Portfolio. Planned AI or Machine Learning capabilities in other projects must not be represented as implemented or production capabilities.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

## 5. Wave 2 — Flagship Case

Wave 2 contains 6 Knowledge Concepts and 12 KnowledgeDocument variants.

Category for all Wave 2 concepts: PROJECT

All Wave 2 KnowledgeDocument variants have Review Status: APPROVED.

### KB-PRJ-001 — Site Portfólio — Product Overview

#### Metadata

Concept ID: KB-PRJ-001
Category: PROJECT
Editorial Version: v1.0

#### PT-BR

Title: Site Portfólio — Product Overview
Slug: site-portfolio-product-overview-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

O Site Portfólio é uma plataforma digital profissional desenvolvida por Luís França para apresentar seu perfil, experiência, competências, projetos e práticas de Engenharia de Software. Mais do que uma página de apresentação, o projeto foi concebido para que o próprio produto também funcione como evidência do processo de engenharia empregado em sua construção e evolução.

O sistema foi desenvolvido como uma aplicação web baseada em Django e PostgreSQL, utilizando renderização server-side com Django Templates, HTML, CSS e JavaScript de forma proporcional às necessidades do produto. Sua arquitetura segue um monólito modular, preservando separação de responsabilidades sem introduzir a complexidade operacional de uma arquitetura distribuída sem necessidade comprovada.

O produto oferece conteúdo profissional bilíngue em português brasileiro e inglês, apresentação de projetos e competências, canais de contato e comunicação, administração baseada no Django Admin e uma base de conhecimento utilizada pela IA Jujuju.

A IA Jujuju é a assistente virtual integrada ao portfólio. Ela utiliza Retrieval-Augmented Generation (RAG) para recuperar conteúdo autorizado da base de conhecimento antes da geração das respostas. O pipeline utiliza embeddings, armazenamento vetorial no PostgreSQL por meio do pgvector, recuperação semântica com filtros controlados e integração com modelos da OpenAI por abstrações de provider.

O desenvolvimento do Site Portfólio foi conduzido de forma orientada por especificações. Requisitos, decisões arquiteturais, contratos, critérios de teste, implantação e evolução foram documentados e relacionados à implementação e às evidências de validação. O projeto também passou por ciclos de refinamento responsivo, UX/UI, validação visual e preparação operacional para produção.

O Site Portfólio está implantado em infraestrutura de produção e suas principais capacidades de aplicação, incluindo o backend Django, PostgreSQL e o pipeline de Knowledge Base, recuperação vetorial e IA Jujuju, possuem evidência de execução e validação em produção. O processo de fechamento operacional global da evolução atual permanece sujeito aos gates finais definidos para o projeto.

#### EN

Title: Site Portfolio — Product Overview
Slug: site-portfolio-product-overview-en
Language: en
Review Status: APPROVED

##### Approved Content

Site Portfolio is a professional digital platform developed by Luís França to present his profile, experience, capabilities, projects, and Software Engineering practices. More than a presentation website, the project was conceived so that the product itself could also serve as evidence of the engineering process applied throughout its construction and evolution.

The system was developed as a web application based on Django and PostgreSQL, using server-side rendering with Django Templates, HTML, CSS, and JavaScript proportionally to the product's actual needs. Its architecture follows a modular monolith approach, preserving separation of responsibilities without introducing the operational complexity of a distributed architecture where no demonstrated need exists.

The product provides bilingual professional content in Brazilian Portuguese and English, presentation of projects and capabilities, contact and communication channels, administration based on Django Admin, and a knowledge base used by IA Jujuju.

IA Jujuju is the virtual assistant integrated into the portfolio. It uses Retrieval-Augmented Generation (RAG) to retrieve authorized content from the knowledge base before generating responses. The pipeline uses embeddings, vector storage in PostgreSQL through pgvector, semantic retrieval with controlled filters, and integration with OpenAI models through provider abstractions.

Site Portfolio development was conducted through a specification-driven process. Requirements, architectural decisions, contracts, testing criteria, deployment, and evolution were documented and related to implementation and validation evidence. The project also underwent responsive, UX/UI, visual validation, and production-readiness refinement cycles.

Site Portfolio is deployed on production infrastructure, and its principal application capabilities, including the Django backend, PostgreSQL, and the Knowledge Base, vector retrieval, and IA Jujuju pipeline, have evidence of production execution and validation. The overall operational closure of the current evolution remains subject to the project's remaining final gates.

#### Evidence / Maturity Notes

O Site Portfólio possui evidência de especificação, implementação, validação e operação em produção. Claims individuais devem preservar sua temporalidade: funcionalidades ou etapas que ainda estejam em processo de fechamento não devem ser descritas como formalmente encerradas apenas porque outras capacidades do sistema já possuem evidência de produção.

Site Portfolio is supported by specification, implementation, validation, and production-operation evidence. Individual claims must preserve their temporal context: features or stages still undergoing closure must not be described as formally closed merely because other system capabilities already have production evidence.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-002 — Site Portfólio — Legacy Modernization

#### Metadata

Concept ID: KB-PRJ-002
Category: PROJECT
Editorial Version: v1.0

#### PT-BR

Title: Site Portfólio — Legacy Modernization
Slug: site-portfolio-legacy-modernization-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

O Site Portfólio representa a modernização de uma presença profissional anterior para um produto de software estruturado por práticas contemporâneas de Engenharia de Software. Em vez de tratar a evolução como uma simples atualização visual do site legado, o projeto utilizou a oportunidade para reavaliar requisitos, arquitetura, experiência do usuário, responsividade, qualidade, segurança, operação e capacidade de evolução.

A modernização foi conduzida progressivamente. O produto passou por uma fundação inicial, implementação das capacidades essenciais e ciclos posteriores de maturidade da plataforma. Esse processo permitiu preservar comportamentos e objetivos relevantes enquanto decisões antigas eram reavaliadas com base nos requisitos atuais.

A evolução da interface também foi tratada como um problema de engenharia. O projeto estabeleceu referências de design e implementou requisitos responsivos verificáveis, considerando diferentes larguras de viewport e comportamentos específicos de componentes. O repositório preserva especificações responsivas, medições de geometria, evidências de fit, screenshots de validação, regressões visuais e rastreabilidade entre referências de design e comportamento observado no navegador.

Figma foi utilizado como autoridade de design integrada a partes desse ciclo por meio de MCP com Codex. Composições e propriedades aprovadas foram comparadas com a implementação, e evidências de geometria e rastreabilidade foram produzidas para apoiar refinamentos responsivos e visuais. A automação e as evidências técnicas complementaram, mas não substituíram, a revisão visual e o aceite humano.

O trabalho incluiu refinamentos em elementos como composição da homepage, comportamento responsivo, header, footer, áreas de conteúdo, imagens, backgrounds e integração visual da IA Jujuju. Correções foram verificadas contra viewports de referência e, quando aplicável, contra limites de transição para reduzir regressões entre tamanhos de tela.

A modernização resultou em uma plataforma que combina apresentação profissional com backend, persistência, administração, testes, documentação, operação e capacidades de IA/RAG. Dessa forma, o projeto demonstra uma evolução de produto baseada em reavaliação arquitetural e validação incremental, e não apenas uma substituição estética do sistema anterior.

#### EN

Title: Site Portfolio — Legacy Modernization
Slug: site-portfolio-legacy-modernization-en
Language: en
Review Status: APPROVED

##### Approved Content

Site Portfolio represents the modernization of a previous professional web presence into a software product structured through contemporary Software Engineering practices. Rather than treating the evolution as a simple visual update of the legacy website, the project used the opportunity to reassess requirements, architecture, user experience, responsiveness, quality, security, operations, and evolvability.

Modernization was conducted progressively. The product went through an initial foundation, implementation of essential capabilities, and subsequent platform-maturity cycles. This process made it possible to preserve relevant behaviors and objectives while reassessing previous decisions against current requirements.

Interface evolution was also treated as an engineering problem. The project established design references and implemented verifiable responsive requirements, considering different viewport widths and component-specific behaviors. The repository preserves responsive specifications, geometry measurements, fit evidence, validation screenshots, visual regression evidence, and traceability between design references and behavior observed in the browser.

Figma was used as a design authority integrated into parts of this cycle through MCP with Codex. Approved compositions and properties were compared with the implementation, and geometry and traceability evidence was produced to support responsive and visual refinements. Automation and technical evidence complemented, but did not replace, human visual review and acceptance.

The work included refinements to elements such as homepage composition, responsive behavior, header, footer, content areas, images, backgrounds, and the visual integration of IA Jujuju. Corrections were verified against reference viewports and, where applicable, transition boundaries to reduce regressions across screen sizes.

Modernization resulted in a platform that combines professional presentation with backend engineering, persistence, administration, testing, documentation, operations, and AI/RAG capabilities. The project therefore demonstrates product evolution based on architectural reassessment and incremental validation rather than merely an aesthetic replacement of the previous system.

#### Evidence / Maturity Notes

A modernização do Site Portfólio é suportada por especificações, implementação, artefatos de validação responsiva e visual e evidência de produção. O uso de Figma integrado por MCP com Codex faz parte do processo efetivamente executado e aprovado pelo Product Owner; a documentação do repositório preserva ampla evidência de Figma e validação, mas não consolidou adequadamente a identificação nominal dessa integração, constituindo uma lacuna documental reconhecida. O site legado deve permanecer caracterizado segundo sua maturidade histórica, sem atribuição retroativa das práticas de engenharia adotadas na plataforma atual.

Site Portfolio modernization is supported by specifications, implementation, responsive and visual validation artifacts, and production evidence. The use of Figma integrated through MCP with Codex is part of the process actually executed and approved by the Product Owner; the repository preserves extensive Figma and validation evidence but did not adequately consolidate the nominal identification of this integration, which is a recognized documentation gap. The legacy website must remain characterized according to its historical maturity without retroactively attributing the engineering practices adopted in the current platform.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-003 — Site Portfólio — Architecture

#### Metadata

Concept ID: KB-PRJ-003
Category: PROJECT
Editorial Version: v1.0

#### PT-BR

Title: Site Portfólio — Architecture
Slug: site-portfolio-architecture-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

A arquitetura do Site Portfólio foi projetada para equilibrar simplicidade, separação de responsabilidades, testabilidade, segurança, implantação e evolução. A solução adota Django como framework principal e uma arquitetura de monólito modular, evitando a introdução prematura de microserviços ou infraestrutura distribuída.

A aplicação utiliza Django 5.2 sobre Python 3.13, Django Templates para renderização server-side e PostgreSQL como banco de dados relacional. HTML e CSS constituem a base da apresentação, com JavaScript utilizado de forma limitada e orientada às necessidades de interação. O ambiente Python e suas dependências são gerenciados de forma reproduzível com `uv`.

As responsabilidades são separadas por módulos funcionais da aplicação. Capacidades como contato, administração, Knowledge Base e IA possuem seus próprios modelos, serviços, integrações e testes quando essa separação é necessária. Dependências externas são isoladas por abstrações, permitindo que testes utilizem providers controlados sem depender de chamadas reais a serviços externos.

Para a Knowledge Base, o PostgreSQL foi estendido com pgvector em vez da introdução de um banco vetorial dedicado. Documentos autorizados são normalizados, divididos deterministicamente em chunks e convertidos em embeddings. Os vetores possuem 1024 dimensões e são pesquisados por similaridade cosseno. Para a escala atual do produto, a recuperação utiliza busca vetorial exata, sem índice ANN.

A arquitetura da IA Jujuju reutiliza essa camada de recuperação. Uma consulta é processada pelo serviço da aplicação, submetida à recuperação semântica com idioma obrigatório e filtros controlados quando aplicáveis, convertida em contexto e enviada ao modelo de geração através de uma abstração de provider. Conversas, mensagens e evidências das fontes recuperadas são persistidas para garantir rastreabilidade.

Na produção, a aplicação utiliza Nginx como reverse proxy e servidor de arquivos estáticos, Gunicorn como servidor WSGI, Django como aplicação e PostgreSQL como camada de persistência. O processo da aplicação é gerenciado pelo systemd, e configuração sensível é fornecida pelo ambiente em vez de incorporada ao código.

Essa arquitetura é deliberadamente proporcional ao produto. Tecnologias adicionais são introduzidas somente quando resolvem uma necessidade comprovada, preservando menor complexidade operacional e mantendo o sistema compreensível, testável e evolutivo.

#### EN

Title: Site Portfolio — Architecture
Slug: site-portfolio-architecture-en
Language: en
Review Status: APPROVED

##### Approved Content

Site Portfolio architecture was designed to balance simplicity, separation of responsibilities, testability, security, deployment, and evolution. The solution uses Django as its primary framework and follows a modular monolith architecture, avoiding premature introduction of microservices or distributed infrastructure.

The application uses Django 5.2 on Python 3.13, Django Templates for server-side rendering, and PostgreSQL as its relational database. HTML and CSS form the presentation foundation, with JavaScript used in a limited manner according to interaction requirements. The Python environment and dependencies are managed reproducibly with `uv`.

Responsibilities are separated across functional application modules. Capabilities such as contact, administration, Knowledge Base, and AI have their own models, services, integrations, and tests where such separation is required. External dependencies are isolated through abstractions, allowing tests to use controlled providers without relying on real calls to external services.

For the Knowledge Base, PostgreSQL was extended with pgvector rather than introducing a dedicated vector database. Authorized documents are normalized, deterministically divided into chunks, and converted into embeddings. Vectors have 1024 dimensions and are searched using cosine similarity. At the product's current scale, retrieval uses exact vector search without an ANN index.

IA Jujuju's architecture reuses this retrieval layer. A query is processed by the application service, submitted to semantic retrieval with a mandatory language constraint and controlled filters where applicable, transformed into context, and sent to the generation model through a provider abstraction. Conversations, messages, and retrieved source evidence are persisted to provide traceability.

In production, the application uses Nginx as a reverse proxy and static-file server, Gunicorn as its WSGI server, Django as the application layer, and PostgreSQL as the persistence layer. The application process is managed by systemd, and sensitive configuration is supplied through the environment rather than embedded in source code.

The architecture is deliberately proportional to the product. Additional technologies are introduced only when they address a demonstrated requirement, preserving lower operational complexity while keeping the system understandable, testable, and evolvable.

#### Evidence / Maturity Notes

A arquitetura descrita possui evidência em documentos arquiteturais, ADRs, especificações, implementação, testes e ambiente de produção. Decisões deliberadamente não adotadas — como microserviços, banco vetorial dedicado e ANN na escala atual — devem ser tratadas como trade-offs arquiteturais, e não como capacidades ausentes por acidente.

The described architecture is supported by architecture documentation, ADRs, specifications, implementation, tests, and the production environment. Deliberately unadopted approaches—such as microservices, a dedicated vector database, and ANN at the current scale—must be understood as architectural trade-offs rather than accidentally missing capabilities.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-004 — Site Portfólio — Release Evolution

#### Metadata

Concept ID: KB-PRJ-004
Category: PROJECT
Editorial Version: v1.0

#### PT-BR

Title: Site Portfólio — Release Evolution
Slug: site-portfolio-release-evolution-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

A evolução do Site Portfólio foi organizada em releases para que cada incremento tivesse escopo, decisões, critérios de aceite, implementação e validação identificáveis. Essa estratégia permitiu evoluir o produto sem misturar indiscriminadamente fundação, refinamento da experiência e capacidades avançadas.

O Release 1 estabeleceu a fundação do produto. Ele consolidou a homepage profissional, apresentação de competências e projetos, navegação, internacionalização, contato e comunicação, responsividade, persistência necessária ao produto e a base operacional da aplicação. O ciclo foi submetido a testes e validação antes de seu fechamento.

Após essa fundação, o Release 1.1 foi utilizado para elevar a maturidade da plataforma. O ciclo incorporou análise de gaps e refinamentos de UX/UI, design e responsividade, além de trabalho relacionado a analytics, SEO, performance e validação conforme o escopo definido para essa evolução. A homepage passou por um processo particularmente detalhado de especificação responsiva, comparação de geometria, validação visual e refinamentos incrementais em múltiplos viewports.

Nesse processo, referências de Figma foram integradas às atividades de design e validação por meio de MCP com Codex. A implementação foi comparada com composições aprovadas e submetida a medições, screenshots, verificações de fit, sweeps de largura e revisão humana. Os artefatos preservados no repositório permitem rastrear parte dessa evolução entre design, implementação e evidência.

O Release 2 expandiu o produto para capacidades de administração, Knowledge Base e Inteligência Artificial. Django Admin passou a fornecer administração controlada; a Knowledge Base introduziu documentos, chunks, embeddings e recuperação vetorial; e a IA Jujuju passou a utilizar esse conhecimento através de um pipeline RAG com rastreabilidade das fontes.

A engenharia e documentação do Release 2 foram formalmente encerradas em sua baseline correspondente. Posteriormente, a implantação e validação operacional confirmaram em produção capacidades centrais da Knowledge Base, recuperação semântica e IA Jujuju. Refinamentos corretivos também foram aplicados durante o ciclo de produção.

A evolução por releases demonstra uma estratégia incremental: primeiro estabelecer uma fundação funcional, depois amadurecer experiência e qualidade e, somente então, introduzir administração, conhecimento estruturado e IA. Cada etapa preserva sua própria autoridade temporal e nível de maturidade.

#### EN

Title: Site Portfolio — Release Evolution
Slug: site-portfolio-release-evolution-en
Language: en
Review Status: APPROVED

##### Approved Content

Site Portfolio evolution was organized into releases so that each increment had identifiable scope, decisions, acceptance criteria, implementation, and validation. This strategy allowed the product to evolve without indiscriminately mixing foundation work, experience refinement, and advanced capabilities.

Release 1 established the product foundation. It consolidated the professional homepage, presentation of capabilities and projects, navigation, internationalization, contact and communication, responsiveness, the persistence required by the product, and the application's operational foundation. The cycle underwent testing and validation before closure.

Following that foundation, Release 1.1 was used to increase platform maturity. The cycle incorporated gap analysis and UX/UI, design, and responsive refinements, as well as work related to analytics, SEO, performance, and validation according to the scope defined for this evolution. The homepage underwent a particularly detailed process of responsive specification, geometry comparison, visual validation, and incremental refinement across multiple viewports.

During this process, Figma references were integrated into design and validation activities through MCP with Codex. The implementation was compared with approved compositions and subjected to measurements, screenshots, fit checks, width sweeps, and human review. Artifacts preserved in the repository make part of this evolution traceable across design, implementation, and evidence.

Release 2 expanded the product with administration, Knowledge Base, and Artificial Intelligence capabilities. Django Admin provided controlled administration; the Knowledge Base introduced documents, chunks, embeddings, and vector retrieval; and IA Jujuju began using this knowledge through a RAG pipeline with source traceability.

Release 2 engineering and documentation were formally closed in their corresponding baseline. Subsequently, deployment and operational validation confirmed central Knowledge Base, semantic retrieval, and IA Jujuju capabilities in production. Corrective refinements were also applied during the production cycle.

The release evolution demonstrates an incremental strategy: first establish a functional foundation, then mature experience and quality, and only then introduce administration, structured knowledge, and AI. Each stage preserves its own temporal authority and maturity level.

#### Evidence / Maturity Notes

A evolução por releases possui documentação histórica e evidência técnica. O uso de Figma por MCP com Codex no ciclo responsivo é um fato aprovado do processo executado, embora sua identificação nominal não tenha sido adequadamente consolidada na documentação contemporânea. Release 1 e Release 1.1 devem ser descritos segundo seus respectivos fechamentos. Para Release 2, o fechamento de engenharia e documentação e a posterior evidência de produção devem ser distinguidos temporalmente do fechamento operacional global, que não deve ser antecipado enquanto seus gates finais permanecerem abertos.

Release evolution is supported by historical documentation and technical evidence. The use of Figma through MCP with Codex during the responsive cycle is an approved fact of the executed process, although its nominal identification was not adequately consolidated in the contemporaneous documentation. Releases 1 and 1.1 must be described according to their respective closure states. For Release 2, engineering and documentation closure and subsequent production evidence must be temporally distinguished from overall operational closure, which must not be anticipated while final gates remain open.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-005 — Site Portfólio — IA Jujuju

#### Metadata

Concept ID: KB-PRJ-005
Category: PROJECT
Editorial Version: v1.0

#### PT-BR

Title: Site Portfólio — IA Jujuju
Slug: site-portfolio-ia-jujuju-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

A IA Jujuju é a assistente virtual do portfólio profissional de Luís França. Sua função é permitir que visitantes consultem informações autorizadas sobre o perfil profissional, competências, experiência, projetos e práticas de engenharia apresentadas pelo portfólio.

A solução utiliza Retrieval-Augmented Generation (RAG). Em vez de depender exclusivamente do conhecimento geral do modelo de linguagem, a aplicação recupera conteúdo da Knowledge Base do próprio portfólio e utiliza os resultados relevantes como contexto controlado para geração da resposta.

A Knowledge Base é armazenada no PostgreSQL. Documentos são normalizados e divididos deterministicamente em chunks; embeddings são produzidos por uma integração com a OpenAI e armazenados com pgvector. A recuperação utiliza similaridade vetorial por cosseno, idioma obrigatório e filtros de categoria quando aplicáveis. A configuração atual utiliza embeddings de 1024 dimensões e recuperação exata com `top_k` padrão igual a cinco.

A camada da IA Jujuju possui abstração própria para o provider de geração. A integração de produção utiliza a OpenAI Responses API, enquanto os testes podem substituir dependências externas por providers controlados. Essa separação reduz acoplamento e permite validar a lógica da aplicação sem exigir chamadas reais aos serviços externos durante a suíte automatizada.

O contexto enviado ao modelo é construído a partir do conteúdo recuperado. O desenho inclui controles destinados a reduzir fabricação de respostas e interferência de instruções presentes nas fontes. A aplicação também mantém rastreabilidade entre conversas, mensagens e evidências recuperadas, permitindo relacionar uma resposta ao conhecimento utilizado em sua geração.

As conversas são associadas à sessão anônima do visitante e persistidas para finalidade operacional e de rastreabilidade. O projeto define retenção configurável, atualmente estabelecida em 90 dias, e disponibiliza administração orientada à consulta desses registros.

O pipeline completo foi implementado e validado. Em produção, foram verificadas a geração real de embeddings, a persistência de vetores no PostgreSQL/pgvector, a recuperação semântica e uma consulta end-to-end da IA Jujuju utilizando o mesmo caminho de aplicação empregado pelo produto.

A IA Jujuju, portanto, não é apresentada como uma IA generalista nem como uma fonte independente de verdade. Sua função no produto é fornecer uma interface conversacional sobre uma base de conhecimento governada, recuperável e rastreável.

#### EN

Title: Site Portfolio — IA Jujuju
Slug: site-portfolio-ia-jujuju-en
Language: en
Review Status: APPROVED

##### Approved Content

IA Jujuju is the virtual assistant for Luís França's professional portfolio. Its purpose is to allow visitors to query authorized information about the professional profile, capabilities, experience, projects, and engineering practices presented by the portfolio.

The solution uses Retrieval-Augmented Generation (RAG). Rather than relying exclusively on the language model's general knowledge, the application retrieves content from the portfolio's own Knowledge Base and uses relevant results as controlled context for response generation.

The Knowledge Base is stored in PostgreSQL. Documents are normalized and deterministically divided into chunks; embeddings are produced through an OpenAI integration and stored with pgvector. Retrieval uses cosine vector similarity, a mandatory language constraint, and category filters where applicable. The current configuration uses 1024-dimensional embeddings and exact retrieval with a default `top_k` of five.

The IA Jujuju layer has its own abstraction for the generation provider. The production integration uses the OpenAI Responses API, while tests can replace external dependencies with controlled providers. This separation reduces coupling and allows application logic to be validated without requiring real external-service calls during the automated test suite.

The context sent to the model is built from retrieved content. The design includes controls intended to reduce fabricated answers and interference from instructions contained in sources. The application also maintains traceability among conversations, messages, and retrieved evidence, allowing a response to be related to the knowledge used in its generation.

Conversations are associated with the visitor's anonymous session and persisted for operational and traceability purposes. The project defines configurable retention, currently set to 90 days, and provides read-oriented administration for these records.

The complete pipeline has been implemented and validated. In production, real embedding generation, vector persistence in PostgreSQL/pgvector, semantic retrieval, and an end-to-end IA Jujuju query using the same application path employed by the product were verified.

IA Jujuju is therefore not presented as a general-purpose AI or as an independent source of truth. Its role in the product is to provide a conversational interface over a governed, retrievable, and traceable knowledge base.

#### Evidence / Maturity Notes

Knowledge Base, embeddings, recuperação vetorial, persistência de conversação e integração RAG da IA Jujuju possuem evidência de implementação, validação e execução em produção. O conteúdo que a assistente pode afirmar permanece condicionado à autoridade e maturidade dos documentos efetivamente aprovados e indexados na Knowledge Base.

The Knowledge Base, embeddings, vector retrieval, conversation persistence, and IA Jujuju RAG integration have implementation, validation, and production-execution evidence. What the assistant may assert remains constrained by the authority and maturity of the documents actually approved and indexed in the Knowledge Base.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-006 — Site Portfólio — Production Delivery

#### Metadata

Concept ID: KB-PRJ-006
Category: PROJECT
Editorial Version: v1.0

#### PT-BR

Title: Site Portfólio — Production Delivery
Slug: site-portfolio-production-delivery-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

A entrega em produção do Site Portfólio foi tratada como uma etapa de engenharia separada da conclusão do código. O processo considera configuração, persistência, runtime da aplicação, reverse proxy, arquivos estáticos, segurança, recuperação, validação operacional e evidência antes do fechamento definitivo da implantação.

A arquitetura de produção utiliza uma instância de computação OCI executando Linux. Nginx recebe as requisições públicas e atua como reverse proxy para Gunicorn, que executa a aplicação Django por WSGI. PostgreSQL fornece a persistência relacional e também suporta a recuperação vetorial através da extensão pgvector.

Gunicorn é gerenciado pelo systemd e executa a aplicação em uma interface local, evitando exposição direta do servidor de aplicação. Nginx também é responsável pelo atendimento dos arquivos estáticos. A configuração de produção do Django utiliza variáveis de ambiente para valores dependentes do ambiente e dados sensíveis.

O deployment utiliza ambiente Python controlado e dependências bloqueadas. Antes da ativação de alterações, o processo considera operações como sincronização do código, dependências, migrações quando necessárias, coleta de arquivos estáticos e validações da aplicação.

A estratégia operacional inclui preparação para recuperação. O projeto possui runbook específico e, durante a implantação do Release 2, foi criado um recovery point contendo evidências necessárias para restauração do estado anterior, incluindo backup do banco e configurações operacionais relevantes. O procedimento de restauração foi testado antes da progressão da implantação.

A evolução do Release 2 também exigiu validação das dependências do pipeline RAG no ambiente real. PostgreSQL e pgvector foram verificados no servidor, incluindo suporte à dimensão vetorial utilizada pelo produto. Posteriormente, embeddings reais foram gerados, documentos foram indexados, recuperação semântica foi executada e a IA Jujuju respondeu por seu caminho end-to-end de produção.

A implantação também foi acompanhada por correções controladas identificadas durante a validação pública, incluindo refinamentos de posicionamento, localização e nomenclatura da IA Jujuju, configuração de links públicos e alinhamento visual do header. Essas correções foram submetidas a controle de versão e validação conforme sua natureza.

Segurança operacional foi tratada como parte do processo de produção. Credenciais expostas durante uma etapa operacional foram rotacionadas, os acessos afetados foram corrigidos e artefatos temporários contendo informações sensíveis foram removidos. Segredos não são mantidos no código-fonte e o arquivo de ambiente de produção permanece protegido por permissões restritas.

A implantação já possui evidência operacional significativa, inclusive para Django, PostgreSQL, pgvector e IA Jujuju. Entretanto, o fechamento global da implantação do Release 2 permanece condicionado aos gates ainda abertos, incluindo a conclusão controlada da população da Knowledge Base, solução estrutural para cache busting de arquivos estáticos e certificação final de produção.

#### EN

Title: Site Portfolio — Production Delivery
Slug: site-portfolio-production-delivery-en
Language: en
Review Status: APPROVED

##### Approved Content

Site Portfolio production delivery was treated as an engineering stage distinct from code completion. The process considers configuration, persistence, application runtime, reverse proxy, static files, security, recovery, operational validation, and evidence before final deployment closure.

The production architecture uses an OCI compute instance running Linux. Nginx receives public requests and acts as a reverse proxy to Gunicorn, which runs the Django application through WSGI. PostgreSQL provides relational persistence and also supports vector retrieval through the pgvector extension.

Gunicorn is managed by systemd and runs the application on a local interface, preventing direct exposure of the application server. Nginx is also responsible for serving static files. Django production configuration uses environment variables for environment-dependent values and sensitive data.

Deployment uses a controlled Python environment and locked dependencies. Before activating changes, the process considers operations such as code synchronization, dependency installation, migrations where required, static-file collection, and application validation.

The operational strategy includes recovery preparation. The project has a dedicated runbook, and during Release 2 deployment a recovery point was created containing the evidence required to restore the previous state, including a database backup and relevant operational configuration. The restoration procedure was tested before deployment progressed.

Release 2 evolution also required validation of RAG pipeline dependencies in the actual environment. PostgreSQL and pgvector were verified on the server, including support for the vector dimensionality used by the product. Subsequently, real embeddings were generated, documents were indexed, semantic retrieval was executed, and IA Jujuju responded through its end-to-end production path.

Deployment was also accompanied by controlled corrections identified during public validation, including refinements to IA Jujuju positioning, localization and naming, public-link configuration, and visual header alignment. These corrections were subjected to version control and validation according to their nature.

Operational security was treated as part of the production process. Credentials exposed during an operational step were rotated, affected access was corrected, and temporary artifacts containing sensitive information were removed. Secrets are not stored in source code, and the production environment file remains protected by restrictive permissions.

Deployment already has significant operational evidence, including Django, PostgreSQL, pgvector, and IA Jujuju. However, overall Release 2 production-deployment closure remains conditional on the gates that are still open, including controlled completion of Knowledge Base population, a structural static-file cache-busting solution, and final production certification.

#### Evidence / Maturity Notes

A entrega do Site Portfólio possui evidência real de operação em produção e validação de componentes centrais. Isso permite classificar claims específicas comprovadas como production-demonstrated. Não permite antecipar o status administrativo de `Release 2 Production Deployment: CLOSED` enquanto os gates finais definidos pelo projeto permanecerem abertos.

Site Portfolio delivery has real production-operation evidence and validation of central components. This allows specifically proven claims to be classified as production-demonstrated. It does not allow the administrative status `Release 2 Production Deployment: CLOSED` to be anticipated while the project's defined final gates remain open.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

## 6. Wave 3 — Engineering Process

Wave 3 contains 9 Knowledge Concepts and 18 KnowledgeDocument variants.

Wave 3 uses categories:

- PROCESS
- ENGINEERING

All Wave 3 KnowledgeDocument variants are Human Approved.

PCS-002 additionally remains:

- APPROVED — DOCUMENTARY CONSOLIDATION REQUIRED

### KB-PCS-001 — Specification-Driven Development na Engenharia de Software

#### Metadata

Concept ID: PCS-001
Category: PROCESS
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Specification-Driven Development na Engenharia de Software
Slug: specification-driven-development-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís utiliza Specification-Driven Development (SDD) como processo estruturante para transformar requisitos em decisões técnicas, especificações implementáveis, software verificável e evidências de aceitação. Nesse modelo, a implementação não é tratada como ponto inicial isolado: ela deriva de requisitos e decisões previamente compreendidos e registrados em nível proporcional à complexidade e ao risco da mudança.

O processo estabelece uma cadeia de rastreabilidade entre requisitos, decisões, especificações, implementação, testes, evidências e aceite. Product briefs, especificações técnicas, documentos de arquitetura, ADRs, contratos, critérios de aceitação, planos de implantação e registros de validação podem exercer papéis distintos nessa cadeia. A documentação não é utilizada apenas como descrição posterior do código; ela participa do controle da engenharia e da definição do comportamento esperado antes e durante a implementação.

No Site Portfólio, essa abordagem foi aplicada desde a fundação arquitetural até evoluções posteriores do produto. Decisões sobre arquitetura, backend, persistência, integração de e-mail, runtime de produção, Knowledge Base, recuperação vetorial e IA Jujuju foram formalizadas e relacionadas à implementação e à validação correspondente. O mesmo princípio foi aplicado ao trabalho responsivo e visual, no qual requisitos aprovados foram convertidos em critérios determinísticos e verificáveis.

O processo também preserva a separação entre implementação, verificação técnica e aceite humano. A existência de código ou a passagem de um teste automatizado não substitui automaticamente a aprovação do resultado quando a decisão exige avaliação humana, visual ou de produto.

Essa experiência demonstra o uso de SDD não apenas como prática documental, mas como mecanismo de governança técnica para reduzir ambiguidade, controlar mudanças, preservar decisões e permitir evolução rastreável do software.

#### EN

Title: Specification-Driven Software Engineering
Slug: specification-driven-development-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís uses Specification-Driven Development (SDD) as a structuring process for transforming requirements into technical decisions, implementable specifications, verifiable software, and acceptance evidence. In this model, implementation is not treated as an isolated starting point: it derives from requirements and decisions that have first been understood and recorded at a level proportional to the complexity and risk of the change.

The process establishes a traceability chain connecting requirements, decisions, specifications, implementation, tests, evidence, and acceptance. Product briefs, technical specifications, architecture documents, ADRs, contracts, acceptance criteria, deployment plans, and validation records may serve distinct roles within this chain. Documentation is not used merely as a retrospective description of code; it participates in engineering control and in defining expected behavior before and during implementation.

In Site Portfolio, this approach was applied from the architectural foundation through subsequent product evolution. Decisions concerning architecture, backend engineering, persistence, email integration, production runtime, Knowledge Base, vector retrieval, and IA Jujuju were formalized and connected to their corresponding implementation and validation. The same principle was applied to responsive and visual engineering, where approved requirements were converted into deterministic and verifiable criteria.

The process also preserves separation between implementation, technical verification, and human acceptance. The existence of code or the successful completion of an automated test does not automatically replace approval of the result when a decision requires human, visual, or product evaluation.

This experience demonstrates the use of SDD not merely as a documentation practice, but as a technical governance mechanism for reducing ambiguity, controlling change, preserving decisions, and enabling traceable software evolution.

#### Evidence / Maturity Notes

O uso de SDD no Site Portfólio possui evidência de especificação, implementação, validação e entrega em produção. Outros projetos podem utilizar ou prever práticas semelhantes em níveis diferentes de maturidade; cada alegação deve preservar a evidência específica do respectivo projeto.

The use of SDD in Site Portfolio is supported by specification, implementation, validation, and production-delivery evidence. Other projects may use or plan similar practices at different maturity levels; each claim must preserve the evidence specific to the respective project.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PCS-002 — Workflow de Engenharia Assistida por IA

#### Metadata

Concept ID: PCS-002
Category: PROCESS
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Workflow de Engenharia Assistida por IA
Slug: ai-assisted-engineering-workflow-pt-br
Language: pt-br
Review Status: APPROVED — DOCUMENTARY CONSOLIDATION REQUIRED

##### Approved Content

Luís utiliza um workflow de engenharia assistida por IA no qual ferramentas de inteligência artificial participam de atividades de análise, especificação, implementação e refinamento, mantendo a decisão de produto, a auditoria técnica e o aceite sob governança humana.

No Site Portfólio, o processo executado distribuiu responsabilidades entre Product Owner, ChatGPT, Codex, Figma integrado por MCP, OpenCode, Git/Ubuntu e validação humana. O Product Owner permaneceu responsável por requisitos, restrições, decisões, revisão e aceite. ChatGPT foi utilizado em atividades de análise de engenharia, Specification-Driven Development, arquitetura, planejamento, auditoria e preparação das etapas de execução. Codex e OpenCode participaram de atividades de implementação e refinamento conforme as fases em que foram empregados.

No ciclo de UX/UI e responsividade, Figma foi integrado ao processo de engenharia por MCP com Codex. Composições e propriedades de design aprovadas foram utilizadas como autoridade para especificações responsivas, comparação geométrica e validação visual. O repositório preserva evidências de consulta ao Figma vivo, interação programática com seus elementos, read-back de propriedades, screenshots e validações de geometria, além da separação entre evidência automatizada e revisão humana.

Git e o ambiente Ubuntu foram utilizados como autoridade independente para auditar mudanças produzidas durante o desenvolvimento. Diffs, estado do repositório, testes, verificações estáticas e outras evidências eram inspecionados separadamente da ferramenta que havia realizado a implementação. Essa separação reduz a dependência da autoavaliação do agente executor e preserva um gate verificável antes de aceite e progressão.

O workflow não atribui autonomia irrestrita aos agentes de IA. A responsabilidade é distribuída deliberadamente: ferramentas podem analisar ou executar trabalho técnico, enquanto requisitos, decisões relevantes, avaliação de evidências, aceite e autorização de progressão permanecem controlados pelo processo de engenharia e pelo Product Owner.

A experiência do Site Portfólio demonstra, portanto, um modelo de engenharia governada por humanos e assistida por IA, no qual diferentes ferramentas são utilizadas conforme sua função, com separação entre decisão, execução, auditoria, validação e aceite.

#### EN

Title: AI-Assisted Engineering Workflow
Slug: ai-assisted-engineering-workflow-en
Language: en
Review Status: APPROVED — DOCUMENTARY CONSOLIDATION REQUIRED

##### Approved Content

Luís uses an AI-assisted engineering workflow in which artificial intelligence tools participate in analysis, specification, implementation, and refinement activities while product decisions, technical auditing, and acceptance remain under human governance.

In Site Portfolio, the executed process distributed responsibilities among the Product Owner, ChatGPT, Codex, Figma integrated through MCP, OpenCode, Git/Ubuntu, and human validation. The Product Owner remained responsible for requirements, constraints, decisions, review, and acceptance. ChatGPT was used for engineering analysis, Specification-Driven Development, architecture, planning, auditing, and preparation of execution stages. Codex and OpenCode participated in implementation and refinement activities according to the phases in which they were employed.

During the UX/UI and responsive engineering cycle, Figma was integrated into the engineering process through MCP with Codex. Approved design compositions and properties were used as authorities for responsive specifications, geometry comparison, and visual validation. The repository preserves evidence of querying live Figma state, programmatic interaction with its elements, property read-back, screenshots, and geometry validation, together with separation between automated evidence and human review.

Git and the Ubuntu environment were used as independent authorities for auditing changes produced during development. Diffs, repository state, tests, static checks, and other evidence were inspected separately from the tool that performed the implementation. This separation reduces dependence on self-assessment by the executing agent and preserves a verifiable gate before acceptance and progression.

The workflow does not grant unrestricted autonomy to AI agents. Responsibility is deliberately distributed: tools may analyze or execute technical work, while requirements, relevant decisions, evidence assessment, acceptance, and authorization to progress remain controlled by the engineering process and the Product Owner.

The Site Portfolio experience therefore demonstrates a model of human-governed, AI-assisted engineering, in which different tools are used according to their roles, with separation between decision-making, execution, auditing, validation, and acceptance.

#### Evidence / Maturity Notes

O workflow foi efetivamente executado e é aprovado pelo Product Owner. O repositório possui evidência técnica substancial de Figma, validação visual, validação baseada em Git e separação entre evidência automatizada e Human Review. Entretanto, a identificação nominal e a atribuição completa dos papéis de ChatGPT, Codex, Figma MCP e OpenCode não foram consolidadas de forma suficiente nos artefatos contemporâneos do projeto. Essa lacuna documental deve ser preservada como tal e corrigida antes de este conceito adquirir autoridade documental integral para o RAG.

The workflow was actually executed and is approved by the Product Owner. The repository contains substantial technical evidence of Figma, visual validation, Git-based validation, and separation between automated evidence and Human Review. However, the nominal identification and complete attribution of the roles of ChatGPT, Codex, Figma MCP, and OpenCode were not sufficiently consolidated in the project's contemporaneous artifacts. This documentation gap must be preserved as such and corrected before this concept acquires full documentary authority for RAG.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PCS-003 — Validação de Engenharia Baseada em Git

#### Metadata

Concept ID: PCS-003
Category: PROCESS
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Validação de Engenharia Baseada em Git
Slug: git-based-engineering-validation-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís utiliza Git não apenas como mecanismo de versionamento, mas também como uma das autoridades de validação do processo de engenharia. Mudanças implementadas são verificadas a partir do estado real do repositório, permitindo distinguir o que uma ferramenta declara ter realizado daquilo que efetivamente foi incorporado ao código e à documentação.

O processo pode verificar baseline inicial, branch, commit de origem, arquivos modificados, diff, integridade textual, escopo da alteração, árvore de trabalho, relação entre commits locais e remotos e ausência de mudanças não previstas. Comandos como `git status`, `git diff`, `git diff --check`, `git show`, `git log` e verificações de divergência são utilizados como evidências independentes conforme a necessidade da mudança.

No Site Portfólio, essa disciplina foi combinada com quality gates de engenharia. Alterações relevantes foram submetidas, conforme o escopo, a testes automatizados, Ruff, mypy, verificações do Django, validações de migrations, staticfiles, segurança, geometria ou comportamento funcional. Resultados bloqueados pelo ambiente foram registrados como bloqueados em vez de convertidos artificialmente em sucesso.

A separação entre executor e auditoria é especialmente relevante em um workflow assistido por IA. A ferramenta que modifica o repositório não é considerada autoridade suficiente para certificar sozinha sua própria alteração. O estado observado pelo Git e os resultados dos gates executados independentemente constituem evidência para a decisão humana de aceitar, corrigir ou rejeitar a mudança.

Esse processo melhora rastreabilidade, reduz risco de alterações acidentais e permite associar uma decisão técnica a um conjunto verificável de mudanças e evidências antes do push, deployment ou encerramento de uma etapa.

#### EN

Title: Git-Based Engineering Validation
Slug: git-based-engineering-validation-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís uses Git not only as a version-control mechanism, but also as one of the authorities for validating the engineering process. Implemented changes are verified against the actual repository state, making it possible to distinguish what a tool reports having done from what was actually incorporated into code and documentation.

The process may verify the initial baseline, branch, source commit, modified files, diff, textual integrity, change scope, working tree, relationship between local and remote commits, and absence of unintended changes. Commands such as `git status`, `git diff`, `git diff --check`, `git show`, `git log`, and divergence checks are used as independent evidence according to the needs of the change.

In Site Portfolio, this discipline was combined with engineering quality gates. Relevant changes were subjected, according to scope, to automated tests, Ruff, mypy, Django checks, migrations validation, staticfiles checks, security checks, geometry validation, or functional behavior verification. Results blocked by the environment were recorded as blocked rather than artificially converted into success.

The separation between executor and audit is particularly relevant in an AI-assisted workflow. The tool modifying the repository is not considered sufficient authority to certify its own change independently. The state observed through Git and the results of independently executed gates provide evidence for the human decision to accept, correct, or reject the change.

This process improves traceability, reduces the risk of accidental modifications, and makes it possible to associate a technical decision with a verifiable set of changes and evidence before push, deployment, or closure of an engineering stage.

#### Evidence / Maturity Notes

A validação baseada em Git possui evidência recorrente ao longo da engenharia do Site Portfólio, incluindo auditoria de diffs, quality gates, controle de commits e certificações de baseline. O processo foi aplicado durante implementação, validação e preparação de entregas em produção.

Git-based validation has recurring evidence throughout Site Portfolio engineering, including diff auditing, quality gates, commit control, and baseline certifications. The process was applied during implementation, validation, and preparation for production delivery.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PCS-004 — Modernização de Software Legado

#### Metadata

Concept ID: PCS-004
Category: PROCESS
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Modernização de Software Legado
Slug: legacy-software-modernization-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís aborda modernização de software legado como um processo de reavaliação de produto e engenharia, e não apenas como substituição de tecnologias. O objetivo é compreender o sistema existente, preservar o conhecimento útil, identificar limitações e redefinir arquitetura, requisitos, experiência de uso e critérios de qualidade de acordo com as necessidades atuais.

O Site Portfólio constitui o principal caso atual dessa abordagem. Uma presença profissional anteriormente construída com menor formalização de engenharia foi reavaliada e transformada em uma plataforma desenvolvida por especificações, arquitetura explícita, backend estruturado, persistência relacional, testes, automação de qualidade, deployment controlado e posteriormente capacidades de Knowledge Base, recuperação vetorial e IA.

A modernização incluiu também revisão progressiva da experiência visual e responsiva. Em vez de tratar diferentes tamanhos de tela apenas como reduções proporcionais do desktop, o projeto estabeleceu referências específicas, critérios geométricos e validação em múltiplos viewports. Figma integrado por MCP com Codex fez parte do processo efetivamente executado para determinadas atividades de design e refinamento, acompanhado de validação técnica e revisão humana.

Esse método preserva uma distinção importante entre o sistema histórico e sua evolução. Práticas modernas não são atribuídas retroativamente ao legado. O sistema anterior permanece evidência de seu período e de sua maturidade original; a reengenharia posterior demonstra a evolução do processo, das decisões e da capacidade de entrega.

A mesma abordagem fornece uma referência para futuras modernizações: primeiro compreender e classificar o legado; depois decidir o que preservar, substituir ou redesenhar; especificar o novo baseline; implementar de forma controlada; validar comportamento e qualidade; e somente então elevar a maturidade das alegações sobre o sistema.

#### EN

Title: Legacy Software Modernization
Slug: legacy-software-modernization-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís approaches legacy software modernization as a product and engineering reassessment process rather than merely a replacement of technologies. The objective is to understand the existing system, preserve useful knowledge, identify limitations, and redefine architecture, requirements, user experience, and quality criteria according to current needs.

Site Portfolio is the primary current case of this approach. A professional web presence previously built with less formal engineering was reassessed and transformed into a platform developed through specifications, explicit architecture, structured backend engineering, relational persistence, testing, quality automation, controlled deployment, and subsequently Knowledge Base, vector retrieval, and AI capabilities.

Modernization also included progressive revision of the visual and responsive experience. Rather than treating different screen sizes merely as proportional reductions of desktop layouts, the project established specific references, geometric criteria, and validation across multiple viewports. Figma integrated through MCP with Codex was part of the process actually executed for specific design and refinement activities, accompanied by technical validation and human review.

This method preserves an important distinction between the historical system and its evolution. Modern practices are not retroactively attributed to the legacy system. The previous system remains evidence of its period and original maturity; subsequent reengineering demonstrates the evolution of the process, decisions, and delivery capability.

The same approach provides a reference for future modernization efforts: first understand and classify the legacy system; then decide what to preserve, replace, or redesign; specify the new baseline; implement in a controlled manner; validate behavior and quality; and only then elevate the maturity of claims about the system.

#### Evidence / Maturity Notes

A modernização do Site Portfólio possui evidência histórica, especificação, implementação, validação visual e técnica e operação em produção. Outros sistemas legados do portfólio não devem ser descritos como modernizados enquanto essa evolução não tiver sido efetivamente executada e comprovada.

Site Portfolio modernization is supported by historical evidence, specification, implementation, visual and technical validation, and production operation. Other legacy systems in the portfolio must not be described as modernized until that evolution has actually been executed and demonstrated.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-ENG-001 — Engenharia Backend

#### Metadata

Concept ID: ENG-001
Category: ENGINEERING
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Engenharia Backend
Slug: backend-engineering-evidence-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís demonstra engenharia backend por meio da construção de aplicações em que regras de negócio, contratos, persistência, integrações e comportamento operacional são tratados como responsabilidades explícitas e testáveis, em vez de ficarem acoplados à interface.

No Site Portfólio, o backend foi estruturado como um monólito modular em Django, com PostgreSQL como persistência relacional. A solução evoluiu para suportar funcionalidades como contato, administração, Knowledge Base, indexação, recuperação de conhecimento, conversações e IA Jujuju sem introduzir uma arquitetura distribuída desnecessária para a escala e os requisitos do produto.

O desenvolvimento do backend inclui validação de entradas, contratos de dados, tratamento de falhas e isolamento de dependências externas. No fluxo de contato, por exemplo, a persistência da solicitação foi projetada para sobreviver a falhas da integração de notificação, evitando que indisponibilidade do provedor externo resulte em perda do dado principal.

Na infraestrutura de conhecimento e IA, integrações com providers externos foram isoladas por abstrações próprias. Operações potencialmente lentas, como geração de embeddings ou chamadas ao modelo, foram mantidas fora de transações longas de banco de dados. A substituição dos chunks indexados utiliza uma etapa atômica curta, preservando um índice válido anterior quando uma tentativa posterior de reindexação falha.

A engenharia backend aplicada no projeto demonstra preocupação conjunta com correção, simplicidade arquitetural, consistência de dados, tratamento de falhas, testabilidade e comportamento em produção.

#### EN

Title: Backend Engineering
Slug: backend-engineering-evidence-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís demonstrates backend engineering through applications in which business rules, contracts, persistence, integrations, and operational behavior are treated as explicit and testable responsibilities rather than being coupled to the user interface.

In Site Portfolio, the backend was structured as a Django modular monolith with PostgreSQL as relational persistence. The solution evolved to support capabilities such as contact handling, administration, Knowledge Base, indexing, knowledge retrieval, conversations, and IA Jujuju without introducing a distributed architecture unnecessary for the product's scale and requirements.

Backend development includes input validation, data contracts, failure handling, and isolation of external dependencies. In the contact workflow, for example, request persistence was designed to survive notification-integration failures, preventing an external provider outage from causing loss of the primary data.

Within the knowledge and AI infrastructure, integrations with external providers were isolated behind dedicated abstractions. Potentially slow operations, such as embedding generation or model calls, were kept outside long-running database transactions. Replacement of indexed chunks uses a short atomic stage, preserving a previously valid index when a later reindexing attempt fails.

The backend engineering applied to the project demonstrates combined attention to correctness, architectural simplicity, data consistency, failure handling, testability, and production behavior.

#### Evidence / Maturity Notes

O Site Portfólio fornece evidência de implementação, testes, validação e operação em produção para seu backend Django e para funcionalidades centrais associadas. Tecnologias ou padrões utilizados em outros projetos devem conservar o nível de maturidade demonstrado pela evidência específica desses projetos.

Site Portfolio provides implementation, testing, validation, and production-operation evidence for its Django backend and associated core capabilities. Technologies or patterns used in other projects must retain the maturity level demonstrated by the specific evidence for those projects.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-ENG-002 — Engenharia de Testes e Qualidade

#### Metadata

Concept ID: ENG-002
Category: ENGINEERING
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Engenharia de Testes e Qualidade
Slug: testing-quality-engineering-evidence-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís aplica testes e quality gates como mecanismos de redução de risco e produção de evidência sobre o comportamento do software. A estratégia de qualidade é definida de acordo com a natureza da mudança e pode combinar testes automatizados, análise estática, validação estrutural, inspeção de configuração, testes de integração e revisão humana.

No Site Portfólio, pytest foi utilizado para validar comportamento de módulos como homepage, contato, administração, Knowledge Base, IA Jujuju e políticas de retenção. Ruff, mypy e verificações do Django complementaram os testes funcionais com análise de qualidade, tipagem e consistência da aplicação. Migrations, staticfiles e configurações relevantes também foram submetidos a gates específicos durante a evolução e preparação para produção.

A validação não se limitou ao backend. O refinamento responsivo utilizou medições de geometria, screenshots, comparação com referências aprovadas e múltiplos viewports. Evidência automatizada foi deliberadamente separada de Human Review: uma correspondência geométrica ou a passagem de um teste não substitui o julgamento humano quando o requisito envolve qualidade visual ou decisão de produto.

O processo também registra limitações de evidência. Quando um teste não pode ser executado por restrição ambiental, o resultado deve permanecer bloqueado ou não verificado, em vez de ser interpretado como aprovação. Da mesma forma, uma verificação parcial não é utilizada para elevar a maturidade de toda a funcionalidade.

Essa disciplina permite que testes sejam tratados não apenas como mecanismo para encontrar defeitos, mas como parte da rastreabilidade entre requisito, implementação, evidência e aceite.

#### EN

Title: Testing & Quality Engineering
Slug: testing-quality-engineering-evidence-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís applies testing and quality gates as mechanisms for reducing risk and producing evidence about software behavior. The quality strategy is defined according to the nature of the change and may combine automated testing, static analysis, structural validation, configuration inspection, integration testing, and human review.

In Site Portfolio, pytest was used to validate the behavior of modules such as the homepage, contact, administration, Knowledge Base, IA Jujuju, and retention policies. Ruff, mypy, and Django checks complemented functional tests with quality analysis, typing verification, and application consistency checks. Migrations, staticfiles, and relevant configuration were also subjected to specific gates during product evolution and production preparation.

Validation was not limited to the backend. Responsive refinement used geometry measurements, screenshots, comparison against approved references, and multiple viewports. Automated evidence was deliberately separated from Human Review: geometric correspondence or successful test execution does not replace human judgment when a requirement concerns visual quality or a product decision.

The process also records limitations in evidence. When a test cannot be executed because of an environmental restriction, the result must remain blocked or unverified rather than being interpreted as approval. Likewise, a partial verification is not used to elevate the maturity of an entire capability.

This discipline allows tests to be treated not merely as a mechanism for finding defects, but as part of the traceability between requirement, implementation, evidence, and acceptance.

#### Evidence / Maturity Notes

A engenharia de testes e qualidade do Site Portfólio possui evidência de suites automatizadas, análise estática, quality gates, validações visuais e geométricas e verificações realizadas no ciclo de produção. A abrangência de cada claim deve permanecer limitada aos gates efetivamente executados e aprovados.

Testing and quality engineering in Site Portfolio is supported by automated suites, static analysis, quality gates, visual and geometric validation, and checks performed during the production cycle. The scope of each claim must remain limited to the gates actually executed and approved.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-ENG-003 — Engenharia de RAG e Recuperação Vetorial

#### Metadata

Concept ID: ENG-003
Category: ENGINEERING
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Engenharia de RAG e Recuperação Vetorial
Slug: rag-vector-retrieval-engineering-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís demonstra engenharia de Retrieval-Augmented Generation (RAG) no Site Portfólio por meio da implementação de uma arquitetura que conecta conhecimento aprovado, embeddings, recuperação vetorial, contexto controlado e geração de respostas pela IA Jujuju.

A solução reutiliza PostgreSQL com pgvector como infraestrutura de armazenamento relacional e vetorial, evitando a introdução de um banco vetorial dedicado sem necessidade comprovada. Para a escala atual, a recuperação utiliza busca exata por similaridade de cosseno, sem índice ANN, reduzindo complexidade operacional enquanto mantém a arquitetura compatível com evolução futura caso volume e desempenho passem a justificar outra estratégia.

Documentos da Knowledge Base são normalizados e divididos deterministicamente em chunks semanticamente manejáveis. Embeddings são gerados por provider isolado e armazenados como vetores de dimensão controlada. A indexação valida a dimensionalidade antes da persistência e utiliza substituição atômica dos chunks, preservando um índice anteriormente válido quando uma reindexação falha.

A recuperação exige idioma e pode aplicar categoria como filtro tipado, combinando controle de metadados com similaridade vetorial. Os chunks recuperados são utilizados como contexto controlado para o modelo de linguagem, e evidências de origem podem ser associadas à conversa e às mensagens para preservar rastreabilidade entre conhecimento recuperado e resposta produzida.

A arquitetura também separa retrieval e geração por abstrações de provider, permitindo testes determinísticos com fakes sem depender de chamadas externas ao executar a suíte automatizada. Chamadas reais aos providers são reservadas para validações operacionais controladas.

Em produção, o pipeline foi validado com geração real de embeddings, armazenamento vetorial, recuperação semântica e execução end-to-end da IA Jujuju, incluindo persistência da conversa e da evidência associada.

#### EN

Title: RAG & Vector Retrieval Engineering
Slug: rag-vector-retrieval-engineering-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís demonstrates Retrieval-Augmented Generation (RAG) engineering in Site Portfolio through the implementation of an architecture connecting approved knowledge, embeddings, vector retrieval, controlled context, and response generation by IA Jujuju.

The solution reuses PostgreSQL with pgvector as relational and vector-storage infrastructure, avoiding the introduction of a dedicated vector database without demonstrated need. At the current scale, retrieval uses exact cosine-similarity search without an ANN index, reducing operational complexity while preserving an architecture capable of evolving if corpus size and performance requirements later justify a different strategy.

Knowledge Base documents are normalized and deterministically divided into semantically manageable chunks. Embeddings are generated through an isolated provider and stored as vectors with controlled dimensionality. Indexing validates dimensionality before persistence and uses atomic chunk replacement, preserving a previously valid index when reindexing fails.

Retrieval requires a language and may apply category as a typed filter, combining metadata control with vector similarity. Retrieved chunks are used as controlled context for the language model, and source evidence can be associated with conversations and messages to preserve traceability between retrieved knowledge and the generated response.

The architecture also separates retrieval and generation through provider abstractions, enabling deterministic tests with fakes without depending on external calls during the automated test suite. Real provider calls are reserved for controlled operational validation.

In production, the pipeline was validated with real embedding generation, vector storage, semantic retrieval, and end-to-end execution of IA Jujuju, including persistence of the conversation and its associated evidence.

#### Evidence / Maturity Notes

Knowledge Base, embeddings, pgvector, recuperação semântica, integração RAG e geração da IA Jujuju possuem evidência de implementação, validação e execução em produção no Site Portfólio. Isso não autoriza atribuir o mesmo maturity level a capacidades de IA ou Machine Learning apenas planejadas em outros projetos.

Knowledge Base, embeddings, pgvector, semantic retrieval, RAG integration, and IA Jujuju generation have implementation, validation, and production-execution evidence in Site Portfolio. This does not authorize assigning the same maturity level to AI or Machine Learning capabilities that are only planned in other projects.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-ENG-004 — Engenharia de Segurança

#### Metadata

Concept ID: ENG-004
Category: ENGINEERING
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Engenharia de Segurança
Slug: security-engineering-evidence-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís aplica segurança como responsabilidade transversal da engenharia, abrangendo configuração da aplicação, controle de acesso, proteção de dados e segredos, integrações externas, comportamento em produção e resposta a incidentes.

No Site Portfólio, a área administrativa utiliza os mecanismos nativos de autenticação, autorização, usuários, grupos e permissões do Django, evitando a criação de um sistema de identidade próprio sem necessidade. O acesso administrativo é separado da experiência pública, enquanto os dados e operações disponíveis no Admin respeitam as responsabilidades definidas para cada módulo.

Configurações sensíveis são fornecidas por ambiente e não devem ser incorporadas ao código-fonte. O runtime de produção utiliza configurações específicas para HTTPS e cookies seguros, além de isolamento entre aplicação pública, Gunicorn, Nginx e PostgreSQL. Decisões de hardening são aplicadas proporcionalmente ao estado operacional e às condições verificadas do ambiente.

O projeto também produziu evidência prática de resposta a exposição acidental de credenciais durante atividades operacionais. Segredos comprometidos foram tratados como comprometidos, rotacionados e invalidados quando aplicável, permissões do arquivo de ambiente foram verificadas e artefatos temporários contendo valores sensíveis foram removidos. A validação posterior foi realizada sem reutilizar os valores expostos como evidência pública.

Na IA Jujuju, controles adicionais reduzem risco de abuso e de utilização inadequada do contexto recuperado. A arquitetura procura limitar respostas ao conhecimento autorizado, preservar rastreabilidade das fontes e separar instruções do sistema do conteúdo recuperado, reduzindo a confiança indevida em conteúdo que possa tentar alterar o comportamento do assistente.

A experiência demonstra segurança como processo contínuo de prevenção, verificação e correção, e não como atributo presumido apenas pela escolha de um framework ou infraestrutura.

#### EN

Title: Security Engineering
Slug: security-engineering-evidence-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís applies security as a cross-cutting engineering responsibility encompassing application configuration, access control, protection of data and secrets, external integrations, production behavior, and incident response.

In Site Portfolio, the administrative area uses Django's native authentication, authorization, user, group, and permission mechanisms, avoiding the creation of a custom identity system without demonstrated need. Administrative access is separated from the public experience, while data and operations exposed through the Admin respect the responsibilities defined for each module.

Sensitive configuration is provided through the environment and must not be incorporated into source code. The production runtime uses specific configuration for HTTPS and secure cookies, together with separation among the public application, Gunicorn, Nginx, and PostgreSQL. Hardening decisions are applied proportionally to the operational state and verified conditions of the environment.

The project also produced practical evidence of response to accidental credential exposure during operational activities. Compromised secrets were treated as compromised, rotated and invalidated where applicable, environment-file permissions were verified, and temporary artifacts containing sensitive values were removed. Subsequent validation was performed without reusing the exposed values as public evidence.

Within IA Jujuju, additional controls reduce the risk of abuse and inappropriate use of retrieved context. The architecture seeks to constrain responses to authorized knowledge, preserve source traceability, and separate system instructions from retrieved content, reducing undue trust in content that may attempt to alter assistant behavior.

This experience demonstrates security as an ongoing process of prevention, verification, and correction rather than an attribute presumed solely from the choice of framework or infrastructure.

#### Evidence / Maturity Notes

O Site Portfólio possui evidência implementada e operacional para controles específicos de autenticação, autorização, configuração segura, proteção de segredos e resposta a incidentes. Segurança deve ser afirmada controle por controle; essa evidência não constitui alegação de segurança absoluta, ausência de vulnerabilidades ou certificação formal de segurança.

Site Portfolio has implemented and operational evidence for specific authentication, authorization, secure-configuration, secret-protection, and incident-response controls. Security must be asserted control by control; this evidence does not constitute a claim of absolute security, absence of vulnerabilities, or formal security certification.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-ENG-005 — Engenharia de Deployment e Produção

#### Metadata

Concept ID: ENG-005
Category: ENGINEERING
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Engenharia de Deployment e Produção
Slug: deployment-production-engineering-evidence-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís demonstra engenharia de deployment e produção por meio da transformação de uma aplicação validada em um serviço operável, considerando runtime, banco de dados, proxy reverso, arquivos estáticos, configuração, recuperação, observabilidade operacional e validação pós-implantação.

No Site Portfólio, a arquitetura de produção utiliza Nginx como ponto de entrada HTTP/HTTPS, Gunicorn como servidor WSGI, Django como aplicação e PostgreSQL como banco de dados. O serviço da aplicação é administrado pelo systemd, executado sem exposição direta do Gunicorn à Internet e configurado por variáveis de ambiente externas ao código-fonte.

O processo de implantação inclui preparação e verificação do ambiente, sincronização do código aprovado, dependências bloqueadas, migrations, coleta de arquivos estáticos, reinicialização controlada dos serviços e smoke tests. Antes de mudanças relevantes no ambiente, foram produzidos pontos de recuperação contendo os artefatos necessários para suportar rollback e restauração.

A introdução do RAG exigiu também validação das dependências de produção associadas ao PostgreSQL e pgvector. Após a implantação, foram executadas verificações reais do pipeline de conhecimento: criação e indexação de documento, geração de embedding pelo provider, recuperação vetorial e uma pergunta end-to-end à IA Jujuju, com persistência da conversa e evidência correspondente.

A operação também revelou problemas que exigiram correções posteriores, incluindo ajustes de interface, configuração pública e comportamento de arquivos estáticos. Esses casos são tratados como parte da engenharia de produção: a existência de deployment não encerra automaticamente a validação, e problemas observados no ambiente real retornam ao ciclo de diagnóstico, correção, teste e nova implantação.

Dessa forma, produção é tratada como um estado verificável do sistema e não apenas como a execução de um comando de deploy.

#### EN

Title: Deployment & Production Engineering
Slug: deployment-production-engineering-evidence-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís demonstrates deployment and production engineering by transforming a validated application into an operable service while considering runtime, database, reverse proxy, static assets, configuration, recovery, operational observability, and post-deployment validation.

In Site Portfolio, the production architecture uses Nginx as the HTTP/HTTPS entry point, Gunicorn as the WSGI server, Django as the application, and PostgreSQL as the database. The application service is managed by systemd, runs without exposing Gunicorn directly to the Internet, and is configured through environment variables external to source code.

The deployment process includes environment preparation and verification, synchronization of approved code, locked dependencies, migrations, static asset collection, controlled service restarts, and smoke tests. Before relevant environment changes, recovery points were produced containing the artifacts required to support rollback and restoration.

Introducing RAG also required validation of production dependencies associated with PostgreSQL and pgvector. After deployment, real checks of the knowledge pipeline were executed: document creation and indexing, embedding generation through the provider, vector retrieval, and an end-to-end question to IA Jujuju, with persistence of the conversation and corresponding evidence.

Operation also revealed issues requiring subsequent corrections, including interface adjustments, public configuration, and static-asset behavior. These cases are treated as part of production engineering: the existence of a deployment does not automatically close validation, and issues observed in the real environment return to the cycle of diagnosis, correction, testing, and redeployment.

Production is therefore treated as a verifiable state of the system rather than merely the execution of a deployment command.

#### Evidence / Maturity Notes

O Site Portfólio possui evidência real de implantação e operação em produção para componentes centrais, incluindo backend, PostgreSQL e o pipeline RAG da IA Jujuju. Claims específicos comprovados podem ser classificados como production-demonstrated. Entretanto, o status administrativo global `Release 2 Production Deployment: CLOSED` não deve ser afirmado enquanto os gates finais definidos pelo projeto permanecerem abertos.

Site Portfolio has real deployment and production-operation evidence for core components, including the backend, PostgreSQL, and the IA Jujuju RAG pipeline. Specifically demonstrated claims may be classified as production-demonstrated. However, the overall administrative status `Release 2 Production Deployment: CLOSED` must not be asserted while the project's defined final gates remain open.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

## 7. Wave 4 — Portfolio Breadth

Wave 4 contains 6 Knowledge Concepts and 12 KnowledgeDocument variants.

Wave 4 uses categories:

- PROJECT
- PORTFOLIO

All Wave 4 KnowledgeDocument variants are Human Approved.

### KB-PRJ-007 — Enterprise Platform — Plataforma Empresarial Orientada por Especificações

#### Metadata

Concept ID: PRJ-007
Category: PROJECT
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Enterprise Platform — Plataforma Empresarial Orientada por Especificações
Slug: enterprise-platform-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís está desenvolvendo a Enterprise Platform, um projeto orientado por especificações destinado a estabelecer uma arquitetura reutilizável para aplicações empresariais. O projeto aplica princípios de engenharia de software para estruturar uma base capaz de evoluir de forma modular, testável e controlada.

O repositório contém uma extensa baseline documental e arquitetural. Requisitos, decisões, arquitetura e responsabilidades do sistema são tratados antes e durante a implementação, permitindo que a evolução do código seja confrontada com autoridades documentais explícitas em vez de depender exclusivamente do estado corrente da implementação.

A arquitetura foi concebida em torno de uma abordagem modular, privilegiando separação de responsabilidades e evolução incremental sem introduzir complexidade distribuída sem necessidade demonstrada. Essa abordagem busca fornecer uma fundação reutilizável para capacidades empresariais, mantendo rastreabilidade entre necessidades de produto, decisões técnicas e implementação.

O projeto também demonstra uma diferença importante entre arquitetura projetada e funcionalidade efetivamente entregue. Embora a baseline documental estabeleça uma visão ampla para a plataforma, sua implementação permanece em evolução. Capacidades descritas por especificações ou roadmap não devem ser apresentadas automaticamente como funcionalidades concluídas.

A Enterprise Platform representa, portanto, a aplicação de Specification-Driven Development em um sistema empresarial em construção, demonstrando como uma baseline arquitetural pode orientar implementação progressiva sem antecipar como concluído aquilo que ainda está sendo desenvolvido.

#### EN

Title: Enterprise Platform — Specification-Driven Enterprise Platform
Slug: enterprise-platform-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís is developing the Enterprise Platform, a specification-driven project intended to establish a reusable architecture for enterprise applications. The project applies software-engineering principles to structure a foundation capable of evolving in a modular, testable, and controlled manner.

The repository contains an extensive documentation and architecture baseline. Requirements, decisions, architecture, and system responsibilities are addressed before and during implementation, allowing code evolution to be evaluated against explicit documentary authorities rather than depending exclusively on the current implementation state.

The architecture was designed around a modular approach, prioritizing separation of responsibilities and incremental evolution without introducing distributed complexity in the absence of a demonstrated need. This approach is intended to provide a reusable foundation for enterprise capabilities while maintaining traceability among product needs, technical decisions, and implementation.

The project also demonstrates an important distinction between designed architecture and actually delivered functionality. Although the documentation baseline establishes a broad vision for the platform, implementation remains in progress. Capabilities described by specifications or the roadmap must not automatically be presented as completed functionality.

The Enterprise Platform therefore represents the application of Specification-Driven Development to an enterprise system under construction, demonstrating how an architecture baseline can guide progressive implementation without prematurely presenting unfinished capabilities as complete.

#### Evidence / Maturity Notes

A Enterprise Platform possui forte evidência documental e arquitetural e implementação em evolução. Claims sobre funcionalidades específicas devem respeitar o estado comprovado de cada capacidade. Não deve ser apresentada como plataforma empresarial integralmente implementada ou implantada em produção sem evidência correspondente.

The Enterprise Platform has strong documentation and architecture evidence, with implementation in progress. Claims concerning specific functionality must preserve the demonstrated state of each capability. It must not be represented as a fully implemented or production-deployed enterprise platform without corresponding evidence.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-008 — Intelligent Currency Platform — Evolução de Sistema de Cotações

#### Metadata

Concept ID: PRJ-008
Category: PROJECT
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Intelligent Currency Platform — Evolução de Sistema de Cotações
Slug: intelligent-currency-platform-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

Luís está desenvolvendo a Intelligent Currency Platform como uma evolução planejada do domínio de software de cotação de moedas trabalhado anteriormente em um projeto legado. A iniciativa busca reavaliar o problema utilizando práticas contemporâneas de arquitetura e engenharia de software, em vez de simplesmente ampliar a implementação histórica.

O projeto possui uma baseline de produto e especificação que descreve a direção pretendida para a plataforma. Essa documentação estabelece requisitos e capacidades planejadas para uma solução mais estruturada, incluindo evolução da arquitetura, persistência e interfaces de aplicação.

O roadmap do projeto inclui capacidades planejadas de Machine Learning e Inteligência Artificial. Essas capacidades pertencem à direção futura do produto e não devem ser descritas como funcionalidades já implementadas ou validadas.

A implementação encontra-se em estágio inicial. Por esse motivo, a Knowledge Base distingue explicitamente aquilo que foi especificado ou planejado daquilo que possui evidência de implementação. Essa separação evita transformar intenção arquitetural ou roadmap em alegação de produto concluído.

A Intelligent Currency Platform demonstra uma abordagem de evolução de software na qual experiência adquirida em uma solução anterior é utilizada como insumo para uma nova avaliação de produto, arquitetura e engenharia, com maior disciplina de especificação e rastreabilidade.

#### EN

Title: Intelligent Currency Platform — Currency System Evolution
Slug: intelligent-currency-platform-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís is developing the Intelligent Currency Platform as a planned evolution of the currency-quotation software domain previously explored through a legacy project. The initiative seeks to reassess the problem using contemporary software architecture and engineering practices rather than simply extending the historical implementation.

The project has a product and specification baseline describing the intended direction of the platform. This documentation establishes requirements and planned capabilities for a more structured solution, including architectural evolution, persistence, and application interfaces.

The project's roadmap includes planned machine-learning and AI capabilities. These capabilities belong to the future direction of the product and must not be described as already implemented or validated functionality.

Implementation is currently at an early stage. For this reason, the Knowledge Base explicitly distinguishes what has been specified or planned from what has implementation evidence. This separation prevents architectural intent or roadmap items from becoming claims of completed product functionality.

The Intelligent Currency Platform demonstrates a software-evolution approach in which experience acquired from an earlier solution is used as input for a new assessment of product, architecture, and engineering, with greater specification discipline and traceability.

#### Evidence / Maturity Notes

O projeto possui evidência de especificação e implementação inicial. Funcionalidades futuras descritas no PRD ou roadmap permanecem planejadas até que implementação e validação correspondentes sejam comprovadas. Em particular, capacidades de Machine Learning e IA são planejadas.

The project has specification evidence and early implementation evidence. Future functionality described in the PRD or roadmap remains planned until corresponding implementation and validation are demonstrated. In particular, machine-learning and AI capabilities are planned.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-009 — Sistema Legado de Cotação de Moedas

#### Metadata

Concept ID: PRJ-009
Category: PROJECT
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Sistema Legado de Cotação de Moedas
Slug: legacy-currency-system-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

O Sistema Legado de Cotação de Moedas registra uma etapa anterior da trajetória de desenvolvimento de software de Luís. O projeto foi construído em Python para automatizar atividades relacionadas à consulta de cotações de moedas e à produção de informações derivadas dessas consultas.

A implementação trabalhou com integração a uma API externa de cotações e automação do processamento dos dados retornados. O projeto também explorou geração de relatórios e organização progressiva do código conforme sua complexidade aumentava.

Sua evolução registra uma transição de uma implementação inicialmente mais direta para uma organização orientada a objetos e posteriormente estruturada segundo responsabilidades inspiradas em MVC. Testes e mocks também passaram a fazer parte do projeto, permitindo exercitar comportamentos sem depender exclusivamente da integração externa real.

Esse projeto é preservado no portfólio como evidência histórica, e não como representação da arquitetura atualmente recomendada por Luís. Seu valor está também em permitir observar problemas, decisões e práticas de uma fase anterior e compará-los com projetos posteriores orientados por especificações, arquitetura explícita, testes sistemáticos e processos de validação mais rigorosos.

A experiência adquirida nesse domínio contribui para a posterior reavaliação representada pela Intelligent Currency Platform, sem implicar que os dois projetos possuam a mesma arquitetura ou maturity level.

#### EN

Title: Legacy Currency Quotation System
Slug: legacy-currency-system-en
Language: en
Review Status: APPROVED

##### Approved Content

The Legacy Currency Quotation System records an earlier stage in Luís's software-development trajectory. The project was built in Python to automate activities related to retrieving currency quotations and producing information derived from those queries.

The implementation worked with integration to an external currency-quotation API and automated processing of the returned data. The project also explored report generation and progressive organization of the code as its complexity increased.

Its evolution records a transition from an initially more direct implementation toward object-oriented organization and subsequently toward responsibilities inspired by MVC. Tests and mocks also became part of the project, allowing behaviors to be exercised without depending exclusively on the real external integration.

This project is preserved in the portfolio as historical evidence rather than as a representation of the architecture Luís currently recommends. Its value also lies in making it possible to observe problems, decisions, and practices from an earlier stage and compare them with later projects driven by specifications, explicit architecture, systematic testing, and more rigorous validation processes.

Experience acquired in this domain contributes to the later reassessment represented by the Intelligent Currency Platform, without implying that the two projects share the same architecture or maturity level.

#### Evidence / Maturity Notes

O projeto possui evidência histórica de implementação. Claims devem permanecer associados às capacidades comprovadas pelo repositório legado e não devem atribuir retroativamente práticas, arquitetura ou maturidade pertencentes aos projetos atuais.

The project has historical implementation evidence. Claims must remain associated with capabilities demonstrated by the legacy repository and must not retroactively assign practices, architecture, or maturity belonging to current projects.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-010 — Gerenciador de Tarefas Desktop

#### Metadata

Concept ID: PRJ-010
Category: PROJECT
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Gerenciador de Tarefas Desktop
Slug: task-manager-desktop-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

O Gerenciador de Tarefas Desktop é um projeto histórico desenvolvido por Luís em Python com interface gráfica baseada em Tkinter. A aplicação explora o gerenciamento local de tarefas por meio de uma interface desktop e persistência baseada em arquivos JSON.

O projeto permitiu trabalhar conceitos fundamentais de desenvolvimento de aplicações, incluindo interação com usuário, manipulação de estado, persistência local e organização do código necessária para coordenar comportamento de interface e dados.

Sua utilização de Tkinter e JSON corresponde às necessidades e ao estágio técnico em que o projeto foi desenvolvido. Esses elementos são preservados como parte da evidência histórica e não devem ser reinterpretados como escolhas arquiteturais para os sistemas atuais do portfólio.

Dentro da trajetória de engenharia, o projeto ajuda a demonstrar a progressão entre aplicações locais relativamente autocontidas e sistemas posteriores com arquitetura web, bancos relacionais, APIs, processos formais de especificação, testes, deployment e integrações de IA.

O Gerenciador de Tarefas Desktop é, portanto, relevante não apenas pela funcionalidade construída, mas por registrar uma etapa concreta da evolução técnica representada pelo portfólio.

#### EN

Title: Desktop Task Manager
Slug: task-manager-desktop-en
Language: en
Review Status: APPROVED

##### Approved Content

The Desktop Task Manager is a historical project developed by Luís in Python with a graphical interface based on Tkinter. The application explores local task management through a desktop interface and JSON-based persistence.

The project provided experience with fundamental application-development concepts, including user interaction, state manipulation, local persistence, and the code organization required to coordinate interface behavior and data.

Its use of Tkinter and JSON corresponds to the needs and technical stage in which the project was developed. These elements are preserved as part of the historical evidence and must not be reinterpreted as architectural choices for the portfolio's current systems.

Within the engineering trajectory, the project helps demonstrate progression from relatively self-contained local applications toward later systems involving web architecture, relational databases, APIs, formal specification processes, testing, deployment, and AI integrations.

The Desktop Task Manager is therefore relevant not only for the functionality that was built, but also because it records a concrete stage in the technical evolution represented by the portfolio.

#### Evidence / Maturity Notes

Projeto histórico com evidência de implementação em Python, Tkinter e persistência JSON. O conteúdo não deve atribuir ao projeto práticas modernas que não estejam comprovadas em sua implementação histórica.

This is a historical project with implementation evidence involving Python, Tkinter, and JSON persistence. The content must not attribute modern practices to the project unless they are demonstrated by its historical implementation.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-PRJ-011 — Gerenciador de Tarefas Web — Baseline Legada

#### Metadata

Concept ID: PRJ-011
Category: PROJECT
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Gerenciador de Tarefas Web — Baseline Legada
Slug: task-manager-web-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

O Gerenciador de Tarefas Web é um projeto histórico desenvolvido por Luís utilizando Python e Flask. A aplicação levou o domínio de gerenciamento de tarefas para uma interface web, mantendo uma solução de persistência baseada em JSON.

O projeto registra uma etapa de transição entre aplicações desktop e desenvolvimento web. Sua implementação permitiu trabalhar rotas HTTP, renderização de páginas, processamento de entradas do usuário e integração entre a camada web e a persistência da aplicação.

A arquitetura e as decisões do projeto refletem o contexto técnico em que ele foi construído. Ele é atualmente tratado como software legado e não como baseline de arquitetura recomendada para novos sistemas.

O projeto possui relevância adicional porque foi selecionado como candidato para uma futura modernização. A intenção é reavaliar seus requisitos e arquitetura utilizando práticas contemporâneas de engenharia e Specification-Driven Development, em vez de simplesmente refatorar incrementalmente o código existente.

Essa modernização ainda é uma intenção futura. Portanto, práticas, tecnologias ou arquitetura que venham a ser adotadas nesse ciclo não devem ser atribuídas à baseline legada antes de serem especificadas, implementadas e validadas.

#### EN

Title: Web Task Manager — Legacy Baseline
Slug: task-manager-web-en
Language: en
Review Status: APPROVED

##### Approved Content

The Web Task Manager is a historical project developed by Luís using Python and Flask. The application brought the task-management domain to a web interface while retaining a JSON-based persistence solution.

The project records a transition stage between desktop applications and web development. Its implementation provided experience with HTTP routes, page rendering, user-input processing, and integration between the web layer and application persistence.

The project's architecture and decisions reflect the technical context in which it was built. It is currently treated as legacy software rather than as a recommended architecture baseline for new systems.

The project has additional relevance because it has been selected as a candidate for future modernization. The intention is to reassess its requirements and architecture using contemporary engineering practices and Specification-Driven Development rather than simply refactoring the existing code incrementally.

This modernization remains a future intention. Therefore, practices, technologies, or architecture that may be adopted during that cycle must not be attributed to the legacy baseline before they are specified, implemented, and validated.

#### Evidence / Maturity Notes

A implementação Flask/JSON pertence à evidência histórica do projeto. A modernização por SDD é planejada e deve permanecer descrita como futura até que o novo ciclo de engenharia produza evidências de especificação, implementação e validação.

The Flask/JSON implementation belongs to the project's historical evidence. Modernization through SDD is planned and must remain described as future work until the new engineering cycle produces specification, implementation, and validation evidence.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

---

### KB-POR-001 — Evolução da Engenharia no Portfólio de Luís França

#### Metadata

Concept ID: POR-001
Category: PORTFOLIO
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Evolução da Engenharia no Portfólio de Luís França
Slug: portfolio-engineering-evolution-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

O portfólio de Luís França registra uma trajetória de evolução técnica por meio de projetos construídos em diferentes momentos, com níveis distintos de arquitetura, processo, validação e maturidade operacional. Os projetos são preservados não apenas para apresentar resultados, mas também para tornar visível essa evolução.

Projetos históricos, como os gerenciadores de tarefas desktop e web e o sistema legado de cotação de moedas, registram experiências com Python, interfaces desktop, desenvolvimento web, persistência em arquivos, integração com APIs, orientação a objetos, organização arquitetural e testes em estágios anteriores da trajetória.

Projetos mais recentes demonstram uma mudança para processos de engenharia mais explícitos. Specification-Driven Development, decisões arquiteturais registradas, rastreabilidade, testes sistemáticos, Git como autoridade de validação, bancos relacionais, deployment controlado e práticas de segurança passam a fazer parte da construção e evolução dos sistemas.

O Site Portfólio constitui o caso mais completo dessa evolução atualmente demonstrado no próprio portfólio. O projeto percorreu especificação, arquitetura, implementação, testes, validação, evolução de UX/UI, integração com design, deployment em produção e construção de uma Knowledge Base com recuperação vetorial e RAG para a IA Jujuju.

Outros projetos representam diferentes pontos dessa trajetória. A Enterprise Platform possui uma baseline documental e arquitetural extensa com implementação em evolução. A Intelligent Currency Platform reavalia um domínio anteriormente explorado e possui capacidades futuras especificadas ou planejadas que ainda não devem ser confundidas com implementação concluída. Projetos legados permanecem preservados como evidência histórica e como referência para futuros ciclos de modernização.

Essa composição permite avaliar competência profissional sem nivelar artificialmente todos os projetos pelo mesmo maturity level. O portfólio procura mostrar tanto o que foi construído no passado quanto a forma como decisões, arquitetura, qualidade, segurança, IA e produção passaram a ser tratadas de maneira progressivamente mais sistemática.

#### EN

Title: Engineering Evolution Across Luís França's Portfolio
Slug: portfolio-engineering-evolution-en
Language: en
Review Status: APPROVED

##### Approved Content

Luís França's portfolio records a trajectory of technical evolution through projects built at different times and exhibiting distinct levels of architecture, process, validation, and operational maturity. The projects are preserved not only to present results, but also to make this evolution visible.

Historical projects, such as the desktop and web task managers and the legacy currency quotation system, record experience with Python, desktop interfaces, web development, file-based persistence, API integration, object-oriented programming, architectural organization, and testing at earlier stages of the trajectory.

More recent projects demonstrate a shift toward more explicit engineering processes. Specification-Driven Development, recorded architectural decisions, traceability, systematic testing, Git as a validation authority, relational databases, controlled deployment, and security practices become part of the construction and evolution of the systems.

Site Portfolio currently constitutes the most complete case of this evolution demonstrated within the portfolio itself. The project progressed through specification, architecture, implementation, testing, validation, UX/UI evolution, design integration, production deployment, and construction of a Knowledge Base with vector retrieval and RAG for IA Jujuju.

Other projects represent different points along this trajectory. The Enterprise Platform has an extensive documentation and architecture baseline with implementation in progress. The Intelligent Currency Platform reassesses a previously explored domain and includes future capabilities that are specified or planned but must not be confused with completed implementation. Legacy projects remain preserved as historical evidence and as references for future modernization cycles.

This composition makes it possible to evaluate professional capability without artificially assigning the same maturity level to every project. The portfolio seeks to show both what was built in the past and how decisions, architecture, quality, security, AI, and production have progressively been addressed in a more systematic engineering process.

#### Evidence / Maturity Notes

POR-001 é uma síntese transversal. Cada afirmação sobre um projeto herda o maturity level e a autoridade das evidências daquele projeto. O conceito não pode utilizar a maturidade do Site Portfólio para elevar retroativamente projetos históricos ou projetos ainda em desenvolvimento.

POR-001 is a cross-project synthesis. Each statement concerning a project inherits the maturity level and authority of that project's evidence. The concept must not use the maturity of Site Portfolio to retroactively elevate historical projects or projects that remain under development.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

## 8. Wave 5 — Retrieval Coverage

Wave 5 contains 1 Knowledge Concept and 2 KnowledgeDocument variants.

Wave 5 uses category:

- GENERAL

All Wave 5 KnowledgeDocument variants are Human Approved.

### KB-GEN-001 — Perguntas Frequentes sobre Luís França e seu Portfólio

#### Metadata

Concept ID: GEN-001
Category: GENERAL
Editorial Version: v1.0
Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

#### PT-BR

Title: Perguntas Frequentes sobre Luís França e seu Portfólio
Slug: professional-faq-pt-br
Language: pt-br
Review Status: APPROVED

##### Approved Content

**Quem é Luís França?**

Luís França é um profissional com trajetória multidisciplinar e atuação em desenvolvimento e engenharia de software. Seu portfólio registra uma evolução desde projetos anteriores em Python até sistemas mais recentes desenvolvidos com processos explícitos de especificação, arquitetura, implementação, testes, validação e deployment.

**Quais são suas principais áreas de engenharia de software?**

Seu trabalho demonstrado no portfólio abrange Python e engenharia backend, arquitetura de software, Specification-Driven Development, APIs e integrações, bancos de dados, testes e qualidade, segurança, deployment e produção, além de aplicações de Inteligência Artificial, LLM e Retrieval-Augmented Generation.

A maturidade dessas competências deve ser avaliada pelas evidências específicas disponíveis em cada projeto, e não apenas pela presença de uma tecnologia ou termo no portfólio.

**Luís trabalha com Python e backend?**

Sim. Python e engenharia backend estão entre as competências demonstradas por seus projetos. O Site Portfólio, por exemplo, utiliza Django em uma arquitetura modular, PostgreSQL para persistência e integrações externas controladas, além de possuir testes e execução em ambiente de produção.

Outros projetos também utilizam Python em diferentes contextos e níveis de maturidade.

**Luís trabalha com arquitetura de software e SDD?**

Sim. Specification-Driven Development é utilizado como processo para relacionar requisitos, decisões, especificações, implementação, testes, evidências e aceite.

No Site Portfólio, esse processo possui evidências que atravessam especificação, implementação, validação e entrega em produção. A Enterprise Platform também possui uma extensa baseline documental e arquitetural orientada por especificações, embora sua implementação permaneça em evolução.

**Luís trabalha com Inteligência Artificial, LLM e RAG?**

Sim, com evidências específicas de implementação e operação no Site Portfólio. A IA Jujuju utiliza uma Knowledge Base própria, embeddings, PostgreSQL com pgvector, recuperação vetorial e Retrieval-Augmented Generation para fornecer contexto controlado ao modelo de linguagem.

Essa evidência não significa que todas as capacidades de IA mencionadas em outros projetos estejam implementadas. Na Intelligent Currency Platform, por exemplo, Machine Learning e Inteligência Artificial permanecem capacidades planejadas no roadmap.

**O que é a IA Jujuju?**

IA Jujuju é a assistente virtual do portfólio profissional de Luís França. Ela utiliza Retrieval-Augmented Generation para recuperar conhecimento autorizado do próprio portfólio antes da geração das respostas.

Sua arquitetura mantém documentos de conhecimento, chunks, embeddings e recuperação vetorial, além de registrar conversas, mensagens e evidências das fontes recuperadas para preservar rastreabilidade.

**Qual projeto demonstra de forma mais completa a engenharia atual de Luís?**

O Site Portfólio constitui atualmente o caso mais completo documentado no próprio portfólio. O projeto percorreu especificação, arquitetura, implementação, testes, validação, evolução de UX/UI, integração com design e implantação em produção. Também incorpora administração, Knowledge Base, recuperação vetorial, RAG e a IA Jujuju.

Isso não significa que todos os projetos do portfólio possuam o mesmo maturity level.

**O Site Portfólio está em produção?**

Sim. Componentes centrais do Site Portfólio possuem evidência real de implantação e operação em produção, incluindo backend, PostgreSQL e o pipeline RAG utilizado pela IA Jujuju.

Entretanto, estados administrativos de encerramento do deployment devem seguir os gates formais do projeto. A existência de componentes operacionais em produção não deve ser utilizada para afirmar que um ciclo de implantação está formalmente encerrado antes de sua certificação final.

**Quais outros projetos fazem parte da trajetória apresentada?**

Além do Site Portfólio, o corpus apresenta a Enterprise Platform, a Intelligent Currency Platform, um sistema legado de cotação de moedas e gerenciadores de tarefas desktop e web.

Esses projetos representam diferentes momentos da trajetória e possuem diferentes níveis de maturidade. A Enterprise Platform está em desenvolvimento, a Intelligent Currency Platform possui especificação e implementação inicial, e os projetos anteriores são preservados como evidência histórica.

**Os projetos legados ainda são relevantes?**

Sim. Eles registram experiências anteriores com Python, aplicações desktop e web, persistência baseada em arquivos, integração com APIs, orientação a objetos, organização arquitetural e testes.

Seu valor no portfólio também está na possibilidade de observar a evolução para processos posteriores com arquitetura mais explícita, SDD, rastreabilidade, bancos relacionais, validação sistemática, segurança e deployment controlado. Isso não autoriza atribuir retroativamente essas práticas modernas aos projetos históricos.

**Como Luís utiliza IA no processo de desenvolvimento?**

No Site Portfólio foi executado um workflow de engenharia assistida por IA sob governança humana. Diferentes ferramentas participaram de atividades de análise, especificação, implementação, refinamento e integração com design, enquanto requisitos, decisões relevantes, auditoria, revisão e aceite permaneceram controlados pelo processo de engenharia e pelo Product Owner.

A evidência documental desse workflow ainda possui uma lacuna específica: a atribuição nominal completa dos papéis das diferentes ferramentas precisa ser consolidada documentalmente antes que esse conceito adquira autoridade documental integral para o RAG.

**Todos os projetos e tecnologias apresentados possuem o mesmo nível de experiência comprovada?**

Não. O portfólio diferencia intenção futura, design, especificação, implementação, validação, produção e evidência histórica. Uma tecnologia listada em roadmap não é tratada como capacidade implementada, assim como a maturidade demonstrada por um projeto não é transferida automaticamente para outro.

Essa distinção é utilizada para manter as respostas da IA Jujuju alinhadas às evidências realmente disponíveis.

#### EN

Title: Frequently Asked Questions about Luís França and His Portfolio
Slug: professional-faq-en
Language: en
Review Status: APPROVED

##### Approved Content

**Who is Luís França?**

Luís França is a professional with a multidisciplinary background working in software development and engineering. His portfolio records an evolution from earlier Python projects to more recent systems developed through explicit processes involving specification, architecture, implementation, testing, validation, and deployment.

**What are his main software-engineering areas?**

His work demonstrated through the portfolio encompasses Python and backend engineering, software architecture, Specification-Driven Development, APIs and integrations, databases, testing and quality, security, deployment and production, as well as applications involving Artificial Intelligence, LLMs, and Retrieval-Augmented Generation.

The maturity of these capabilities must be evaluated through the specific evidence available for each project rather than merely through the presence of a technology or term in the portfolio.

**Does Luís work with Python and backend engineering?**

Yes. Python and backend engineering are among the capabilities demonstrated through his projects. Site Portfolio, for example, uses Django within a modular architecture, PostgreSQL for persistence, and controlled external integrations, together with testing and operation in a production environment.

Other projects also use Python in different contexts and at different maturity levels.

**Does Luís work with software architecture and SDD?**

Yes. Specification-Driven Development is used as a process for connecting requirements, decisions, specifications, implementation, tests, evidence, and acceptance.

In Site Portfolio, this process has evidence spanning specification, implementation, validation, and production delivery. The Enterprise Platform also has an extensive specification-driven documentation and architecture baseline, although its implementation remains in progress.

**Does Luís work with Artificial Intelligence, LLMs, and RAG?**

Yes, with specific implementation and operational evidence in Site Portfolio. IA Jujuju uses its own Knowledge Base, embeddings, PostgreSQL with pgvector, vector retrieval, and Retrieval-Augmented Generation to provide controlled context to the language model.

This evidence does not mean that every AI capability mentioned in other projects has been implemented. In the Intelligent Currency Platform, for example, machine-learning and AI capabilities remain planned roadmap items.

**What is IA Jujuju?**

IA Jujuju is the virtual assistant for Luís França's professional portfolio. It uses Retrieval-Augmented Generation to retrieve authorized knowledge from the portfolio itself before responses are generated.

Its architecture maintains knowledge documents, chunks, embeddings, and vector retrieval, while also recording conversations, messages, and retrieved source evidence to preserve traceability.

**Which project most completely demonstrates Luís's current engineering approach?**

Site Portfolio currently constitutes the most complete case documented within the portfolio itself. The project progressed through specification, architecture, implementation, testing, validation, UX/UI evolution, design integration, and production deployment. It also incorporates administration, a Knowledge Base, vector retrieval, RAG, and IA Jujuju.

This does not mean that every project in the portfolio has the same maturity level.

**Is Site Portfolio in production?**

Yes. Core components of Site Portfolio have real deployment and production-operation evidence, including the backend, PostgreSQL, and the RAG pipeline used by IA Jujuju.

However, administrative deployment-closure states must follow the project's formal gates. The existence of operational production components must not be used to claim that a deployment cycle has been formally closed before its final certification.

**What other projects are part of the trajectory presented in the portfolio?**

In addition to Site Portfolio, the corpus presents the Enterprise Platform, the Intelligent Currency Platform, a legacy currency quotation system, and desktop and web task managers.

These projects represent different stages of the trajectory and have different maturity levels. The Enterprise Platform is under development, the Intelligent Currency Platform has specification and early implementation evidence, and the earlier projects are preserved as historical evidence.

**Are the legacy projects still relevant?**

Yes. They record earlier experience involving Python, desktop and web applications, file-based persistence, API integration, object-oriented programming, architectural organization, and testing.

Their value within the portfolio also lies in showing the evolution toward later processes involving more explicit architecture, SDD, traceability, relational databases, systematic validation, security, and controlled deployment. This does not authorize retroactively assigning those modern practices to the historical projects.

**How does Luís use AI in the software-development process?**

An AI-assisted engineering workflow under human governance was executed in Site Portfolio. Different tools participated in analysis, specification, implementation, refinement, and design-integration activities, while requirements, relevant decisions, auditing, review, and acceptance remained controlled by the engineering process and the Product Owner.

The documentary evidence for this workflow still has a specific gap: complete nominal attribution of the roles of the different tools must be consolidated in project documentation before this concept acquires full documentary authority for RAG.

**Do all projects and technologies presented have the same demonstrated experience level?**

No. The portfolio distinguishes future intention, design, specification, implementation, validation, production, and historical evidence. A technology listed in a roadmap is not treated as an implemented capability, just as maturity demonstrated by one project is not automatically transferred to another.

This distinction is used to keep IA Jujuju's responses aligned with the evidence that is actually available.

#### Evidence / Maturity Notes

GEN-001 é um documento de cobertura e orientação semântica. Ele sintetiza fatos já aprovados nos conceitos especializados do corpus e não cria autoridade independente para novas alegações profissionais.

Cada resposta herda a autoridade e o maturity level dos conceitos aos quais se refere. Em caso de diferença entre uma resposta desta FAQ e um KnowledgeDocument especializado aprovado, o conceito especializado e sua evidência específica devem prevalecer.

A afirmação sobre o workflow assistido por IA preserva o controle de PCS-002: o processo foi executado e aprovado pelo Product Owner, mas permanece DOCUMENTARY CONSOLIDATION REQUIRED antes de adquirir autoridade documental integral para o RAG.

A afirmação sobre produção preserva o controle de ENG-005: componentes comprovados podem ser descritos como production-demonstrated, mas o status global Release 2 Production Deployment: CLOSED não deve ser afirmado enquanto os gates finais permanecerem abertos.

GEN-001 is a semantic-coverage and orientation document. It synthesizes facts already approved in specialized corpus concepts and does not establish independent authority for new professional claims.

Each answer inherits the authority and maturity level of the concepts to which it refers. If a response in this FAQ differs from an approved specialized KnowledgeDocument, the specialized concept and its specific evidence must prevail.

The statement concerning the AI-assisted workflow preserves the PCS-002 control: the process was executed and approved by the Product Owner but remains DOCUMENTARY CONSOLIDATION REQUIRED before acquiring full documentary authority for RAG.

The production statement preserves the ENG-005 control: demonstrated components may be described as production-demonstrated, but the overall status Release 2 Production Deployment: CLOSED must not be asserted while the final gates remain open.

#### Approval

Human Review: APPROVED
Editorial Baseline: APPROVED

## 9. Wave 1 Traceability Matrix

| ID | Category | PT-BR | EN | CER-01 | Maturity | Equivalence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KB-PRF-001 | PROFILE | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-PRF-002 | PROFILE | Approved v1.1 | Approved v1.1 | PASS | PASS | PASS | APPROVED |
| KB-EXP-001 | EXPERIENCE | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-001 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-002 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-003 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-004 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |

## 10. Wave 4 Traceability Matrix

| ID | Category | PT-BR | EN | CER-01 | Maturity | Equivalence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KB-PRJ-007 | PROJECT | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-PRJ-008 | PROJECT | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-PRJ-009 | PROJECT | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-PRJ-010 | PROJECT | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-PRJ-011 | PROJECT | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-POR-001 | PORTFOLIO | Approved | Approved | PASS | PASS | PASS | APPROVED |

## 11. Wave 5 Traceability Matrix

| ID | Category | PT-BR | EN | CER-01 | Maturity | Equivalence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KB-GEN-001 | GENERAL | Approved | Approved | PASS | PASS | PASS | APPROVED |

## 12. Retrieval Acceptance Intent

The approved corpus must later support questions concerning:

- professional profile;
- multidisciplinary background;
- professional experience;
- Python/backend engineering;
- software architecture;
- Specification-Driven Development;
- testing and quality;
- production delivery;
- AI/LLM application engineering;
- RAG;
- embeddings;
- vector retrieval;
- evidence supporting professional capabilities.

Negative-boundary validation intent includes ensuring that the assistant does not incorrectly claim:

- foundation-model training experience;
- implemented roadmap capabilities;
- production maturity for projects that have not reached production;
- equal maturity across all listed technologies;
- SDD maturity retrospectively for historical projects.

These are validation intentions only. Retrieval tests have not yet been executed against this baseline.

## 13. Approval and Change Control

- Wave 1 editorial content is Human Approved.
- Wave 2 editorial content is Human Approved.
- Wave 3 editorial content is Human Approved.
- Wave 4 editorial content is Human Approved.
- Wave 5 editorial content is Human Approved.
- The baseline is immutable except through an explicit reviewed revision.
- Future content changes require a new editorial revision.
- Materialization into Django must preserve the approved content.
- Database persistence does not authorize editorial rewriting.
- Reindexing does not authorize editorial rewriting.
- Translation changes require factual-equivalence review.
- Maturity changes require new supporting evidence.
- Capability-strength changes require CER-01 reassessment.

PCS-002 remains APPROVED — DOCUMENTARY CONSOLIDATION REQUIRED until its documentary gap is resolved.
