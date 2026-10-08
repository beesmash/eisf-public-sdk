import unittest

from eisf.conformance import run_internal_suite


class ConformanceTests(unittest.TestCase):
    def test_mandatory_suite(self):
        passed, total, _ = run_internal_suite()
        self.assertEqual((passed, total), (8, 8))


if __name__ == "__main__":
    unittest.main()
