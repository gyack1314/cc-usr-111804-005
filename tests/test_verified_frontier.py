"""初始卡片收据不等于门户业务关系闭合。"""
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.portal_workflow import collect_initial
from capture_service.progress import coverage
from capture_service.archive import release_verified

ROOT=Path(__file__).resolve().parents[1]

class VerifiedPortalFrontier(unittest.TestCase):
    def test_initial_card_is_unverified_until_other_source_arrives(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'state.sqlite3')
            collect_initial(c,'sample',ROOT/'data'/'portal.html')
            result=coverage(c,'sample')
            self.assertEqual(result['received'],1)
            self.assertEqual(len(result['unverified_required']),2)
            with self.assertRaises(ValueError):release_verified(c,'sample')
            c.close()

