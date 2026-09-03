# KNOWLEDGE-CONTENT-BASELINE-001

Document-ID: KNOWLEDGE-CONTENT-BASELINE-001
Version: 1.0.0
Status: HUMAN APPROVED
Scope: Wave 1 — Core Professional Authority
Knowledge Concepts: 7
KnowledgeDocuments: 14

Languages:

- pt-br
- en

Operational state:

Persistence Status: NOT STARTED
Indexing Status: NOT STARTED
Retrieval Validation: NOT STARTED
Grounded Answer Validation: NOT STARTED

## 1. Purpose

KNOWLEDGE-CONTENT-BASELINE-001 is the authoritative, version-controlled editorial baseline for the approved Wave 1 Knowledge Content of IA Jujuju.

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

Title: Site Portfólio — Production Delivery
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

## 6. Wave 1 Traceability Matrix

| ID | Category | PT-BR | EN | CER-01 | Maturity | Equivalence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KB-PRF-001 | PROFILE | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-PRF-002 | PROFILE | Approved v1.1 | Approved v1.1 | PASS | PASS | PASS | APPROVED |
| KB-EXP-001 | EXPERIENCE | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-001 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-002 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-003 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |
| KB-SKL-004 | SKILL | Approved | Approved | PASS | PASS | PASS | APPROVED |

## 7. Retrieval Acceptance Intent

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

## 8. Approval and Change Control

- Wave 1 editorial content is Human Approved.
- The baseline is immutable except through an explicit reviewed revision.
- Future content changes require a new editorial revision.
- Materialization into Django must preserve the approved content.
- Database persistence does not authorize editorial rewriting.
- Reindexing does not authorize editorial rewriting.
- Translation changes require factual-equivalence review.
- Maturity changes require new supporting evidence.
- Capability-strength changes require CER-01 reassessment.

Future Waves may extend this baseline through controlled revisions. No future Wave is marked as approved in this document.
