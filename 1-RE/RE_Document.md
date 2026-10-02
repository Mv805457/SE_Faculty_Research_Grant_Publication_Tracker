# Requirements Engineering (RE) Document
## Faculty Research Grant & Publication Tracker
**Document Version:** 1.0.0  
**Target Organization:** Academic Deanery of Research & Development  
**Academic Course:** Software Engineering (Lab 3)
**Problem Statement #09:** Faculty Research Grant & Publication Tracker
**Student Name:** Madhav Vinod (PES1UG24CS254)

---

## 1. Problem Context & Overview

Higher education and research institutions receive substantial sponsored research funding from governmental agencies (e.g., DST, SERB, DARPA, NSF) and industrial sponsors. Currently, the research deanery faces significant bottlenecks in tracking these distributed research operations, including:
1. **Unmonitored Budget Burn Rates**: Lack of real-time visibility into capital equipment procurement, leading to unauthorized overdrafts or end-of-grant budget lapses.
2. **Disconnected Publication Tracking**: Faculty publications, journal indexings (SCI, Scopus, Web of Science), and citation metrics are manually reported, leading to inaccurate Institutional Research Ranking submissions (NIRF, QS, NAAC).
3. **Disputed Co-Authorship**: Delayed and non-transparent multi-institution co-author approval processes leading to authorship conflicts and ethical disputes.
4. **Vulnerable Audit Trails**: Financial and publication claim records lack tamper-evident integrity guarantees, posing risks during external institutional audits.

The **Faculty Research Grant & Publication Tracker** provides a centralized, automated portal with real-time financial tracking, immutable audit trails, automated citation syncing, and multi-party signoff workflows.

---

## 2. Stakeholders & System Actors

| Actor | Role Category | Primary Responsibilities |
| :--- | :--- | :--- |
| **Faculty Researcher (PI / Co-PI)** | Primary End-User | Submits grant applications, logs equipment procurement expenses, tracks budget balances, submits manuscript details for co-author review, and views personal citation metrics. |
| **Research Dean** | Administrative / Executive | Reviews and approves grant allocations, reviews fund burn-up analytics, authorizes budget cap overrides, enforces institutional publication policies, and audits financial logs. |
| **Department Research Head** | Management | Monitors departmental grant output, verifies milestone deliverables, and tracks departmental h-index and citation trajectories. |
| **Finance / Accounts Officer** | Financial Operations | Verifies procurement invoices, manages vendor payments, validates tax exemptions, and reconciles institutional ledgers. |
| **External Co-Author** | External Collaborator | Receives cryptographically secure signoff tokens via email to review manuscript drafts and affirm authorship order and institutional affiliation. |
| **External Indexing APIs** | External System | Third-party services (Scopus, Web of Science, CrossRef, OpenAlex, Google Scholar) providing citation counters, DOI metadata, and journal quartile ratings. |

---

## 3. Functional Requirements (FR)

### FR-001: Grant Fund Allocation & Equipment Procurement Cap Tracking
- **Priority:** High
- **Description:** The system shall track grant fund allocations across categorized budget heads (Equipment Procurement, Consumables, Travel, Contingency, Human Resources), allow faculty Principal Investigators (PIs) to log procurement expenses with quotes and invoices, and compute the remaining budgetary balance in real time.
- **Inputs:** Grant ID, Budget Head Category, Vendor Quotation Amount, Invoice Copy, Date of Procurement.
- **Outputs:** Deducted balance, Updated head-wise balance, Real-time ledger status.
- **Acceptance Criteria:**
  - *Pass:* Budget balance updates accurately immediately upon transaction confirmation; expenses attempting to exceed the designated budget head or total grant cap are strictly blocked and marked pending override.
  - *Fail:* Overdraft allowed without verified Deanery administrative override, or balance fails to decrement.

---

