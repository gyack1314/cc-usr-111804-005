"""初始门户采集接入账本与持久进度。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.portal_workflow import collect_initial

ROOT = Path(__file__).resolve().parents[1]

class PortalWorkflow(unittest.TestCase):
    def test_initial_capture_survives_reopen_without_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'capture.sqlite3'
            db = connect(path)
            first = collect_initial(db, '111804-005', ROOT / 'data' / 'portal.html')
            self.assertEqual(len(first['records']), 1)
            self.assertEqual(len(first['portal_progress']), 1)
            self.assertEqual(first['records'][0]['source_sha256'], first['portal_progress'][0]['body_sha256'])
            db.close()
            db = connect(path)
            resumed = collect_initial(db, '111804-005', ROOT / 'data' / 'portal.html')
            self.assertEqual(len(resumed['records']), 1)
            self.assertEqual(len(resumed['portal_progress']), 1)
            db.close()
