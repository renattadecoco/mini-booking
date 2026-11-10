import unittest
from datetime import date
from decimal import Decimal

from booking.models import Room
from booking.pricing import quote

D = date
R1 = Room("R1", "Standard", "100.00", 2)


class TestPricing(unittest.TestCase):
    def test_weekdays(self):  # Tue + Wed
        q = quote(R1, D(2026, 12, 1), D(2026, 12, 3))
        self.assertEqual(q, Decimal("200.00"))
        self.assertIsInstance(q, Decimal)

    def test_weekend(self):  # Fri + Sat
        self.assertEqual(quote(R1, D(2026, 12, 4), D(2026, 12, 6)), Decimal("250.00"))

    def test_sunday_is_normal(self):
        self.assertEqual(quote(R1, D(2026, 12, 6), D(2026, 12, 7)), Decimal("100.00"))

    def test_long_stay(self):  # Tue..Mon, 7 nights, 2 weekend nights
        self.assertEqual(quote(R1, D(2026, 12, 1), D(2026, 12, 8)), Decimal("675.00"))

    def test_rounding(self):
        r = Room("X", "x", "99.99", 1)
        self.assertEqual(quote(r, D(2026, 12, 4), D(2026, 12, 5)), Decimal("124.99"))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            quote(R1, D(2026, 12, 3), D(2026, 12, 3))


if __name__ == "__main__":
    unittest.main()