### FR-002: Overdraft Prevention & Administrative Dean Override Mechanism
- **Priority:** High
- **Description:** The system shall enforce a strict overdraft barrier preventing any procurement expense from clearing if it exceeds the remaining budget cap. The system shall allow the Research Dean to issue a signed administrative override with justification and fund reallocation parameters.
- **Inputs:** Overdraft claim reference ID, Dean digital authorization token, Reallocation source head, Justification note.
- **Outputs:** Overdraft override clearance token, Updated dual-head reallocated ledger record, Audit notification.
- **Acceptance Criteria:**
  - *Pass:* System rejects any transaction exceeding remaining balance by ≥ ₹1 / $1; successfully unblocks transaction only when Dean cryptographic override signature is validated.
  - *Fail:* Faculty bypasses cap via concurrent requests; Dean override fails to record in audit ledger.

---

### FR-003: Faculty Publication Metadata & DOI Automated Ingestion
- **Priority:** High
- **Description:** The system shall allow faculty to register research manuscripts and published papers by providing a Digital Object Identifier (DOI) or manual metadata (Title, Journal, ISSN, Issue, Volume, Author List, Corresponding Author).
- **Inputs:** DOI string or manual publication metadata payload.
- **Outputs:** Verified publication entry, DOI schema validation, Ingested author list, Unique Publication Tracking ID (`Pub-ID`).
- **Acceptance Criteria:**
  - *Pass:* Valid DOI automatically fetches and populates Title, Journal, Volume, Publisher, and Publication Date within 2 seconds; duplicate DOIs are rejected with conflict error.
  - *Fail:* Malformed DOI accepted without format validation; publication saved without associating at least one registered faculty member.

---

### FR-004: Automated External Indexing & Citation Synchronization
- **Priority:** Medium
- **Description:** The system shall periodically query external scholarly APIs (Scopus, Web of Science, CrossRef) to verify whether registered publications are indexed in SCI/SCIE/Scopus databases, capture journal quartile (Q1/Q2/Q3/Q4), and synchronize cumulative citation counts.
- **Inputs:** Publication DOI / ISSN / Author Scopus ID.
- **Outputs:** Verified Indexing Status (e.g., `Scopus Indexed`, `WoS SCIE`), Journal Quartile, Real-time citation count, Last Sync Timestamp.
- **Acceptance Criteria:**
  - *Pass:* Indexing engine matches DOI with Scopus/WoS; updates citation count and quartile ranking; logs sync history.
  - *Fail:* API failure causes system crash; non-indexed journal incorrectly labeled as SCI/Scopus without verification proof.

---

### FR-005: Multi-Party Co-Author Digital Consent & Approval Workflow
- **Priority:** High
- **Description:** The system shall orchestrate a multi-party approval workflow for all co-authored manuscripts. The submitting author defines author sequence and institutional contributions; the system dispatches secure one-time cryptographic signoff tokens to all co-authors to affirm their consent.
- **Inputs:** Submitting Author ID, Co-Author Email Addresses, Authorship Order, Contribution Percentage, Manuscript Draft / Abstract.
- **Outputs:** Individual cryptographic signoff URLs, Co-author approval status dashboard (`Pending`, `Approved`, `Disputed`), Final Clearance Certificate.
- **Acceptance Criteria:**
  - *Pass:* All listed co-authors must submit digital signoff before manuscript status transitions to `Deanery Endorsed`; any co-author objection instantly triggers `Disputed` status and halts clearance.
  - *Fail:* Manuscript marked approved while one or more co-author signoffs remain pending or rejected.

---

### FR-006: Fund Burn-Up Velocity & Runout Forecasting Analytics
- **Priority:** High
- **Description:** The system shall calculate historical fund burn rates across grants, plot burn-up charts showing cumulative planned vs. actual expenditure against project milestones, and forecast estimated fund depletion dates (runout velocity).
- **Inputs:** Grant Start Date, End Date, Approved Milestone Schedule, Historical Transaction Ledger.
- **Outputs:** Interactive Burn-Up chart, Burn velocity (₹ / month), Projected runout date, Variance percentage against milestone baseline.
- **Acceptance Criteria:**
  - *Pass:* Burn-up projection mathematically aligns with linear regression of past 3 months' spend; warns if projected runout occurs before milestone completion.
  - *Fail:* Negative burn rate displayed; runout date calculated incorrectly past grant end date without warning.

