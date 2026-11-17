"""本地页面状态转换可重复，不依赖外站。"""
import unittest
from pathlib import Path
from capture_service.browser_capture import inspect

class BrowserFixture(unittest.TestCase):
    def test_transition(self):
        states = inspect(Path(__file__).resolve().parents[1] / 'data' / 'portal.html')
        self.assertEqual([row['phase'] for row in states], ['loaded', 'pending', 'loaded'])
        self.assertNotEqual(states[0]['scope'], states[-1]['scope'])
        self.assertEqual(states[0]['card_scope'], states[1]['card_scope'])
        self.assertEqual(states[-1]['scope'], states[-1]['card_scope'])
