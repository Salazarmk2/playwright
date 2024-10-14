import os
from playwright.sync_api import Page, sync_playwright

def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots3"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def test_example(page: Page) -> None:
    try:
        # Navigate to the login page
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
        
        # Sign in
        page.get_by_placeholder("someone@example.com").fill("")
        page.get_by_role("button", name="Next").click()
        page.get_by_placeholder("Password").fill("")
        page.get_by_role("button", name="Sign in").click()
        page.get_by_role("button", name="Yes").click()
        
        # Navigate to main page
        page.goto("https://bctest.dayliff.com/BC160/")
        
        # Interact with posted documents
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Posted Sales Credit Memos,").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
        
        # Fill in search field
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").fill("10995")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 10995").click()
        
        # Extract text from invoice number
        invoice_number = page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").inner_text()
        print(f"Invoice Number Extracted: {invoice_number}")
        c = invoice_number

        # Take screenshot after search
        take_screenshot(page, "after_search_results")
        
        # Navigate back and clear search
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Back").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Clear search").click()

        # Further interactions
        # Access the iframe's content first, then perform actions inside it
        page.frame_locator("iframe[title=\"Main Content\"]").get_by_role("menuitem", name="Posted Sales Invoices, Open").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("UGANDA, Posted Documents, Posted Sales Invoices", exact=True).get_by_text("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").fill("194657")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 194657").click()
        
        # Navigate back again
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Back").click()
        
        print(c)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

# Running the test
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    test_example(page)
    browser.close()
