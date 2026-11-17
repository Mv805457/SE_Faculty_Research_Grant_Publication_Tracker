# Static analysis reflection

**Which findings mattered most?** A negative expense increased the grant balance, and a replayed invoice could consume it twice. Those outcomes would give a faculty researcher a misleading picture of available funds.

**What did the tools contribute?** Flake8 highlighted import and layout problems. Pylint also flagged missing documentation. Bandit's B101 points to the assertion used to check the amount. An assertion is a poor input boundary because an optimized interpreter can omit it.

**What needed human review?** The comparison `amount >= balance` is legal Python. The requirement that faculty can spend the exact balance makes the equality case a defect. The duplicate-invoice policy also required a domain decision. An invoice counts as used only after approval, so a researcher can correct a rejected claim.

**How can the fixes be checked again?** Run all three analyzers on both files, then execute the six regression tests. The sample ends with zero paise remaining after accepting GPU-01 and LAB-02. The repeated reference and the one-paisa overdraft appear in the rejection list.
