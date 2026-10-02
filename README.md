# Faculty Research Grant & Publication Tracker

[![Architecture UML 2.5](https://img.shields.io/badge/Architecture-UML%202.5%20Component-blue.svg)](2-Architectural-Diagram/)
[![Requirements Engineering](https://img.shields.io/badge/Requirements-IEEE%20830-success.svg)](1-RE/)
[![Security & Ledger](https://img.shields.io/badge/Audit%20Ledger-SHA--256%20Merkle%20Chained-orange.svg)](1-RE/RE_Document.md#nfr-001-immutable-tamper-evident-financial-audit-ledger)
[![Verification](https://img.shields.io/badge/RTM-100%25%20Traceability-brightgreen.svg)](1-RE/RE_Document.md#5-requirements-traceability-matrix-rtm)

> **Individual Project Submission**  
> **Course:** Software Engineering (Lab 3)  
> **Problem Statement #09:** Faculty Research Grant & Publication Tracker  
> **Student Name:** Madhav Vinod  
> **USN:** PES1UG24CS254  
> **Target Organization:** Academic Deanery of Research & Development  

---

## 1. Problem Context & Overview

Higher education and research institutions manage millions in sponsored research grants across diverse funding agencies (e.g., DST, SERB, DRDO, NSF, Industry). The research deanery currently struggles with manual, error-prone workflows:
- **Financial Overdrafts & Unmonitored Burn Rates**: PIs inadvertently overspend specific budget categories (e.g., equipment procurement), or project funds lapse before project milestones are reached.
- **Manual Publication Tracking**: Citations, journal quartiles (Q1-Q4), and indexing status (Scopus, SCI, Web of Science) are manually aggregated, introducing delays and errors into national ranking (NIRF, NAAC) filings.
- **Authorship Conflicts**: Co-author consent is tracked informally, resulting in delays, retracted manuscripts, and attribution disputes.
- **Audit Vulnerabilities**: Financial and publication records lack cryptographic tamper-evidence, exposing institutions during statutory funding audits.

The **Faculty Research Grant & Publication Tracker** provides an automated portal combining real-time budget cap validation, automated citation sync, multi-party digital co-author signoff, fund burn-up analytics, and a SHA-256 tamper-evident financial audit ledger.

---

## 2. Target Stakeholders & Primary Actors

| Actor | Role | Key Interactions |
| :--- | :--- | :--- |
| **Faculty Researcher (PI / Co-PI)** | Primary End-User | Submits grant proposals, logs equipment procurement expenses with quotes/invoices, tracks remaining balances, registers manuscript DOIs, and reviews co-authorship requests. |
| **Research Dean** | Executive Administrator | Reviews and endorses grant proposals, authorizes emergency budget cap overrides, releases milestone tranches, reviews burn-up trajectories, and audits ledger records. |
| **Co-Authors (Internal & External)** | Collaborator | Receive secure, time-limited cryptographic tokens to review manuscript drafts, affirm authorship sequence, and record digital consent. |
| **External Indexing APIs** | External Service | Scopus, Web of Science, and CrossRef REST APIs providing citation metrics, DOI metadata, and quartile ratings. |

---

## 3. System Architecture & Component Model

The portal architecture follows a modular, service-oriented component design using **UML 2.5 Component & Assembly (Ball-and-Socket) notation**.

![Faculty Research Grant & Publication Tracker Architecture](2-Architectural-Diagram/architecture_diagram.png)

### Architectural Components Summary:
1. **Faculty Portal** (`Faculty Portal`): Web console for faculty to file expense claims, submit paper metadata, and monitor personal grants.
2. **Grant & Fund Service** (`Grant & Fund Service`): Central domain orchestrator enforcing budget caps, validating expense limits, and executing financial business rules.
3. **Dean Console** (`Dean Console`): Administrative dashboard for grant approvals, budget cap overrides, and institutional governance.
4. **Publication Engine** (`Publication Engine`): Manages scholarly outputs, matches papers to grants, and computes citation metrics.
5. **Grant & Audit Store** (`Grant & Audit Store`): High-integrity data tier containing relational grant records and an append-only, SHA-256 tamper-evident ledger (fulfilling **NFR-001**).
6. **Co-Author Service** (`Co-Author Service`): State machine coordinating multi-party digital author consent and dispute detection.
7. **Indexing Adapter** (`Indexing Adapter`): Resilient external gateway with circuit breakers connecting to Scopus, Web of Science, and CrossRef.
8. **Burn-Up Analytics** (`Burn-Up Analytics`): Statistical engine calculating historical spend velocity and linear regression runout forecasting.
9. **Notification Service** (`Notification Service`): Asynchronous multi-channel messaging service for 75%/90%/100% budget threshold alerts and co-author prompts.

---

## 4. Requirements Engineering Highlights

### 4.1 Functional Requirements (FR)

| Req ID | Priority | Requirement Title | Core Acceptance Criteria |
| :--- | :---: | :--- | :--- |
| **FR-001** | **High** | Grant Fund Allocation & Equipment Expense Cap | **Pass:** Balance updates accurately; blocks expenses exceeding grant cap.<br>**Fail:** Overdraft allowed without admin override. |
| **FR-002** | **High** | Overdraft Prevention & Dean Override | **Pass:** Enforces strict cap; clears transaction only with verified Dean cryptographic override signature.<br>**Fail:** Overdraft cleared without Dean authorization. |
| **FR-003** | **High** | Publication Metadata & DOI Auto-Ingestion | **Pass:** Auto-fetches metadata via DOI in < 2s; rejects duplicates.<br>**Fail:** Malformed DOI accepted; author association missing. |
| **FR-004** | **Medium** | External Indexing & Citation Synchronization | **Pass:** Synchronizes Scopus/WoS metrics; circuit breaker prevents external API timeout cascades.<br>**Fail:** Stale/fake metrics recorded without verification. |
| **FR-005** | **High** | Multi-Party Co-Author Digital Consent | **Pass:** All co-authors must sign off via secure tokens; objection halts endorsement.<br>**Fail:** Manuscript cleared while signoffs remain pending. |
| **FR-006** | **High** | Fund Burn-Up Velocity & Runout Forecasting | **Pass:** Linear regression projects fund depletion date; warns on early exhaustion.<br>**Fail:** Negative burn rate or inaccurate runout timeline. |

👉 *Full list of 12 Functional Requirements available in [`1-RE/RE_Document.md`](1-RE/RE_Document.md).*

---

### 4.2 Non-Functional Requirements (NFR)

| Req ID | Type | Description | Core Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **NFR-001** | **Security & Integrity** | Immutable, Tamper-Evident Audit Ledger | **Pass:** Maintains SHA-256 Merkle chain for all financial/status mutations; verification tool flags simulated byte modification immediately.<br>**Fail:** Database modified directly without invalidating hash chain. |
| **NFR-002** | **Performance** | Latency & Peak Load Throughput | **Pass:** P95 latency < 250ms, P99 < 450ms at 150 TPS under 2,000 concurrent sessions.<br>**Fail:** Latency > 2,000ms or error rate > 0.5%. |
| **NFR-003** | **Reliability** | High Availability (99.95% Uptime) | **Pass:** Automatic node failover within 30 seconds; RPO = 0s, RTO < 2 min.<br>**Fail:** Single server outage causes downtime > 5 min. |
| **NFR-004** | **Security** | End-to-End Encryption | **Pass:** TLS 1.3 in transit; AES-256 at rest; zero plaintext credentials in logs.<br>**Fail:** Weak ciphers permitted or unencrypted sensitive data. |

👉 *Full list of 8 Non-Functional Requirements available in [`1-RE/RE_Document.md`](1-RE/RE_Document.md).*

---

## 5. Requirements Traceability Matrix (RTM)

A summarized snapshot of the bidirectional RTM:

| Req ID | Category | Architectural Component | Interface | Verification Test ID | Acceptance Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Functional | `Grant & Fund Service` | `IGrantAllocation` | `TC-FIN-001` | **Verified (Pass)** |
| **FR-002** | Functional | `Grant & Fund Service` | `IDeanGovernance` | `TC-FIN-002` | **Verified (Pass)** |
| **FR-003** | Functional | `Publication Engine` | `IPublicationMetrics` | `TC-PUB-001` | **Verified (Pass)** |
| **FR-004** | Functional | `Indexing Adapter` | `IExternalIndexing` | `TC-PUB-002` | **Verified (Pass)** |
| **FR-005** | Functional | `Co-Author Service` | `ICoAuthorWorkflow` | `TC-AUTH-001` | **Verified (Pass)** |
| **FR-006** | Functional | `Burn-Up Analytics` | `IBurnUpAnalytics` | `TC-ANL-001` | **Verified (Pass)** |
| **FR-011** | Functional | `Notification Service` | `INotification` | `TC-NOTIF-001` | **Verified (Pass)** |
| **FR-012** | Functional | `Grant & Audit Store` | `IAuditLedgerStore` | `TC-AUD-001` | **Verified (Pass)** |
| **NFR-001** | Non-Func | `Grant & Audit Store` | `IAuditLedgerStore` | `TC-NFR-001` | **Verified (Pass)** |
| **NFR-002** | Non-Func | Microservices Layer | All Interfaces | `TC-NFR-002` | **Verified (Pass)** |

👉 *Complete 20-row matrix with test cases available in [`1-RE/RE_Document.md`](1-RE/RE_Document.md#5-requirements-traceability-matrix-rtm).*

---

## 6. Repository Organization

```
├── .gitignore                             # Git ignore rules
├── 1-RE/
│   ├── README.md                          # Requirements Engineering folder view
│   └── RE_Document.md                     # Complete FR, NFR, RTM Table & Test Case specs
├── 2-Architectural-Diagram/
│   ├── README.md                          # Architecture diagram folder view
│   ├── architecture_diagram.png           # High-resolution rendered UML component diagram
│   ├── architecture_diagram.svg           # Scalable vector graphics file
│   ├── architecture_diagram.html          # Interactive browser viewer
│   └── ARCHITECTURE_SPECIFICATION.md      # Detailed component & interface specifications
├── 7_SE_Lab1_SE_Problem_Statements.pdf     # SE Problem Statements Reference PDF
└── README.md                              # Master project overview & index
```
