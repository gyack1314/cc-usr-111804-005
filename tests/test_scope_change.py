"""门户目录换版后旧范围仍留在当前进度的基线行为。"""
import json
import tempfile
import unittest
from pathlib import Path
from capture_service.ledger import connect
from capture_service.progress import register,coverage

ROOT=Path(__file__).resolve().parents[1]

class ScopeChange(unittest.TestCase):
    def test_catalog_replacement_currently_keeps_old_scope(self):
        with tempfile.TemporaryDirectory() as directory:
            c=connect(Path(directory)/'state.sqlite3')
            original=json.loads((ROOT/'data'/'portal-sources.json').read_text(encoding='utf-8'))
            revised=json.loads((ROOT/'data'/'portal-sources-revised.json').read_text(encoding='utf-8'))
            register(c,'sample',original['sources'])
            register(c,'sample',revised['sources'])
            self.assertEqual(coverage(c,'sample')['expected'],2)
            c.close()