---

### FR-007: Milestone Deliverable Tracking & Tranche Fund Release
- **Priority:** Medium
- **Description:** The system shall tie grant fund availability to scheduled project milestones (e.g., Year 1 Milestone Deliverable: Prototype Complete). PIs submit milestone reports; Deanery approves release of subsequent fund tranches.
- **Inputs:** Milestone ID, Deliverable Report PDF, PI Completion Declaration, Dean Approval Action.
- **Outputs:** Tranche status transition (`Locked` -> `Released`), Available balance update, Deanery signoff stamp.
- **Acceptance Criteria:**
  - *Pass:* Tranche funds remain locked and unavailable for procurement until Dean approves the corresponding milestone deliverable.
  - *Fail:* Funds from Tranche 2 released automatically while Milestone 1 remains incomplete.

---

### FR-008: Role-Based Access Control (RBAC) & Deanery Approval Console
- **Priority:** High
- **Description:** The system shall provide distinct, authenticated web consoles tailored to user roles: Faculty Researcher (access to personal grants, papers, expenses) and Research Dean (institutional overview, approvals, cap overrides, cross-departmental auditing).
- **Inputs:** User credentials, Multi-Factor Authentication (MFA) OTP, Role assignment.
- **Outputs:** JWT token with scoped permissions, Role-specific UI dashboard.
- **Acceptance Criteria:**
  - *Pass:* Faculty user attempting to access Dean administrative endpoints receives `403 Forbidden`; unauthorized access attempts are logged in security audit.
  - *Fail:* Privilege escalation allows faculty to approve their own grants or expense claims.

---

### FR-009: Equipment Procurement Invoice Logging & Asset Tagging
- **Priority:** Medium
- **Description:** The system shall require faculty to upload vendor quotation, invoice PDF, and equipment physical serial number/asset code upon logging an equipment expense, generating an institutional Asset Barcode ID.
- **Inputs:** Equipment Name, Vendor Details, Invoice Amount, Serial Number, Physical Location / Lab Room ID, Invoice File Upload.
- **Outputs:** Institutional Asset Tag ID, Equipment Ledger Entry, Physical Verification Schedule.
- **Acceptance Criteria:**
  - *Pass:* Equipment expense cannot be submitted without an attached PDF invoice and physical lab location identifier.
  - *Fail:* Duplicate invoice numbers accepted across different grants; file uploads other than sanitized PDF/PNG allowed.

---

### FR-010: Consolidated Departmental Research Output Analytics
- **Priority:** Medium
- **Description:** The system shall aggregate grant revenues, active projects, publication counts, citations, and average journal impact factors across academic departments, generating printable PDF/Excel reports for accreditation bodies (NIRF, NAAC).
- **Inputs:** Academic Year range, Department Filter, Report Format (`PDF`, `XLSX`).
- **Outputs:** Formatted report table, Graphical summary charts, Downloadable export file.
- **Acceptance Criteria:**
  - *Pass:* Aggregated figures match exact sum of individual faculty and grant records within selected date range; report exports in < 3 seconds.
  - *Fail:* Cross-department faculty dual-appointments result in duplicate grant revenue counting.

---

### FR-011: Automated Alerting on Budget Depletion Thresholds (75%, 90%, 100%)
- **Priority:** Medium
- **Description:** The system shall continuously monitor grant budget consumption and dispatch automated multi-channel notifications (in-app, email, SMS) when cumulative expenditure reaches 75%, 90%, and 100% of the allocated cap.
- **Inputs:** Spend transaction event, Budget threshold configuration.
- **Outputs:** Alert trigger event, Notification queue dispatch, Deanery alert banner.
- **Acceptance Criteria:**
  - *Pass:* Notifications dispatched within 10 seconds of expense clearing that crosses 75%, 90%, or 100% threshold; PI and Dean notified simultaneously.
  - *Fail:* Expense crossing threshold fails to trigger notification; duplicate spam alerts generated for subsequent expenses within same tier.

