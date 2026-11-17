import tempfile
import unittest
from pathlib import Path
from automata.analytics import summarize_ledger

class AnalyticsTests(unittest.TestCase):
    def test_only_approved_commissions_count(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "ledger.csv"
            file.write_text("type,status,amount_brl\ncommission,pending,100\ncommission,approved,25.50\nexpense,paid,5.25\n", encoding="utf-8")
            result = summarize_ledger(file)
            self.assertEqual(result["net_brl"], "20.25")

if __name__ == "__main__":
    unittest.main()
