# Lab 5 · Static analysis of grant expense claims

The [course problem 09 Movie Seats solution](09_movie_seats/) includes the corrected program, issue register, reflection and before/after tool output. The faculty-themed exercise below applies the same analysis to grant spending.

A finance officer checks a batch of invoices against one grant budget head. The sample processes integer paise in input order. Invoice deduplication covers a single batch. The baseline is an intentionally faulty exercise fixture.

From this directory, install `pylint flake8 bandit` with pip and run:

```sh
python expense_review.py
python -m unittest -v
python -m pylint expense_review.py
python -m flake8 expense_review.py
python -m bandit expense_review.py
```

Repeat the three analysis commands on `baseline/expense_review.py` for comparison. See the [findings](issues.md), [reflection](reflection.md) and [captured tool output](reports/). A clean Flake8 report has no output.
