import unittest
from game import Card, Desk, TRAY_Y, TRAY_W, WIDTH, CARD_W, CARD_H


class DeskTests(unittest.TestCase):
    def setUp(self):
        self.desk = Desk(seed=9)

    def test_airborne_card(self):
        self.assertFalse(self.desk.catches(Card(self.desk.x, 110, "Paper")))

    def test_adjacent_arrivals(self):
        self.desk.cards = [Card(self.desk.x, TRAY_Y - CARD_H, kind)
                           for kind in ("Grant", "Paper")]
        self.desk.file_cards()
        self.assertEqual(self.desk.filed, {"Grant": 1, "Paper": 1})
        self.assertEqual(self.desk.cards, [])

    def test_right_and_left_limits(self):
        for direction, limit in ((1, WIDTH - TRAY_W), (-1, 0)):
            for _ in range(160):
                self.desk.step(1 / 60, direction)
            self.assertEqual(self.desk.x, limit)

    def test_spawn_variation_and_limit(self):
        previous = None
        for _ in range(30):
            self.desk.spawn()
            self.assertNotEqual(self.desk.last_lane, previous)
            previous = self.desk.last_lane
            self.assertTrue(0 <= self.desk.cards[-1].x <= WIDTH - CARD_W)
        self.desk.cards = self.desk.cards[:5]
        self.desk.until_spawn = 0
        self.desk.step(1 / 30)
        self.assertEqual(len(self.desk.cards), 5)

    def test_boost_expires(self):
        self.desk.expedite()
        self.desk.step(0.1, 1)
        self.assertAlmostEqual(self.desk.x, (WIDTH - TRAY_W) / 2 + 51)
        for _ in range(100):
            self.desk.step(1 / 60)
        self.assertEqual(self.desk.boost, 0)
        self.desk.expedite()
        self.assertEqual(self.desk.boost, 0)

    def test_shift_ends_after_five_misses(self):
        self.desk.cards = [Card(0, 530, "Grant") for _ in range(5)]
        self.desk.file_cards()
        self.desk.step(0.05, 1)
        self.assertEqual(self.desk.missed, 5)
        self.assertEqual(self.desk.x, (WIDTH - TRAY_W) / 2)
