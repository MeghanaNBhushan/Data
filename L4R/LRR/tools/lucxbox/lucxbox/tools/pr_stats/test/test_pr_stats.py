""" Test for a pr_stats """

import unittest
import lucxbox.tools.pr_stats.pr_stats as pr_stats


class TestPrStats(unittest.TestCase):
    def test_main(self):
        with self.assertRaises(SystemExit):
            pr_stats.main()


if __name__ == "__main__":
    unittest.main()