---

### FR-012: Comprehensive Audit Trail Querying & Verification
- **Priority:** High
- **Description:** The system shall provide an audit investigation interface allowing the Deanery and external auditors to filter, inspect, and verify the cryptographic integrity of all financial transactions, cap overrides, and publication status alterations.
- **Inputs:** Grant ID / Date Range / Event Type filter, Verification Hash.
- **Outputs:** Filtered chronologically ordered event timeline, Cryptographic block hash, Chain integrity verification badge (`VALID` / `TAMPERED`).
- **Acceptance Criteria:**
  - *Pass:* System scans hash chain and confirms 100% block integrity; any manual database modification flags the specific altered record with a `TAMPERED` red alert.
  - *Fail:* Modified historical record validates without detecting cryptographic hash mismatch.

---

## 4. Non-Functional Requirements (NFR)

### NFR-001: Immutable, Tamper-Evident Financial Audit Ledger
- **Type:** Security & Integrity
- **Description:** The system shall maintain an immutable, tamper-evident audit ledger for all financial approvals, expense allocations, cap overrides, and journal status modifications using SHA-256 cryptographic chaining (Merkle block linking).
- **Acceptance Criteria:**
  - *Pass:* Each ledger entry contains a cryptographic hash of its payload combined with the previous record's hash (`PrevHash + Nonce + Data -> CurrentHash`). Benchmarking confirms hash generation latency < 15ms per transaction; verification utility detects any simulated bit flip in historical records.
  - *Fail:* Database records can be modified via SQL UPDATE/DELETE without invalidating chain integrity.

---

### NFR-002: System Latency & Throughput Under Peak Workload
- **Type:** Performance
- **Description:** The portal shall maintain high responsiveness during end-of-quarter grant closing and accreditation cycles, sustaining at least 150 concurrent transactions per second (TPS).
- **Acceptance Criteria:**
  - *Pass:* 95th percentile (P95) API response time < 250ms and 99th percentile (P99) < 450ms under simulated peak load of 2,000 active concurrent sessions.
  - *Fail:* Response latency exceeds 2,000ms or error rate exceeds 0.5% under simulated peak load.

---

### NFR-003: High Availability & Disaster Recovery
- **Type:** Reliability & Availability
- **Description:** The system shall guarantee an operational uptime of 99.95% during active academic terms, with automated database replication, point-in-time recovery (PITR), and zero-data-loss failover.
- **Acceptance Criteria:**
  - *Pass:* Automated health probes detect node failure and switch traffic within 30 seconds; Recovery Point Objective (RPO) = 0 seconds; Recovery Time Objective (RTO) < 2 minutes.
  - *Fail:* Single server outage causes portal unavailability > 5 minutes.

---

### NFR-004: End-to-End Cryptographic Data Protection
- **Type:** Security & Confidentiality
- **Description:** All data in transit must be encrypted using TLS 1.3 with forward secrecy; all persistent grant files, invoices, and sensitive financial tables must be encrypted at rest using AES-256-GCM.
- **Acceptance Criteria:**
  - *Pass:* SSL Labs rating of A+; automated vulnerability scanning confirms no cleartext credentials or tokens stored in database or application logs.
  - *Fail:* Weak cipher suites allowed; plain-text storage of grant financial details or author authentication tokens.

---

### NFR-005: Role-Based Access Security & Least Privilege Principle
- **Type:** Security
- **Description:** Access to all REST APIs and microservice endpoints must strictly adhere to the Principle of Least Privilege, verified via short-lived JWT tokens signed using RS256 with role claims.
- **Acceptance Criteria:**
  - *Pass:* Requests without valid bearer token rejected with HTTP 401; requests with insufficient role scope rejected with HTTP 403.
  - *Fail:* Insecure Direct Object Reference (IDOR) allows a faculty member to view another faculty member's unapproved grant proposal.

---

