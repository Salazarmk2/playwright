import os
from playwright.sync_api import Page, sync_playwright

def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots8"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def click_and_get_value(page: Page, label: str) -> str:
    """Clicks on a label and returns its inner text."""
    locator = page.locator(f"iframe[title='Main Content'] >> text={label}")
    locator.click()
    return locator.inner_text().strip()  # Return stripped text

def test_example(page: Page) -> None:
    try:
        # Navigate to login page
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f&sso_reload=true")

        # Fill in credentials and log in
        page.locator("input[placeholder='someone@example.com']").fill("ictqa@dayliff.com")
        page.locator("button:has-text('Next')").click()
        page.locator("input[placeholder='Password']").fill("P@s5VV0rD123!")
        page.locator("button:has-text('Sign in')").click()
        page.locator("button:has-text('No')").click()

        # Navigate to the main application
        page.goto("https://bctest.dayliff.com/BC160/")
        
        # Interact with the Posted Documents
        page.locator("iframe[title='Main Content'] >> role=menuitem[name='Posted Documents']").click()
        page.locator("iframe[title='Main Content'] >> text='Posted Sales Credit Memos,'").click()
        page.locator("iframe[title='Main Content'] >> text=''").click()
        
        # Search for a specific document
        page.locator("iframe[title='Main Content'] >> placeholder='Search'").fill("10995")
        page.locator("iframe[title='Main Content'] >> label='No., 10995'").click()

        # Get Total Incl. VAT (first) and take a screenshot
        b1 = click_and_get_value(page, "Total Incl. VAT (UGX),")
        print(f"Total Incl. VAT (first) extracted: {b1}")
        take_screenshot(page, "total_incl_vat_first")

        # Interact with the Invoice Number
        invoice_locator = page.locator("iframe[title='Main Content'] >> label='Invoice No.,'")
        invoice_locator.dblclick()  # Double-click to focus

        # Click multiple times to focus on the Invoice No.
        for _ in range(4):
            invoice_locator.click()

        # Navigate back and clear search
        page.locator("iframe[title='Main Content'] >> role=button[name='Back']").click()
        page.locator("iframe[title='Main Content'] >> text='Clear search'").click()
        page.locator("iframe[title='Main Content'] >> role=menuitem[name='Posted Documents']").click()
        page.locator("iframe[title='Main Content'] >> role=menuitem[name='Posted Sales Invoices, Open']").click()
        
        # Search for another invoice
        page.locator("iframe[title='Main Content'] >> label='Search UGANDA, Posted Documents, Posted Sales Invoices'").fill("194615")
        page.locator("iframe[title='Main Content'] >> label='No., 194615'").click()

        # Get Total Incl. VAT (second) and take a screenshot
        b2 = click_and_get_value(page, "Total Incl. VAT (UGX),")
        print(f"Total Incl. VAT (second) extracted: {b2}")
        take_screenshot(page, "total_incl_vat_second")

        # Compare b1 and b2
        if b1 == b2:
            print("Total Incl. VAT values match.")
        else:
            print(f"Mismatched Total Incl. VAT values: b1 = {b1}, b2 = {b2}")

    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

# Running the test
if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        test_example(page)
        browser.close()

