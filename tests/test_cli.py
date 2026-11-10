import io
import unittest

from booking.cli import main
from tests.helpers import make_service


class TestCli(unittest.TestCase):
    def setUp(self):
        _, self.db = make_service(self)

    def run_cli(self, *args):
        buf = io.StringIO()
        code = main(["--db", self.db, *args], out=buf)
        return code, buf.getvalue()

    def test_book_and_available(self):
        code, out = self.run_cli("book", "R1", "ana", "2026-12-01", "2026-12-03")
        self.assertEqual((code, out), (0, "booked 1\n"))
        code, out = self.run_cli("available", "2026-12-01", "2026-12-03")
        self.assertEqual((code, out), (0, "R2\n"))
        code, out = self.run_cli("available", "2026-12-01", "2026-12-03", "--guests", "5")
        self.assertEqual((code, out), (0, ""))

    def test_quote(self):
        self.assertEqual(self.run_cli("quote", "R1", "2026-12-04", "2026-12-06"), (0, "250.00\n"))

    def test_errors_exit_1(self):
        self.run_cli("book", "R1", "ana", "2026-12-01", "2026-12-03")
        code, out = self.run_cli("book", "R1", "budi", "2026-12-02", "2026-12-04")
        self.assertEqual(code, 1)
        self.assertTrue(out.startswith("error: "), out)
        code, out = self.run_cli("cancel", "99")
        self.assertEqual(code, 1)
        self.assertTrue(out.startswith("error: "), out)
        code, out = self.run_cli("book", "R1", "ana", "2026-13-01", "2026-12-03")
        self.assertEqual(code, 1)
        self.assertTrue(out.startswith("error: "), out)


if __name__ == "__main__":
    unittest.main()