### NFR-006: Usability & Web Accessibility
- **Type:** Usability
- **Description:** The web portal interface shall comply with Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards, provide high contrast ratios (≥ 4.5:1), and be fully navigable via keyboard.
- **Acceptance Criteria:**
  - *Pass:* Automated Lighthouse accessibility score ≥ 95; screen reader compatibility verified for all grant submission and approval forms.
  - *Fail:* Interactive elements lack accessible labels; keyboard trap prevents navigation through modal approval dialogs.

---

### NFR-007: External Scholarly API Resilience & Fault Tolerance
- **Type:** Robustness & Integration
- **Description:** Invocations to third-party indexing APIs (Scopus, Web of Science, CrossRef) must implement exponential backoff, rate limiting, and circuit breaker patterns to prevent external outages from degrading core portal operations.
- **Acceptance Criteria:**
  - *Pass:* Circuit breaker trips open after 5 consecutive external API timeouts; system serves cached citation data with "stale data" indicator without throwing unhandled exceptions.
  - *Fail:* External API slowdown causes portal request worker starvation and crashes the application server.

---

### NFR-008: Compliance & Archival Data Retention
- **Type:** Regulatory Compliance
- **Description:** The system shall retain all grant financial records, procurement invoices, co-author consent logs, and audit chains for a minimum of 7 years in compliance with national statutory research funding regulations.
- **Acceptance Criteria:**
  - *Pass:* Archival worker automatically migrates closed grants older than 1 year to immutable cold storage while preserving queryability for audit requests.
  - *Fail:* Historical grant records deleted or purged without authorized Deanery archival procedure.

---

## 5. Requirements Traceability Matrix (RTM)

The Requirements Traceability Matrix establishes bidirectional traceability linking User Needs, Functional/Non-Functional Requirements, Architectural Components, Interfaces, and Verification Test IDs.

| Req ID | Category | Requirement Title | Architectural Component | Interface Name | Verification Test ID | Acceptance Criteria Summary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-001** | Functional | Grant Fund Allocation & Equipment Expense Cap | Grant & Fund Service | `IGrantAllocation` | `TC-FIN-001` | Balance updates accurately; blocks overdrafts exceeding cap. |
| **FR-002** | Functional | Overdraft Prevention & Dean Override | Grant & Fund Service | `IDeanGovernance` | `TC-FIN-002` | Rejects spend > cap; clears only with valid Dean signature. |
| **FR-003** | Functional | Publication Metadata & DOI Ingestion | Publication Engine | `IPublicationMetrics` | `TC-PUB-001` | DOI auto-populates metadata in < 2s; rejects duplicates. |
| **FR-004** | Functional | External Indexing & Citation Synchronization | Indexing Adapter | `IExternalIndexing` | `TC-PUB-002` | Fetches Scopus/WoS metrics; gracefully handles timeouts. |
| **FR-005** | Functional | Co-Author Approval & Consent Workflow | Co-Author Service | `ICoAuthorWorkflow` | `TC-AUTH-001` | All co-authors must sign off; objection halts endorsement. |
| **FR-006** | Functional | Fund Burn-Up Velocity & Runout Forecasting | Burn-Up Analytics | `IBurnUpAnalytics` | `TC-ANL-001` | Accurate spend velocity regression; warns on early runout. |
| **FR-007** | Functional | Milestone Deliverables & Tranche Release | Grant & Fund Service | `IGrantAllocation` | `TC-FIN-003` | Tranche funds unlock only upon Dean milestone approval. |
| **FR-008** | Functional | Role-Based Access Control (RBAC) | Faculty Portal / Dean Console | `IGrantAllocation` / `IDeanGovernance` | `TC-SEC-001` | 403 on privilege violation; strict role segregation. |
| **FR-009** | Functional | Equipment Invoice & Asset Tagging | Grant & Fund Service | `IGrantAllocation` | `TC-FIN-004` | Requires invoice upload & serial number; generates Asset ID. |
| **FR-010** | Functional | Departmental Research Output Analytics | Burn-Up Analytics | `IBurnUpAnalytics` | `TC-ANL-002` | Aggregated report matches sum of records; exports < 3s. |
| **FR-011** | Functional | Budget Depletion Threshold Alerts (75/90/100%) | Notification Service | `INotification` | `TC-NOTIF-001` | Alerts dispatched < 10s of crossing spend threshold. |
| **FR-012** | Functional | Audit Trail Querying & Verification | Grant & Audit Store | `IAuditLedgerStore` | `TC-AUD-001` | Verifies SHA-256 chain; detects any simulated data tamper. |
| **NFR-001** | Non-Func | Immutable Tamper-Evident Audit Ledger | Grant & Audit Store | `IAuditLedgerStore` | `TC-NFR-001` | Cryptographic hash chained; detects tampering instantly. |
| **NFR-002** | Non-Func | Latency & Throughput Under Peak Workload | All Microservices | All Interfaces | `TC-NFR-002` | P95 < 250ms, P99 < 450ms at 150 TPS and 2000 sessions. |
| **NFR-003** | Non-Func | High Availability & Disaster Recovery | Infrastructure Layer | Service Mesh | `TC-NFR-003` | 99.95% uptime; failover completes in < 30s. |
| **NFR-004** | Non-Func | End-to-End Cryptographic Data Protection | All Services | TLS 1.3 / AES-256 | `TC-NFR-004` | A+ SSL rating; zero plaintext credentials in logs/DB. |
| **NFR-005** | Non-Func | Least Privilege & Role-Based Security | API Gateway / Auth | JWT Claims | `TC-NFR-005` | Rejects unauthenticated/unauthorized API requests. |
| **NFR-006** | Non-Func | Usability & WCAG 2.1 AA Accessibility | Frontend Consoles | Web UI | `TC-NFR-006` | Lighthouse score ≥ 95; screen reader & keyboard verified. |
| **NFR-007** | Non-Func | External API Resilience & Circuit Breaker | Indexing Adapter | `IExternalIndexing` | `TC-NFR-007` | Circuit breaker trips after 5 timeouts; returns cached data. |
| **NFR-008** | Non-Func | Compliance & 7-Year Archival Retention | Data Storage Layer | Cold Storage Archive | `TC-NFR-008` | Preserves records for 7 years; automated lifecycle rules. |

