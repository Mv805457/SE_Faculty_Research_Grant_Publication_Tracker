# Bookstore Trade-In coverage results

These measurements cover the assigned module `bookstore_trade_in.py`. They exclude test code from the coverage denominator.

| Suite | Tests passed | Executable statements | Missed statements | Branch outcomes | Partial branches |
|---|---:|---:|---:|---:|---:|
| Line coverage | 22 | 57 | 0 | — | — |
| Branch coverage | 26 | 57 | 0 | 40 of 40 | 0 |

```sh
python -m pip install pytest coverage
python -m coverage run --source=bookstore_trade_in -m pytest CodeCoverageTest_09_bookstore_trade_in.py
python -m coverage report -m
python -m coverage run --branch --source=bookstore_trade_in -m pytest BranchCoverageTest_09_bookstore_trade_in.py
python -m coverage report -m
```

The suites exercise format-specific payouts, rejected formats, counterfeit textbooks, missing pages, zero credit and scanner misread streaks. A single high reading and two consecutive high readings take different paths. A low reading resets the streak. Coverage records execution of those paths. The assertions in the suites determine which outcomes were checked.

[Original line-coverage screenshot](screenshots/code_coverage_100.png) · [Original branch-coverage screenshot](screenshots/branch_coverage_100.png)
