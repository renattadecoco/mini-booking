import unittest
from datetime import date

from booking.service import BookingService
from booking.storage import Storage
from tests.helpers import make_service

D = date


class TestStorage(unittest.TestCase):
    def test_round_trip(self):
        svc, path = make_service(self)
        svc.book("R1", "ana", D(2026, 12, 1), D(2026, 12, 3))
        s2 = Storage(path)
        self.assertEqual(len(s2.bookings), 1)
        self.assertEqual(s2.bookings[0].check_in, D(2026, 12, 1))
        self.assertIsInstance(s2.bookings[0].check_out, date)
        self.assertEqual(sorted(s2.rooms), ["R1", "R2"])

    def test_cancel_persisted(self):
        svc, path = make_service(self)
        b = svc.book("R1", "ana", D(2026, 12, 1), D(2026, 12, 3))
        svc.cancel(b.id)
        self.assertEqual(Storage(path).bookings, [])

    def test_ids_not_reused_after_reload(self):
        svc, path = make_service(self)
        a = svc.book("R1", "ana", D(2026, 12, 1), D(2026, 12, 3))
        svc.book("R2", "budi", D(2026, 12, 1), D(2026, 12, 3))
        svc.cancel(a.id)
        svc2 = BookingService(Storage(path))
        c = svc2.book("R1", "citra", D(2026, 12, 5), D(2026, 12, 6))
        self.assertEqual(c.id, 3)


if __name__ == "__main__":
    unittest.main()
