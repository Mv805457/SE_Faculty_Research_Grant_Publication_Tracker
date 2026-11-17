"""
Lab 6 – Code Coverage Test Suite
Problem 09: Bookstore Trade-In

Target: ≥ 90% LINE (code) coverage of bookstore_trade_in.py
Run:
    coverage run -m pytest CodeCoverageTest_09_bookstore_trade_in.py -v
    coverage report -m
"""

import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


# ─────────────────────────────────────────────────────────────────────────────
# process_book_buybacks – happy-path / core scenarios
# ─────────────────────────────────────────────────────────────────────────────

def test_single_paperback_good_condition():
    """Paperback in 'good' condition → base_value 8.0, status COMPLETED."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_single_hardcover_good_condition():
    """Hardcover in 'good' condition → base_value 15.0."""
    batches = [
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 15.0
    assert result["status"] == "COMPLETED"


def test_single_textbook_good_condition():
    """Textbook in 'good' condition → base_value 40.0."""
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 40.0
    assert result["status"] == "COMPLETED"


def test_mint_condition_bonus():
    """Mint condition applies 1.25× multiplier."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "mint", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == round(8.0 * 1.25, 2)
    assert result["status"] == "COMPLETED"


def test_poor_condition_penalty():
    """Poor condition applies 0.40× multiplier."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "poor", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == round(8.0 * 0.40, 2)
    assert result["status"] == "COMPLETED"


def test_payout_in_credit_adds_bonus():
    """Store-credit flag adds store_credit_bonus to batch total."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": True,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 10.0)
    assert result["total_payout"] == 18.0   # 8 + 10
    assert result["status"] == "COMPLETED"


def test_batch_not_approved_is_skipped():
    """Batches with intake_approved=False are silently skipped → ZERO_CREDIT."""
    batches = [
        {
            "intake_approved": False,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_missing_pages_rejects_book():
    """Books with missing_pages > 0 are rejected (increment rejected_items)."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 3, "condition": "good", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_unknown_format_rejected():
    """Unknown format increments rejected_items and the batch is skipped."""
    batches = [
        {
            "intake_approved": True,
            "format": "ebook",          # unsupported format
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_non_textbook_adds_zero():
    """Counterfeit book in a non-textbook batch adds 0 credit but batch continues."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
                {"missing_pages": 0, "condition": "good", "counterfeit": False},
            ],
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    # First book: counterfeit → 0; second book: good → 8.0
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_counterfeit_textbook_zeroes_batch_and_breaks():
    """Counterfeit in textbook batch zeroes entire batch_credit and breaks inner loop."""
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "good", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
                {"missing_pages": 0, "condition": "mint", "counterfeit": False},
            ],
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_audit_rejected_when_too_many_rejected_items():
    """More than 4 rejected items triggers AUDIT_REJECTED even if payout > 0."""
    # 5 bad books (missing pages) + 1 good book → 5 rejected items → AUDIT_REJECTED
    bad_books = [{"missing_pages": 1, "condition": "good", "counterfeit": False}] * 5
    good_book  = [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": bad_books + good_book,
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_invalid_batches_raises_valueerror():
    """Non-list batches raise ValueError."""
    with pytest.raises(ValueError):
        process_book_buybacks("not a list", 5.0)


def test_negative_credit_bonus_raises_valueerror():
    """Negative store_credit_bonus raises ValueError."""
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


def test_empty_batches_returns_zero_credit():
    """Empty batches list → ZERO_CREDIT."""
    result = process_book_buybacks([], 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_multiple_batches_total_correctly():
    """Multiple approved batches sum their credits."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        },
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}],
        },
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 23.0   # 8 + 15
    assert result["status"] == "COMPLETED"


# ─────────────────────────────────────────────────────────────────────────────
# inspect_scanner_calibration – all branches
# ─────────────────────────────────────────────────────────────────────────────

def test_scanner_no_data_empty_list():
    """Empty matrix → NO_DATA."""
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_calibrated_all_low_errors():
    """All error rates ≤ 5 → CALIBRATED."""
    matrix = [[1, 2, 3], [4, 5, 5]]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_scanner_recalibrate_two_consecutive_high():
    """Two consecutive error_rate > 5 → RECALIBRATE."""
    matrix = [[6, 7, 1]]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"


def test_scanner_high_errors_not_consecutive():
    """High errors interrupted by low → stays CALIBRATED."""
    matrix = [[6, 1, 6]]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_scanner_calibrated_single_high_value():
    """Single high error rate (streak=1) does not trigger RECALIBRATE."""
    matrix = [[6]]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_scanner_multiple_devices_second_triggers_recalibrate():
    """First device fine; second device has two consecutive errors."""
    matrix = [[1, 2], [8, 9]]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"