---

## 6. Verification & Test Case Guidelines

### Sample Test Case 1: `TC-FIN-001` (FR-001 Verification)
- **Objective:** Verify equipment procurement expense logging and cap enforcement.
- **Preconditions:** Grant `GR-2026-042` has ₹5,00,000 allocated under Equipment Head. Remaining balance = ₹1,20,000.
- **Test Steps:**
  1. Faculty logs in and initiates procurement request for "Spectrophotometer accessory" amounting to ₹1,50,000.
  2. System evaluates `₹1,50,000 > Remaining Balance (₹1,20,000)`.
  3. Attempt transaction clearance.
- **Expected Outcome (Pass):** Transaction is rejected with code `ERR_BUDGET_CAP_EXCEEDED`. Balance remains ₹1,20,000. Prompt displayed: "Request Deanery Overdraft Override".
- **Failure Condition:** Transaction completes, creating negative balance `-₹30,000` without Dean authorization.

### Sample Test Case 2: `TC-NFR-001` (NFR-001 Verification)
- **Objective:** Verify tamper-evident cryptographic chaining in audit ledger.
- **Preconditions:** 500 financial and status transactions recorded with valid SHA-256 block hashes.
- **Test Steps:**
  1. Execute system audit integrity check `verify_chain_integrity()`. Confirm return status = `VALID`.
  2. Simulate unauthorized database attack by executing direct SQL: `UPDATE financial_tx SET amount = 50000 WHERE tx_id = 245;`
  3. Re-run `verify_chain_integrity()`.
- **Expected Outcome (Pass):** Verification engine flags Block #245 with `HASH_MISMATCH` (`CalculatedHash != StoredHash`) and marks subsequent blocks as unverified due to broken `PrevHash` linkage.
- **Failure Condition:** System reports chain as `VALID` despite modified record.
