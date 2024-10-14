import os
from playwright.sync_api import Page, sync_playwright

def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def test_example(page: Page, invoice_number: str) -> None:
    try:
        # Navigate to the login page
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
        
        # Fill in login credentials
        page.get_by_placeholder("someone@example.com").fill("ictqa@dayliff.com")
        page.get_by_role("button", name="Next").click()
        page.get_by_placeholder("Password").fill("P@s5VV0rD123!")
        page.get_by_role("button", name="Sign in").click()
        page.get_by_role("button", name="No").click()

        # Navigate to the main page
        page.goto("https://bctest.dayliff.com/BC160/")
        
        # Interact with the Posted Sales Credit Memos
        page.locator("iframe[title=\"Main Content\"]").content_frame().get_by_label("Posted Sales Credit Memos,").click()
        
        # Search for the invoice dynamically
        page.locator("iframe[title=\"Main Content\"]").content_frame().get_by_placeholder("Search").fill(invoice_number)
        page.locator(f"iframe[title=\"Main Content\"]").content_frame().get_by_label(f"No., {invoice_number}").click()
        
        # Extract Total Incl. VAT
        Totalinc_locator = page.locator("iframe[title=\"Main Content\"]").content_frame().get_by_label("Total Incl. VAT (UGX),")
        Totalinc_locator.dblclick()
        total_inc_vat = Totalinc_locator.inner_text()
        print(f"Total Incl. VAT extracted: {total_inc_vat}")

        # Extract Invoice No.
        invoice_locator = page.locator("iframe[title=\"Main Content\"]").content_frame().get_by_label("Invoice No.,")
        invoice_locator.dblclick()
        invoice_no_extracted = invoice_locator.inner_text()
        print(f"Invoice Number Extracted: {invoice_no_extracted}")

        # Perform comparison
        if total_inc_vat == invoice_no_extracted:
            print("The values are equal.")
        else:
            print("The values are not equal.")

        # Take screenshot
        take_screenshot(page, "after_invoice_selection")

    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

if __name__ == "__main__":
    invoice_to_search = "11175"  
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        test_example(page)
        browser.close()
