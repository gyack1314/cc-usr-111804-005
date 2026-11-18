"""Collect the original stable portal scope into the existing source ledger."""
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from .ledger import receive
from .progress import record, receipts
from .view import overview

def collect_initial(connection, collection, page_path):
    """Save only the original scope; a selected scope needs separate validation."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(Path(page_path).resolve().as_uri())
            state = json.loads(page.locator('#state').inner_text())
            if state['phase'] != 'loaded' or state['scope'] != state['card_scope']:
                raise ValueError('页面卡片与当前范围不一致')
            declared = state['card'].get('page_scope', state['card'].get('card_scope',
                       state['card'].get('session', state['card'].get('configuration',
                       state['card'].get('store_id')))))
            if declared != state['scope']:
                raise ValueError('来源卡片与页面范围不一致')
            raw = json.dumps(state['card'], ensure_ascii=False, sort_keys=True).encode('utf-8')
            receipt = {'status': 200, 'url': page.url, 'body_sha256': hashlib.sha256(raw).hexdigest()}
            digest = receive(connection, collection, raw, receipt)
            record(connection, collection, state['scope'], digest, page.url)
        finally:
            browser.close()
    result = overview(connection, collection)
    result['portal_progress'] = receipts(connection, collection)
    return result
