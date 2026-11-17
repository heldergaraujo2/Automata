import tempfile
import unittest
from pathlib import Path
from automata.state import connect, start_cycle, finish_cycle

class StateTests(unittest.TestCase):
    def test_cycle_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            with connect(Path(tmp) / "state.sqlite3") as db:
                cid = start_cycle(db)
                finish_cycle(db, cid, {"queued": 2, "failed": 0}, "completed")
                row = db.execute("SELECT status,queued,failed FROM cycles WHERE id=?", (cid,)).fetchone()
                self.assertEqual(row, ("completed", 2, 0))

if __name__ == "__main__":
    unittest.main()
