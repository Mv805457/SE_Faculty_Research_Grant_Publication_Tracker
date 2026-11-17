# Reflection on the seat reservation exercise

**Which issue had the largest practical consequence?** The out-of-range and mixed-type bookings invalidated the free-seat count. Counting an invalid seat as occupied directly changes what the next customer can book.

**Which tool helped with which issue?** Bandit identified the MD5 use and the broad permissions. Flake8 exposed a bare exception and formatting problems. Pylint identified the mutable default, missing documentation and resource-management issues.

**Which bug needed manual testing?** A text value and an integer can represent the same seat to a customer. Membership checks on a Python list distinguish them. Testing a duplicate reservation across a load/save cycle verifies what the customer experiences.

**How was the repair verified?** The regression suite checks boundaries, repeat bookings, release behavior, stable ticket references and JSON round-tripping. Loading an invalid plan raises an error and retains the previous valid bookings. Run the three tools on the same module to reproduce the final reports.
