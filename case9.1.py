import os
import json
from playwright.sync_api import Page, sync_playwright

def take_screenshot(page: Page, step_name: str) -> None:
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def load_config(filepath: str) -> dict:
    with open(filepath) as f:
        return json.load(f)

def get_label_selector(label_name: str) -> str:
    return f"iframe[title='Main Content'] >> label:has-text('{label_name}')"

def click_with_retry(locator, retries=3):
    for attempt in range(retries):
        try:
            locator.click()
            return
        except Exception:
            if attempt == retries - 1:
                raise

def test_example(page: Page, config: dict) -> None:
    try:
        page.goto(config['login_url'])
        page.get_by_placeholder("someone@example.com").fill(config['username'])
        page.get_by_placeholder("Password").fill(config['password'])
        page.get_by_role("button", name="Sign in").click()
        page.goto(config['base_url'])

        frame = page.locator("iframe[title='Main Content']").content_frame()
        frame.get_by_role("menuitem", name="Posted Documents").click()

        # Example usage of dynamic selectors
        invoice_no_1 = config['invoice_no_1']
        frame.get_by_label(f"No., {invoice_no_1}").click()
        
        # Get total incl VAT dynamically
        b1 = frame.locator(get_label_selector("Total Incl. VAT (UGX),")).inner_text()
        print(f"Total Incl. VAT (first) extracted: {b1}")
        take_screenshot(page, "total_incl_vat_first")

        # Handle additional steps...
        
    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        config = load_config('config.json')
        test_example(page, config)
        browser.close()
