"""门户初始范围已采，切换后的待采范围与页面修订可追踪。"""
import json
import unittest
from pathlib import Path
from capture_service.browser_capture import inspect

ROOT=Path(__file__).resolve().parents[1]

class PortalRevision(unittest.TestCase):
    def test_selected_scope_has_distinct_version(self):
        states=inspect(ROOT/'data'/'portal.html')
        sources=json.loads((ROOT/'data'/'portal-sources.json').read_text(encoding='utf-8'))['sources']
        self.assertEqual(len(sources),2)
        self.assertEqual(states[1]['scope'],sources[1]['scope'])
        self.assertEqual(states[1]['card_scope'],sources[0]['scope'])
        self.assertEqual(states[-1]['card_scope'],sources[1]['scope'])
        self.assertEqual(states[-1]['card']['revision'],'v2')
        self.assertEqual(states[-1]['card']['kind'],sources[1]['kind'])
