"""读取本地演练页面的当前可见状态。"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

def inspect(page_path):
    url = Path(page_path).resolve().as_uri()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        states = [json.loads(page.locator('#state').inner_text())]
        page.get_by_role('button', name='切换').click()
        states.append(json.loads(page.locator('#state').inner_text()))
        page.wait_for_function('JSON.parse(document.querySelector("#state").textContent).phase === "loaded"')
        states.append(json.loads(page.locator('#state').inner_text()))
        browser.close()
        return states

if __name__ == '__main__':
    import sys
    print(json.dumps(inspect(sys.argv[1]), ensure_ascii=False, indent=2))
