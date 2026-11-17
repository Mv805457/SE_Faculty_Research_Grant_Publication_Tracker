# Expense review findings

Line numbers refer to the frozen [baseline](baseline/expense_review.py). Amounts are integer paise. Re-run the functional checks with `python -m unittest -v` from Lab5.

| ID | Severity and type | Lines | Reproduction on baseline | Correction |
|---|---|---|---|---|
| EXP-01 | High, integrity | 7–12 | A claim for −10 against 100 increases the balance to 110. | Reject zero, negative, fractional and boolean amounts before accounting. |
| EXP-02 | High, duplicate debit | 11–12 | Submit invoice A for 20 twice against 100. Both are paid and 60 remains. | Remember approved invoice references within the batch after trimming and case folding. |
| EXP-03 | Medium, boundary | 9 | A claim for exactly 100 against 100 is skipped. | Reject only amounts strictly above the available balance. |
| EXP-04 | Medium, input validation | 8 | A string amount triggers AssertionError in normal mode. Python can omit the assertion in optimized mode. | Validate explicitly and return a row-level rejection. Bandit identifies the original assertion as B101. |
| EXP-05 | Medium, robustness | 7, 11 | A missing invoice raises KeyError instead of returning the remaining balance. | Validate required fields before deducting and record the row and reason. |
| EXP-06 | Low, maintainability | 1–3, 13 | Unused imports, combined imports, missing documentation and cramped spacing make the review harder to read. | Keep only the imports used by the sample runner, document the function contract and apply consistent formatting. |
