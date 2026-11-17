# Use-Case Flow Specification

**Project:** Faculty Research Grant & Publication Tracker  
**Course:** Software Engineering Lab 1 (PES University - Dept. of CSE)  
**Problem Statement:** #09 (Campus & Academic Operations)  

---

## Use Case Specification: UC-01
### Log Equipment Procurement Expense & Grant Fund Deduction

| Attribute | Specification Detail |
|---|---|
| **Use Case ID** | `UC-01` |
| **Use Case Name** | Log Equipment Procurement Expense & Grant Fund Deduction |
| **Primary Actor** | Faculty Researcher (Principal Investigator) |
| **Secondary Actor(s)** | Research Dean (Override Approver), Finance Audit Subsystem |
| **Scope** | Research Grant Financial Management Module |
| **Level** | User-Goal Level |
| **Trigger** | Faculty researcher procures laboratory/research equipment and submits an expense claim against an active research grant. |

---

### 1. Brief Description
This use case enables a Faculty Researcher (Principal Investigator or Co-PI) to record an equipment procurement expense against an active sponsored research grant. The system validates the invoice attachment, verifies that the remaining balance under the designated budget head is sufficient, deducts the expense, logs an immutable audit entry, and recalculates real-time grant burn-up analytics.

---

### 2. Preconditions
1. The Faculty Researcher is authenticated into the portal with valid PI/Co-PI role privileges.
2. The selected research grant has status `ACTIVE` and has an allocated budgetary balance.
3. An itemized vendor invoice is available in digital format (PDF, PNG, or JPEG under 15 MB).

---

### 3. Postconditions
1. **Financial Update:** The grant's "Equipment" budget head and total remaining grant balance are decremented by the exact expense amount.
2. **Ledger Record:** An immutable audit log entry is created with transaction metadata and SHA-256 hash.
3. **Analytics Refresh:** Real-time fund burn-up analytics and velocity curves are refreshed immediately.
4. **Status:** The expense record is marked as `DEDUCTED` (or `PENDING_DEAN_OVERRIDE` in the alternate flow).

---

### 4. Main Success Scenario (MSS / Happy Path)
1. **Researcher Action:** Faculty Researcher navigates to the **"My Sponsored Grants"** workspace.
2. **System Response:** System retrieves and displays active grants, showing budgetary allocations, expenditure heads (Equipment, Consumables, Travel, Contingency), and remaining balances.
3. **Researcher Action:** Researcher selects the active grant and clicks **"Log Procurement Expense"**.
4. **System Response:** System renders the expense logging form with pre-populated grant metadata.
5. **Researcher Action:** Researcher inputs expense details:
   - *Expense Head:* "Equipment"
   - *Item Description:* "High-Performance GPU Workstation for Deep Learning Simulation"
   - *Vendor Name & Invoice Number:* "Apex Technologies Ltd. - INV-2026-7732"
   - *Purchase Date:* "2026-08-22"
   - *Amount:* "$12,400"
   - *Attachment:* Uploads scanned invoice PDF.
6. **Researcher Action:** Researcher clicks **"Submit Expense"**.
7. **System Response:** System validates mandatory fields and confirms file upload format and checksum.
8. **System Response (`«include» UC-02`):** System performs automated balance verification against the "Equipment" budget head.
9. **System Response:** System verifies `Invoice Amount ($12,400) ≤ Available Equipment Balance ($18,000)`.
10. **System Response:** System deducts `$12,400` from the Equipment line-item balance and updates total grant balance.
11. **System Response (`«include» NFR-001`):** System creates an immutable audit record containing Transaction ID, Actor ID, Grant ID, Amount, Timestamp, and SHA-256 integrity hash.
12. **System Response:** System updates the real-time fund burn-up chart, displays a **"Transaction Successful - Ref #EXP-2026-0942"** confirmation banner, and emails a receipt to the researcher.
13. **Conclusion:** Use case ends successfully.

---

### 5. Alternate Flows

#### Alternate Flow 1: ALT-1 (Expense Exceeds Allocated Head Balance - Dean Override Workflow)
*Triggered at Step 8 via `«extend» UC-03` when `[Invoice Amount > Available Budget Balance]`*

- **8a.** System detects that `Invoice Amount ($22,000) > Available Equipment Balance ($18,000)`.
- **8b.** System blocks automatic debit and checks if the grant contingency reserve can cover the $4,000 difference.
- **8c.** System prompts researcher:
  > *"Expense exceeds available Equipment budget by $4,000. Would you like to request an Overdraft Reallocation from the Research Dean?"*
- **8d.** Researcher enters justification: *"Procured upgraded multi-GPU cluster required for Phase 2 benchmarking as approved in technical review"* and clicks **"Submit Override Request"**.
- **8e.** System marks expense as `PENDING_DEAN_OVERRIDE` and places a temporary hold on the contingency head.
- **8f.** System dispatches a high-priority alert to the **Research Dean's Review Queue**.
- **8g.** Research Dean reviews the justification, validates project milestone runway, and clicks **"Approve Overdraft Reallocation"**.
- **8h.** System shifts $4,000 from Contingency to Equipment head, completes the debit, records dual signatures in the audit ledger, and sets status to `APPROVED_BY_DEAN`.
- **8i.** System notifies the researcher and recalculates the burn-up curve.

#### Alternate Flow 2: ALT-2 (Corrupted or Invalid Receipt Upload)
*Triggered at Step 7 during file integrity check*

- **7a.** System detects unsupported file type or corrupted PDF file.
- **7b.** System displays error banner: *"Invalid attachment. Please upload an authentic PDF, PNG, or JPEG file under 15 MB."*
- **7c.** System retains all inputted text fields.
- **7d.** Researcher selects a valid file and re-submits. Flow resumes at Step 7 of the Main Success Scenario.

---

### 6. Exception Flows
- **EXC-1: Grant Frozen / Terminated:** If the grant project duration has expired or is frozen by the funding agency, system displays an error modal: *"This grant is closed or frozen. No expenses may be logged."* Transaction aborts.
