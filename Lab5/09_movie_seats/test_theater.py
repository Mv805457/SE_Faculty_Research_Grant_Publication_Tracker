import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import theater_system as theater


class TheaterTests(unittest.TestCase):
    def setUp(self):
        self.patch = patch.dict(theater.shows, {"A":{"title":"Demo","seats":3,"booked":[]}}, clear=True)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_boundaries_and_replay(self):
        logs = []
        self.assertTrue(theater.reserve_seat("A", 3, logs))
        for seat in [3, 0, -1, 4, "2", True]:
            self.assertFalse(theater.reserve_seat("A",seat,logs))
        self.assertFalse(theater.reserve_seat("unknown",1))
        self.assertEqual(theater.shows["A"]["booked"], [3])
        self.assertEqual(len(logs), 7)

    def test_release(self):
        theater.reserve_seat("A",1)
        self.assertFalse(theater.release_seat("A",True))
        self.assertTrue(theater.release_seat("A",1))
        self.assertFalse(theater.release_seat("A",1))

    def test_round_trip_and_invalid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"seats.json"
            theater.reserve_seat("A",2)
            theater.dump_reservations(path)
            theater.release_seat("A",2)
            theater.load_reservations(path)
            self.assertEqual(theater.shows["A"]["booked"],[2])
            path.write_text(json.dumps({"A":{"title":"Demo","seats":3,"booked":[9]}}))
            with self.assertRaises(ValueError):
                theater.load_reservations(path)
            self.assertEqual(theater.shows["A"]["booked"],[2])

    def test_ticket_reference(self):
        self.assertEqual(theater.ticket_code("A",1),theater.ticket_code("A",1))
        self.assertNotEqual(theater.ticket_code("A1",2),theater.ticket_code("A",12))
