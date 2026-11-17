"""Regression cases for the grant claim reviewer."""
import unittest

from expense_review import review


class ReviewTests(unittest.TestCase):
    def test_exact_cap(self):
        result = review(100, [{"invoice": "A", "paise": 100}])
        self.assertEqual(result["remaining_paise"], 0)
        self.assertEqual(result["approved"], ["A"])

    def test_replay(self):
        result = review(100, [{"invoice": "A", "paise": 20},
                              {"invoice": " a ", "paise": 20}])
        self.assertEqual(result["remaining_paise"], 80)
        self.assertEqual(result["rejected"], [{"row": 2, "reason": "duplicate invoice"}])

    def test_bad_amounts_preserve_funds(self):
        for amount in [-10, 0, True, 2.5, "10", None]:
            with self.subTest(amount=amount):
                result = review(100, [{"invoice": "A", "paise": amount}])
                self.assertEqual(result["remaining_paise"], 100)
                self.assertEqual(result["rejected"][0]["reason"], "invalid amount")

    def test_bad_invoice_can_be_corrected(self):
        claims = [None, {"paise": 2}, {"invoice": " ", "paise": 2},
                  {"invoice": "B", "paise": 101}, {"invoice": "B", "paise": 99}]
        result = review(100, claims)
        self.assertEqual(result["approved"], ["B"])
        self.assertEqual(result["remaining_paise"], 1)
        self.assertEqual([r["reason"] for r in result["rejected"]],
                         ["invalid claim", "missing invoice", "missing invoice", "over budget"])

    def test_empty(self):
        self.assertEqual(review(0, []), {"remaining_paise": 0, "approved": [], "rejected": []})

    def test_invalid_batch(self):
        for cap, claims in [(-1, []), (True, []), ("100", []), (100, None)]:
            with self.subTest(cap=cap, claims=claims), self.assertRaises(ValueError):
                review(cap, claims)
