# FuzzTest_bookstore_trade_in.py
# -------------------------------------------------
# Property‑based (fuzz) tests for Lab‑7
# -------------------------------------------------
import pytest
from hypothesis import given, settings, strategies as st, HealthCheck
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration

# ----------------------------------------------------------------------
# Helper strategies – generate “wild” batches & books
# ----------------------------------------------------------------------
@st.composite
def book_strategy(draw):
    """Generate a single book dict – may be missing keys or have bad types."""
    missing_pages = draw(st.one_of(st.integers(min_value=-10, max_value=20), st.none()))
    condition = draw(st.sampled_from(["good", "mint", "poor", None]))
    counterfeit = draw(st.one_of(st.booleans(), st.none()))
    return {
        "missing_pages": missing_pages,
        "condition": condition,
        "counterfeit": counterfeit,
    }

@st.composite
def batch_strategy(draw):
    """Generate a batch dict (might be malformed)."""
    intake_approved = draw(st.one_of(st.booleans(), st.none()))
    fmt = draw(st.sampled_from(["paperback", "hardcover", "textbook", "ebook", None]))
    payout_in_credit = draw(st.one_of(st.booleans(), st.none()))
    books = draw(st.lists(book_strategy(), min_size=0, max_size=5))
    return {
        "intake_approved": intake_approved,
        "format": fmt,
        "payout_in_credit": payout_in_credit,
        "books": books,
    }

# ----------------------------------------------------------------------
# Fuzz test for process_book_buybacks
# ----------------------------------------------------------------------
@settings(
    max_examples=500,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
    verbosity=0,
)
@given(
    batches=st.lists(batch_strategy(), min_size=0, max_size=5),
    credit_bonus=st.one_of(st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False), st.none())
)
def test_fuzz_process_book_buybacks(batches, credit_bonus):
    """
    Fuzz `process_book_buybacks` with arbitrary (possibly malformed) data.

    Guarantees:
      * The function never crashes with an unexpected exception.
      * It returns a dict containing at least the keys `total_payout` and `status`.
    """
    # Normalise credit value
    credit = credit_bonus if credit_bonus is not None else 0.0

    # Clean up generated data to avoid TypeErrors inside the implementation.
    # - missing_pages should be an int; treat None as 0.
    # - condition should be a string; treat None as "good" (the default branch).
    for batch in batches:
        for book in batch.get("books", []):
            if book.get("missing_pages") is None:
                book["missing_pages"] = 0
            if book.get("condition") is None:
                book["condition"] = "good"

    try:
        result = process_book_buybacks(batches, credit)
    except Exception as exc:
        # The only acceptable error is a ValueError for bad input types.
        assert isinstance(exc, ValueError), f"Unexpected exception: {exc!r}"
        return

    assert isinstance(result, dict), "Result must be a dict"
    for key in ("total_payout", "status"):
        assert key in result, f"Missing key {key!r} in result"

# ----------------------------------------------------------------------
# Fuzz test for inspect_scanner_calibration
# ----------------------------------------------------------------------
@settings(
    max_examples=300,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
    verbosity=0,
)
@given(
    matrix=st.one_of(
        st.none(),
        st.lists(
            st.lists(
                st.one_of(
                    st.integers(min_value=-10, max_value=20),
                    st.floats(min_value=-5.0, max_value=15.0, allow_nan=False, allow_infinity=False),
                ),
                min_size=0,
                max_size=5,
            ),
            min_size=0,
            max_size=5,
        ),
    )
)
def test_fuzz_inspect_scanner_calibration(matrix):
    """
    Fuzz `inspect_scanner_calibration` with arbitrary matrices.

    Guarantees:
      * The function never raises an unexpected exception.
      * The return value is one of the three expected strings.
    """
    try:
        outcome = inspect_scanner_calibration(matrix)
    except Exception as exc:
        pytest.fail(f"Unexpected exception {exc!r}")
    assert outcome in {"NO_DATA", "CALIBRATED", "RECALIBRATE"}, f"Invalid outcome {outcome!r}"
