import unittest
from datetime import date

from booking.service import BookingError
from tests.helpers import make_service

D = date


class TestService(unittest.TestCase):
    def setUp(self):
        self.svc, _ = make_service(self)

    def test_back_to_back_allowed(self):
        self.svc.book("R1", "ana", D(2026, 12, 1), D(2026, 12, 3))
        self.svc.book("R1", "budi", D(2026, 12, 3), D(2026, 12, 5))

    def test_overlap_rejected(self):
        self.svc.book("R1", "ana", D(2026, 12, 1), D(2026, 12, 3))
        with self.assertRaises(BookingError):
            self.svc.book("R1", "budi", D(2026, 12, 2), D(2026, 12, 4))

    def test_bad_dates(self):
        for a, b in [(D(2026, 12, 3), D(2026, 12, 3)), (D(2026, 12, 4), D(2026, 12, 3))]:
            with self.assertRaises(BookingError):
                self.svc.book("R1", "ana", a, b)

    def test_unknown_room(self):
        with self.assertRaises(BookingError):
            self.svc.book("R9", "ana", D(2026, 12, 1), D(2026, 12, 2))

    def test_capacity(self):
        with self.assertRaises(BookingError):
            self.svc.book("R1", "ana", D(2026, 12, 1), D(2026, 12, 2), guests=3)

    def test_cancel_unknown(self):
        with self.assertRaises(BookingError):
            self.svc.cancel(42)

    def test_ids_unique_after_cancel(self):
        a = self.svc.book("R1", "ana", D(2026, 12, 1), D(2026, 12, 2))
        b = self.svc.book("R1", "budi", D(2026, 12, 2), D(2026, 12, 3))
        self.svc.cancel(a.id)
        c = self.svc.book("R2", "citra", D(2026, 12, 1), D(2026, 12, 2))
        self.assertNotIn(c.id, (a.id, b.id))

    def test_available_rooms(self):
        r = self.svc.available_rooms(D(2026, 12, 1), D(2026, 12, 3))
        self.assertEqual(r, ["R1", "R2"])
        self.svc.book("R1", "ana", D(2026, 12, 2), D(2026, 12, 4))
        self.assertEqual(self.svc.available_rooms(D(2026, 12, 1), D(2026, 12, 3)), ["R2"])
        self.assertEqual(self.svc.available_rooms(D(2026, 12, 4), D(2026, 12, 6)), ["R1", "R2"])
        self.assertEqual(self.svc.available_rooms(D(2026, 12, 10), D(2026, 12, 11), guests=3), ["R2"])


if __name__ == "__main__":
    unittest.main()
