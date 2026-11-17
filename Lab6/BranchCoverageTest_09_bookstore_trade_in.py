"""
Lab 6 – Branch Coverage Test Suite
Problem 09: Bookstore Trade-In

Target: ≥ 90% BRANCH coverage of bookstore_trade_in.py
Run:
    coverage run --branch -m pytest BranchCoverageTest_09_bookstore_trade_in.py -v
    coverage report -m

Branch map for process_book_buybacks
─────────────────────────────────────
B1  line 2  : batches not a list OR credit_bonus < 0  → True (raises) / False (continues)
B2  line 9  : intake_approved → True / False
B3  line 15 : format == "textbook"   → True / False
B4  line 17 : format == "hardcover"  → True / False
B5  line 19 : format == "paperback"  → True / False(else)
B6  line 32 : pages_missing > 0     → True / False
B7  line 36 : is_counterfeit         → True / False
B8  line 38 : format == "textbook" (inside counterfeit) → True / False
B9  line 42 : condition == "mint"    → True / False
B10 line 44 : condition == "poor"    → True / False(else)
B11 line 49 : payout_in_credit       → True / False
B12 line 54 : rejected_items > 4     → True / False
B13 line 56 : total_payout == 0.0   → True / False

Branch map for inspect_scanner_calibration
──────────────────────────────────────────
B14 line 62 : not scanner_matrix     → True / False
B15 line 68 : error_rate > 5         → True / False
B16 line 70 : misread_streak >= 2    → True / False
"""

import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


# ── B1 (True): invalid input raises ValueError ────────────────────────────
def test_b1_invalid_batches_type():
    with pytest.raises(ValueError):
        process_book_buybacks("oops", 5.0)


def test_b1_negative_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -0.01)


# ── B1 (False) + B2 (False): valid call, batch not approved ───────────────
def test_b2_false_batch_not_approved():
    batches = [{"intake_approved": False, "format": "paperback", "payout_in_credit": False, "books": []}]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "ZERO_CREDIT"


# ── B2 (True) + B3 (True): textbook format ────────────────────────────────
def test_b3_true_textbook_format():
    batches = [{
        "intake_approved": True, "format": "textbook",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 40.0


# ── B3 (False) + B4 (True): hardcover format ──────────────────────────────
def test_b4_true_hardcover_format():
    batches = [{
        "intake_approved": True, "format": "hardcover",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 15.0


# ── B4 (False) + B5 (True): paperback format ──────────────────────────────
def test_b5_true_paperback_format():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0


# ── B5 (False/else): unknown/unsupported format ───────────────────────────
def test_b5_false_unknown_format():
    batches = [{
        "intake_approved": True, "format": "audio",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "ZERO_CREDIT"


# ── B6 (True): missing pages → book rejected ──────────────────────────────
def test_b6_true_missing_pages():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [{"missing_pages": 5, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "ZERO_CREDIT"


# ── B6 (False): no missing pages ──────────────────────────────────────────
def test_b6_false_no_missing_pages():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0


# ── B7 (True) + B8 (False): counterfeit non-textbook ─────────────────────
def test_b7_true_b8_false_counterfeit_paperback():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [
            {"missing_pages": 0, "condition": "good", "counterfeit": True},
            {"missing_pages": 0, "condition": "good", "counterfeit": False},
        ]
    }]
    result = process_book_buybacks(batches, 0.0)
    # first book: counterfeit → 0; second: 8.0
    assert result["total_payout"] == 8.0


# ── B7 (True) + B8 (True): counterfeit textbook → batch zeroed + break ───
def test_b7_true_b8_true_counterfeit_textbook():
    batches = [{
        "intake_approved": True, "format": "textbook",
        "payout_in_credit": False,
        "books": [
            {"missing_pages": 0, "condition": "good", "counterfeit": False},
            {"missing_pages": 0, "condition": "good", "counterfeit": True},
            {"missing_pages": 0, "condition": "mint", "counterfeit": False},  # never reached
        ]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


# ── B7 (False) + B9 (True): mint condition ────────────────────────────────
def test_b9_true_mint_condition():
    batches = [{
        "intake_approved": True, "format": "hardcover",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == round(15.0 * 1.25, 2)


# ── B9 (False) + B10 (True): poor condition ───────────────────────────────
def test_b10_true_poor_condition():
    batches = [{
        "intake_approved": True, "format": "textbook",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "poor", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == round(40.0 * 0.40, 2)


# ── B10 (False/else): "good" and any other condition ─────────────────────
def test_b10_false_good_condition():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0


# ── B11 (True): payout_in_credit adds bonus ───────────────────────────────
def test_b11_true_credit_payout_adds_bonus():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": True,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 7.0)
    assert result["total_payout"] == 15.0   # 8 + 7


# ── B11 (False): cash payout – no bonus ──────────────────────────────────
def test_b11_false_no_credit_bonus():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 99.0)
    assert result["total_payout"] == 8.0


# ── B12 (True): > 4 rejected items → AUDIT_REJECTED ──────────────────────
def test_b12_true_audit_rejected():
    # 5 books with missing pages → 5 rejected items
    bad_books = [{"missing_pages": 1, "condition": "good", "counterfeit": False}] * 5
    good_book  = [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": bad_books + good_book,
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "AUDIT_REJECTED"


# ── B12 (False) + B13 (True): ≤ 4 rejected, total == 0 → ZERO_CREDIT ─────
def test_b13_true_zero_credit_status():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [{"missing_pages": 1, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "ZERO_CREDIT"
    assert result["total_payout"] == 0.0


# ── B12 (False) + B13 (False): normal completed payout ───────────────────
def test_b13_false_completed_payout():
    batches = [{
        "intake_approved": True, "format": "paperback",
        "payout_in_credit": False,
        "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    }]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "COMPLETED"


# ─────────────────────────────────────────────────────────────────────────────
# inspect_scanner_calibration branch coverage
# ─────────────────────────────────────────────────────────────────────────────

# ── B14 (True): empty matrix → NO_DATA ───────────────────────────────────
def test_b14_true_no_data_empty_matrix():
    assert inspect_scanner_calibration([]) == "NO_DATA"


# ── B14 (False): matrix has data ──────────────────────────────────────────
def test_b14_false_matrix_has_data():
    result = inspect_scanner_calibration([[1, 2]])
    assert result in ("CALIBRATED", "RECALIBRATE")


# ── B15 (True) + B16 (True): two consecutive high errors → RECALIBRATE ───
def test_b15_true_b16_true_recalibrate():
    assert inspect_scanner_calibration([[6, 8]]) == "RECALIBRATE"


# ── B15 (True) + B16 (False): one high error (streak < 2) ────────────────
def test_b15_true_b16_false_single_high():
    assert inspect_scanner_calibration([[6, 1, 1]]) == "CALIBRATED"


# ── B15 (False): all errors ≤ 5 ──────────────────────────────────────────
def test_b15_false_all_low_errors():
    assert inspect_scanner_calibration([[1, 2, 5], [3, 4]]) == "CALIBRATED"


# ── streak reset: high → low → high (no RECALIBRATE) ─────────────────────
def test_streak_resets_after_low_value():
    assert inspect_scanner_calibration([[7, 1, 7, 1]]) == "CALIBRATED"


# ── multi-device: first ok, second triggers RECALIBRATE ──────────────────
def test_second_device_triggers_recalibrate():
    matrix = [[1, 2, 3], [9, 10, 1]]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"
