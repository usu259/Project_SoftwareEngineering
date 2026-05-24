# Software Requirements Specification

## For Simple Billing Application

Version 0.1

Prepared by Luca Rosenberg, Andrea Usuelli and Willi Zeltner

for "Software Engineering and Design Patterns" at ZHAW Life Sciences

graded by Dr. Ahmad Aghaebrahimian

25.05.2026


## Table of Contents

<!-- TOC -->
- [Software Requirements Specification](#software-requirements-specification)
  - [For Simple Billing Application](#for-simple-billing-application)
  - [Table of Contents](#table-of-contents)
  - [Revision History](#revision-history)
  - [1. Introduction](#1-introduction)
    - [1.1 Document Purpose](#11-document-purpose)
    - [1.2 Product Scope](#12-product-scope)
    - [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
    - [1.4 Project Organisation](#14-project-organisation)
    - [1.5 References](#15-references)
    - [1.6 Document Overview](#16-document-overview)
  - [2. Product Overview](#2-product-overview)
    - [2.1 Product Perspective](#21-product-perspective)
    - [2.2 Product Functions](#22-product-functions)
    - [2.3 Product Constraints](#23-product-constraints)
    - [2.4 User Characteristics](#24-user-characteristics)
    - [2.5 Assumptions and Dependencies](#25-assumptions-and-dependencies)
  - [3. Main Features](#3-main-features)
    - [3.1 Reporting Work](#31-reporting-work)
    - [3.2 Creating Invoices](#32-creating-invoices)
    - [3.3 Managing Stem Data](#33-managing-stem-data)
  - [4. External Interfaces](#4-external-interfaces)
    - [4.1 User Interfaces](#41-user-interfaces)
    - [4.2 Hardware Interfaces](#42-hardware-interfaces)
    - [4.3 Software Interfaces](#43-software-interfaces)
  - [5. Further Non-Functional Requirements](#5-further-non-functional-requirements)
    - [5.1 Design and Implementation](#51-design-and-implementation)
      - [5.1.1 Architecture](#511-architecture)
      - [5.1.2 Database](#512-database)
      - [5.1.3 Distribution](#513-distribution)
      - [5.1.4 Proof of Concept and Deadline](#514-proof-of-concept-and-deadline)
      - [5.1.5 Change Management](#515-change-management)
    - [5.2 Quality of Service](#52-quality-of-service)
      - [5.2.1 Performance](#521-performance)
      - [5.2.2 Security](#522-security)
    - [5.3 AI/ML](#53-aiml)
  - [6. Verification](#6-verification)
    - [6.1 Verification Environment](#61-verification-environment)
    - [Appendix A: Analysis Models](#appendix-a-analysis-models)
    - [Appendix B: Architecture Models](#appendix-b-architecture-models)
    - [Appendix C: User Interface Mockups](#appendix-c-user-interface-mockups)
<!-- TOC -->

---

## Revision History

| Name                                            | Date       | Reason for Change | Version |
| ----------------------------------------------- | ---------- | ----------------- | ------- |
| Luca Rosenberg, Andrea Usuelli, Willi Zeltner  | 2026-03-19 | Initial version   | 0.1     |

---

## 1. Introduction

This application is a streamlined work reporting system designed for simplicity and ease of use. Its primary purpose is to allow workers (end-users) to document completed tasks associated with specific projects or customers. Administrative users can then aggregate these reports to generate accurate invoices.

While many market alternatives offer complex workflows, this application intentionally prioritises a minimal feature set to reduce cognitive overhead and ensure high adoption rates among field staff. This document also outlines out-of-scope concepts and future considerations to provide a comprehensive roadmap without compromising the initial goal of simplicity.


### 1.1 Document Purpose

This Software Requirements Specification (SRS) defines the functional and non-functional requirements for a streamlined work reporting and automated invoicing application. Its primary objectives are to provide a clear technical roadmap for developers and testers, to serve as a project baseline for the student group, and to act as a formal evaluation document for the course supervisor. Some chapters therefore extend beyond the standard IEEE SRS guidelines to meet course-specific requirements.

### 1.2 Product Scope

The application, hereafter referred to as "the System," facilitates the logging of labour and material usage into digital work reports and automates the aggregation of those reports into professional invoices, thereby reducing manual billing errors.

**Exclusions:** In its current iteration, the System intentionally excludes authentication and login modules, advanced administrative configuration, and a dedicated portal for external customers. These are considered out of scope in order to deliver a lightweight, focused MVP (Minimum Viable Product).


### 1.3 Definitions, Acronyms, and Abbreviations

| Term        | Definition                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------- |
| API         | Application Programming Interface – a set of definitions and protocols for building and integrating application software.       |
| AI/ML       | Artificial Intelligence / Machine Learning – techniques that enable systems to learn from data or perform tasks that typically require human reasoning. |
| Invoice     | A billing document generated by aggregating one or more work reports for a specific project or customer.                        |
| MVP         | Minimum Viable Product – a version of a product with just enough features to be usable by early adopters.                      |
| ORM         | Object-Relational Mapper – a library that translates between object-oriented code and relational database tables.               |
| SRS         | Software Requirements Specification – this document; describes the intended purpose and nature of the software.                 |
| Stem Data   | A centralised catalogue of available personnel, hourly rates, and material items available for selection in reports.            |
| UI          | User Interface – the visual elements through which a user interacts with the software.                                          |
| Work Report | A digital record documenting specific completed tasks, including time spent and materials used.                                 |

### 1.4 Project Organisation

This project is carried out by three students in the Master in Life Sciences programme at ZHAW in Wädenswil. It forms part of the final grade in the course "Software Engineering and Design Patterns" and is supervised by Dr. Ahmad Aghaebrahimian.

| Team Member     | Scrum Role                          | Project Role |
| --------------- | ----------------------------------- | ------------ |
| Luca Rosenberg | Development, Software Architecture  | define software architecture and help implement it |
| Andrea Usuelli  | Development, Testing                | full stack implementation and design of unit tests |
| Willi Zeltner   | Product Owner                       | write software documentation and software requirements, test functional requirements |

### 1.5 References

The following documents and standards provide additional context for this SRS:

- ISO/IEC/IEEE 29148:2018, Systems and software engineering — Life cycle processes — Requirements engineering. Informative.
- Percival, H. J. W. and Gregory, B. _Architecture Patterns with Python: Enabling Test-Driven Development, Domain-Driven Design, and Event-Driven Microservices._ 2nd ed., O'Reilly, 2020.

### 1.6 Document Overview

This SRS is organised into six sections. Following this Introduction, **Section 2** provides a high-level view of product functions and user characteristics. **Section 3** details the core functional requirements, grouped by feature area. **Section 4** defines external interface requirements covering UI, hardware, and software integrations. **Section 5** addresses further non-functional requirements including architecture, database, and quality of service. **Section 6** defines the verification approach and environment. All figures and models can be found in the **Appendices** at the end of the document.

## 2. Product Overview

### 2.1 Product Perspective

The market for work reporting tools is saturated with feature-rich, complex applications that often overwhelm small teams with unnecessary functionality and come at considerable cost. Many also rely on proprietary cloud storage, making direct data access difficult.

This application is a lightweight alternative specifically tailored for small companies with one to five employees. Although the initial release is intentionally simple, the System's architecture must remain modular to allow for future standalone extensions or integration into larger ecosystems.

### 2.2 Product Functions

The System's core functionality covers the complete workflow from labour documentation to billing:

- **Work Documentation**: Workers can create, view, and edit daily reports linked to specific customers or projects.
- **Report Management**: Accountants can review and modify all worker reports to ensure data integrity before billing.
- **Automated Invoicing**: Accountants can aggregate one or more reports into a single, professional invoice.
- **Stem Data Utilisation**: All users can draw from a predefined catalogue of materials and human resources to ensure consistency.

### 2.3 Product Constraints

The following constraints are mandatory for project success and compliance:

- **Open Source**: The application must be developed as open-source software and hosted on a public repository (e.g., GitHub).
- **Data Sovereignty**: The stem must support direct database access for administrative tasks.
- **Minimalist UI**: The interface must allow a worker to complete a standard work report entry in no more than three interactions.
- **Timeline**: Development is strictly limited to the duration of the Software Engineering and Design Patterns course in semester SS 2026.

### 2.4 User Characteristics

**Worker (_End-User_)**

| Attribute   | Description                                                                                                                                                                                                          |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Profile     | Moderate IT skills. Primary goal is fast data entry under field conditions.                                                                                                                                          |
| Device      | Primarily mobile devices (smartphones).                                                                                                                                                                              |
| Access      | Can create and edit their own reports. Edit access is revoked once a report has been included in a billed invoice.                                                                                                   |
| Needs       | High performance and offline-first capabilities to prevent frustration on site.                                                                                                                                      |
| Permissions | Can view customers and the stem catalogue but cannot edit them. May add free-text positions for unique items not found in the stem. Unit prices for human resources are hidden to preserve confidentiality.           |

**Accountant (_Administrative User_)**

| Attribute   | Description                                                                                                          |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| Profile     | Intermediate IT skills. Focuses on data accuracy and financial output.                                               |
| Device      | Primarily desktop systems with large displays.                                                                       |
| Access      | Full visibility of all worker reports, grouped by project or customer.                                               |
| Needs       | Bulk editing capabilities and clear status indicators (e.g., Billed vs. Unbilled).                                  |
| Permissions | Can override any report data prior to invoicing and trigger the automated invoice generation process.                |

### 2.5 Assumptions and Dependencies

- **Database-Level Administration**: Stem data (personnel rates, material costs) will be managed directly at the database level by a System Administrator. No UI for these tasks is required in this version.
- **Finalisation Logic**: To maintain data integrity, a report is considered locked and uneditable by a worker once it has been submitted or flagged for invoicing.
- **Environment**: The project assumes a stable, web-standard deployment environment. Specific technology stack decisions remain pending.

## 3. Main Features

The functional requirements are divided into two main feature areas corresponding to the use cases for _workers_ and _accountants_ (see _Appendix A, Figure 1_).

Both features rely on the same domain model, whose main entities are:

- **Employees** – workers for whom hours can be reported
- **Customers** – recipients of work reports and invoices
- **Work Reports**
- **Work Report Positions**
- **Invoices**

All of these entities must be present in the MVP. A detailed class diagram with relationships is provided in _Appendix A (Figure 3)_.

### 3.1 Reporting Work

The core of this feature is the creation of **work reports** `REQ-FUNC-001`. A report is created by an **employee** and addressed to a **customer**; **work report positions** can then be added to it `REQ-FUNC-003`. Both the report header and its positions remain editable `REQ-FUNC-002` `REQ-FUNC-004` as long as the report has not been included in a billed **invoice**. Reports that are no longer needed can be soft-deleted `REQ-FUNC-005`.

_High Priority (MVP)_

> **`REQ-FUNC-001`** _(New Report)_ A worker can create a new report and associate it with a customer and an employee.

> **`REQ-FUNC-002`** _(Edit Report)_ A worker can open an editable report and update the associated customer and employee.

> **`REQ-FUNC-003`** _(Add Report Position)_ A worker can open an editable report and add a work report position.

> **`REQ-FUNC-004`** _(Edit Report Position)_ A worker can open an editable report and update existing work report positions.

> **`REQ-FUNC-005`** _(Delete Report)_ A worker can soft-delete an editable report.

_Low Priority_

> **`REQ-FUNC-006`** _(Stem Integration)_ A worker can select between material, personnel, and free-text position types when adding work report positions. Material and personnel positions are drawn from the stem data catalogue.

> **`REQ-FUNC-007`** _(Work Hours Summary)_ A worker can view a summary of reported hours aggregated by day, week, and month.

### 3.2 Creating Invoices

The core of this feature is the creation of **invoices** `REQ-FUNC-011`. An invoice is addressed to a **customer** and consolidates the work report positions from one or more **work reports** belonging to that same customer `REQ-FUNC-013`. The associated work reports and customer can be updated after initial creation `REQ-FUNC-012` `REQ-FUNC-014`. Once the invoice is complete, it can be downloaded as a PDF `REQ-FUNC-015` and its status set to "Billed" or "Paid" `REQ-FUNC-016`, at which point the constituent work reports become locked `REQ-FUNC-017`. Invoices that are no longer needed can be soft-deleted `REQ-FUNC-018`.

_High Priority (MVP)_

> **`REQ-FUNC-010`** _(Basic Accountant Requirments)_ All requirements `REQ-FUNC-001` through `REQ-FUNC-006` are also available to accountants.

> **`REQ-FUNC-011`** _(Add Invoice)_ An accountant can create a new invoice and associate it with a customer.

> **`REQ-FUNC-012`** _(Edit Invoice)_ An accountant can open an invoice and update the associated customer.

> **`REQ-FUNC-013`** _(Add Report to Invoice)_ An accountant can open an invoice and add work reports associated with the same customer, provided those reports have not already been included in another invoice.

> **`REQ-FUNC-014`** _(Add Report at Invoice)_ An accountant can open an invoice and update the associated work reports.

> **`REQ-FUNC-015`** _(Invoice PDF Export)_ An accountant can open an invoice and download a PDF version of it.

> **`REQ-FUNC-016`** _(Invoice Status)_ An accountant can open an invoice and set its status to "Billed" or "Paid".

> **`REQ-FUNC-017`** _(Status Lock)_ Work reports associated with an invoice whose status is "Billed" or "Paid" are no longer editable.

> **`REQ-FUNC-018`** _(Delete Invoice)_ An accountant can soft-delete an invoice.

### 3.3 Managing Stem Data

This feature is out of scope for the MVP. However, the requirements listed below must be taken into account during MVP implementation to ensure the data model and architecture remain compatible with this future feature.

The stem catalogue is managed by a system administrator, who can add `REQ-FUNC-020` and update `REQ-FUNC-021` material and personnel items. To maintain consistency in historical records, updates create a new version of the item rather than overwriting the original. The catalogue can be exported and imported as CSV files `REQ-FUNC-022` `REQ-FUNC-023` to support bulk administration.

_High Priority_

> **`REQ-FUNC-020`** _(Add Stem Item)_ A system administrator can add material and personnel items to the stem catalogue.

> **`REQ-FUNC-021`** _(Update Stem Item)_ A system administrator can update existing stem data. An update creates a new version of the item, leaving prior entries in work reports and invoices unchanged to preserve data integrity.

> **`REQ-FUNC-022`** _(Export Stem as CSV)_ A system administrator can export the stem catalogue as a CSV file.

> **`REQ-FUNC-023`** _(Import CSV to Stem)_ A system administrator can import new stem items from a CSV file.

_Low Priority_

> **`REQ-FUNC-024`** _(Statistics)_ A system administrator and an accountant can access usage statistics for stem items across work reports and invoices.

## 4. External Interfaces

### 4.1 User Interfaces

As described in Sections 2.3 and 2.4, the user interface must be kept simple and optimised for rapid completion of primary tasks. The Worker UI targets smartphone viewports `UI-001`, while the Accountant and Administrator UI targets desktop viewports `UI-002`. Both roles require that core workflows are reachable within three interactions from the dashboard `UI-003` `UI-005`. Mockups and wireframes are provided in _Appendix C_.

> **`UI-001`** _(Mobile Worker Design)_ The System shall employ responsive web design optimised for viewport widths of 375 px to 430 px (standard smartphones) for the Worker role.

> **`UI-002`** _(Desktop Accountant Design)_ The System shall employ responsive web design optimised for a viewport width of 1440 px (standard notebook) for the Accountant and Administrator roles.

> **`UI-003`** _(Work Report Access)_ A work report must be creatable within three taps from the dashboard. Work report positions must be addable within three taps from the report overview.

> **`UI-004`** _(Report Dashboard)_ The dashboard shall display the most recent reports requiring attention and the status of the latest sent invoices.

> **`UI-005`** _(Invoice Access)_ An invoice must be creatable within three clicks from the dashboard. Work reports to be billed must be addable within three clicks from the invoice overview.

> **`UI-006`** _(Export Action)_ A downloadable PDF version of an invoice shall be generatable with a single click, based on a predefined template (see `REQ-FUNC-015`).

### 4.2 Hardware Interfaces

There are no hardware interface requirements for this release.

### 4.3 Software Interfaces

> **`INT-001`** _(PDF Generation)_ The System shall integrate with a PDF generation library to transform aggregated report data into a standardised invoice format.

> **`INT-002`** _(Database ORM)_ The System shall interface with a relational database via an ORM layer to ensure data persistence and support direct admin-level queries.

## 5. Further Non-Functional Requirements

### 5.1 Design and Implementation

#### 5.1.1 Architecture

The System follows a client–server architecture `IMP-001` with a strict separation between the frontend and the backend. The backend is structured according to Domain-Driven Design (DDD) `IMP-002`, organising the codebase around the core business concepts — work reports, invoices, customers, and employees — rather than technical layers alone. Data access and business logic are further decoupled through a service and repository pattern `IMP-003`.

These choices are deliberate, even if they may exceed the immediate demands of an MVP. A client–server split enables the frontend and backend to evolve independently, supporting future replacement or extension of either layer without affecting the other. DDD ensures that the domain model remains the authoritative source of truth for business rules, making the codebase easier to reason about as the System grows. The service and repository pattern makes individual components testable in isolation, directly supporting the 70% test-coverage target (`REQ-MAINT-001`, see Section 5.2), and allows the underlying database to be swapped without touching business logic — relevant given the planned migration from SQLite to PostgreSQL (see Section 5.1.2). Collectively, these patterns reflect the architectural principles studied in the course (Percival & Gregory, 2020) and provide a solid foundation for the extensions described in Section 3.3.

Some of the following requirements may therefore appear to go beyond what is strictly necessary for the MVP, but they are included to ensure long-term reliability and maintainability.

> **`IMP-001`** _(Client–Server Model)_ The System shall follow a client–server architecture with a clear separation between the frontend and backend.

> **`IMP-002`** _(Domain-Driven Design)_ The System shall be implemented using Domain-Driven Design (DDD).

> **`IMP-003`** _(Services and Repositories)_ The System shall use a service and repository pattern to manage data access and business logic.

#### 5.1.2 Database

The proof-of-concept uses SQLite as its database, and PostgreSQL is planned for production. This choice reflects several converging considerations.

The System's data — work reports, positions, invoices, customers, and employees — is inherently structured and relational, with well-defined relationships and no unstructured or variable-schema content. A relational database is therefore the natural fit. Both SQLite and PostgreSQL are open-source and free of licensing cost, which aligns with the open-source constraint in Section 2.3 and the free-tier deployment requirement `REQ-DEAD-001`. SQLite requires zero configuration and is ideal during development and for the PoC, while PostgreSQL provides the ACID compliance, concurrent write support, and production-grade reliability needed for a deployed system. The transition between the two is made straightforward by the ORM layer (`INT-002`), which abstracts the database dialect and allows the same model and query code to run against either backend. PostgreSQL is also natively supported by all major free-tier hosting providers (e.g., Render, Railway), making it compatible with the cost constraints of this project.

#### 5.1.3 Distribution

The source code is hosted on [GitHub](https://github.com/usu259/Project_SoftwareEngineering) in a private repository. Public access is not planned at this time.

Since the product owner is part of the development team and production usage is uncertain at this stage, continuous integration and deployment (CI/CD) is not planned for the current release.

> **`IMP-004`** _(Distribution)_ The source code shall be accessible on GitHub. The latest commit on the main branch shall always represent a working version of the application.

#### 5.1.4 Proof of Concept and Deadline

> **`REQ-DEAD-001`** A functional proof of concept demonstrating the end-to-end flow from work report creation to invoice generation must be ready for the mid-semester review (date: 25.05.2026).

#### 5.1.5 Change Management

Change management requirements have not yet been specified. Future iterations should define change categories (breaking, additive, bugfix), approval workflows, and required artefacts such as changelogs, migration guides, and release notes. Backward and forward compatibility guarantees, deprecation timelines, and rollout and rollback procedures should also be addressed.


### 5.2 Quality of Service

#### 5.2.1 Performance

Performance requirements are assigned lower priority for the MVP, as functional correctness takes precedence. Nevertheless, two baseline targets are defined to ensure the System remains usable in the field.

> **`REQ-PERF-001`** The System shall load the stem selection list (up to 500 items) in under 500 ms under standard 4G network conditions.

> **`REQ-PERF-002`** PDF invoice generation shall complete within 3 seconds of the accountant's request.

#### 5.2.2 Security

As noted in Section 1.2, authentication is out of scope at this stage. The following requirements address fundamental data integrity and confidentiality concerns that must be present even in the MVP.

> **`REQ-SEC-001`** _(Data Integrity)_ The System shall use parameterised queries for all database interactions to prevent SQL injection.

> **`REQ-SEC-002`** _(Soft Deletes)_ All delete actions shall be implemented as soft deletes. Updates to stem items shall produce a new version of the item, preserving consistency in existing reports.

An implementation of user authentication at a later stage would also enable role-based access control:

> **`REQ-SEC-003`** _(Role Privacy)_ The System shall filter stem data in the Worker view to exclude unit costs and profit margins.

### 5.3 AI/ML

The System does not incorporate AI or ML components, and this is a deliberate design decision rather than an oversight.

The core workflows — logging hours and materials, aggregating report positions into an invoice, and computing totals — are fully deterministic and rule-based. Every billing calculation can be expressed as a precise arithmetic formula, and every workflow step follows a defined sequence of user actions. There is no unstructured input, no pattern that needs to be learned from historical data, and no ambiguity that a model would need to resolve. Introducing AI/ML in this context would add infrastructure complexity (model serving, data pipelines, versioning, monitoring) and maintenance overhead without providing any functional benefit that cannot be achieved more reliably with simple conditional logic.

Beyond the technical argument, the target users are field workers and accountants in small companies who prioritise predictability and transparency. A billing system that produces deterministic, auditable results is more appropriate in this context than one that relies on probabilistic inference. Any unexpected output from a model — however rare — would undermine trust in a financial tool.

One area where AI/ML could plausibly add value in a future release is automated text recognition of physical receipts or delivery notes, allowing workers to scan a document and pre-populate a work report position rather than entering data manually. This capability is noted in the project roadmap but is explicitly out of scope for the current version.
## 6. Verification

This section outlines the objective evidence required to confirm that each requirement has been satisfied. The primary verification methods are **Test** (automated or manual execution), **Analysis** (evaluation of code or logic), and **Demonstration** (walkthrough with a stakeholder).

| Requirement ID   | Title                                    | Verification Method | Test / Artefact Link                                    | Status  | Evidence                |
| :--------------- | :--------------------------------------- | :------------------ | :------------------------------------------------------ | :------ | :---------------------- |
| `REQ-FUNC-001`   | Create work report                       | Test                | `tests/ui_worker_report.py`                             | Pending | Test run report         |
| `REQ-FUNC-002`   | Update report customer / employee        | Test                | `tests/ui_worker_report.py`                             | Pending | Test run report         |
| `REQ-FUNC-003`   | Add work report position                 | Test                | `tests/unit_report_logic.py`                            | Pending | Test run report         |
| `REQ-FUNC-004`   | Update work report positions             | Test                | `tests/unit_report_logic.py`                            | Pending | Test run report         |
| `REQ-FUNC-005`   | Soft-delete report                       | Test                | `tests/unit_report_logic.py`                            | Pending | Test run report         |
| `REQ-FUNC-006`   | Position type selection (stem / text)    | Test                | `tests/unit_report_logic.py`                            | Pending | Test run report         |
| `REQ-FUNC-007`   | Hours summary (day / week / month)       | Test                | `tests/unit_report_logic.py`                            | Pending | Test run report         |
| `REQ-FUNC-010`   | Accountant access to worker features     | Test                | `tests/ui_accountant.py`                                | Pending | Test run report         |
| `REQ-FUNC-011`   | Create invoice                           | Test                | `tests/ui_accountant.py`                                | Pending | Test run report         |
| `REQ-FUNC-012`   | Update invoice customer                  | Test                | `tests/ui_accountant.py`                                | Pending | Test run report         |
| `REQ-FUNC-013`   | Add work reports to invoice              | Test                | `tests/unit_invoice_logic.py`                           | Pending | Test run report         |
| `REQ-FUNC-014`   | Update work reports on invoice           | Test                | `tests/unit_invoice_logic.py`                           | Pending | Test run report         |
| `REQ-FUNC-015`   | Download invoice as PDF                  | Demonstration       | `docs/demo_scripts/billing.md`                          | Pending | Signed demo log         |
| `REQ-FUNC-016`   | Set invoice status (Billed / Paid)       | Test                | `tests/unit_invoice_logic.py`                           | Pending | Test run report         |
| `REQ-FUNC-017`   | Edit lock on billed reports              | Analysis            | `src/middleware/lock.py`                                | Pending | Code review summary     |
| `REQ-FUNC-018`   | Soft-delete invoice                      | Test                | `tests/unit_invoice_logic.py`                           | Pending | Test run report         |
| `REQ-FUNC-020`   | Admin: add stem items                    | Demonstration       | `docs/demo_scripts/stem.md`                             | Pending | Signed demo log         |
| `REQ-FUNC-021`   | Admin: update stem items (versioning)    | Analysis            | `src/domain/stem.py`                                    | Pending | Code review summary     |
| `REQ-FUNC-022`   | Admin: export stem as CSV                | Test                | `tests/unit_stem_logic.py`                              | Pending | Test run report         |
| `REQ-FUNC-023`   | Admin: import stem from CSV              | Test                | `tests/unit_stem_logic.py`                              | Pending | Test run report         |
| `REQ-FUNC-024`   | Stem usage statistics                    | Demonstration       | `docs/demo_scripts/stats.md`                            | Pending | Signed demo log         |
| `REQ-PERF-001`   | Stem list load time < 500 ms             | Test (Manual)       | `tests/performance_metrics.xlsx`                        | Pending | Browser DevTools log    |
| `REQ-PERF-002`   | PDF generation < 3 s                     | Test (Manual)       | `tests/performance_metrics.xlsx`                        | Pending | Browser DevTools log    |
| `REQ-SEC-001`    | Parameterised queries (SQL injection)    | Analysis            | `docs/security/threat_model.md`                         | WIP     | Static analysis report  |
| `REQ-SEC-002`    | Soft deletes and stem versioning         | Analysis            | `src/domain/`                                           | Pending | Code review summary     |
| `REQ-SEC-003`    | Role privacy (hide unit prices)          | Inspection          | `src/views/worker_view.py`                              | Pending | Screenshot of UI        |
| `IMP-001`        | Client–server architecture               | Analysis            | `docs/architecture/overview.md`                         | Pending | Architecture review     |
| `IMP-002`        | Domain-Driven Design                     | Analysis            | `src/domain/`                                           | Pending | Code review summary     |
| `IMP-003`        | Service and repository pattern           | Analysis            | `src/services/`, `src/repositories/`                    | Pending | Code review summary     |
| `IMP-004`        | GitHub main branch always deployable     | Demonstration       | `https://github.com/usu259/Project_SoftwareEngineering` | Pending | Live branch access      |
| `REQ-DEAD-001`   | Mid-semester proof of concept            | Demonstration       | `docs/milestones/poc_v1.md`                             | Pending | Presentation slides     |

### 6.1 Verification Environment

- **Development:** Localhost (Python environment).
- **Staging:** Private repository, local testing.
- **Database:** SQLite for local testing.
- **Tools:** PyTest for logic testing.

---

### Appendix A: Analysis Models

The models below can also be found in the GitHub repository under `documentation/diagrams`.

![Use Case diagram](../diagrams/use-case.png)

_Figure 1_: Use Case diagram. The relevant actors are the worker and the accountant.

![Sequence diagram](../diagrams/sequence.png)

_Figure 2_: Sequence diagram. Divided between worker and accountant workflows.

![Class diagram](../diagrams/class.png)

_Figure 3_: Base classes identified. This model excludes service and repository classes as well as API routes.

![Activity diagram](../diagrams/activity.png)

_Figure 4_: Activity diagram.

### Appendix B: Architecture Models


![Database diagram](../diagrams/architecture.jpg)

_Figure 5_: Architecture design.

![Database diagram](../diagrams/domain_drive_design.jpg)

_Figure 6_: Simplified version of domain driven design. This can be extented for every domain class displayed in _Figure 3 (Appendix A)_

![Database diagram](../diagrams/database_er.png)
_Figure 7_: Entity relation diagram.


### Appendix C: User Interface Mockups

![GUI Mockup 1](../diagrams/gui_mockup_1.png)

_Figure 8_: Mockup for the worker UI when adding a new report. Smaller frames represent individual position entries to be added to a work report.

![GUI Mockup 2](../diagrams/gui_mockup_2.png)

_Figure 9_: Mockup for the accountant UI when generating a new invoice. Shows an overview of relevant positions and reports, the invoice total, and the action buttons.
