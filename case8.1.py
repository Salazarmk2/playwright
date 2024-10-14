import os
from playwright.sync_api import Page, expect
from playwright.sync_api import Page, sync_playwright
import streamlit as st
#test:11185
def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots8.1"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def test_example(page: Page) -> None:
    try:

        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
        
    
        page.get_by_placeholder("someone@example.com").fill("ictqa@dayliff.com")
        page.get_by_role("button", name="Next").click()
        page.get_by_placeholder("Password").fill("P@s5VV0rD123!")
        page.get_by_role("button", name="Sign in").click()
        page.get_by_role("button", name="No").click()
        
        page.goto("https://bctest.dayliff.com/BC160/")
        
        # Interact with the Sales Role Center
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Sales Role Center").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Posted Sales Credit Memos,").click()

        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
        
        # Fill in search field
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").fill("11185")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 11185").click()
        
        # Click on Total Incl. VAT (UGX)
        Totalinc_locator= page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),")
        Totalinc_locator.dblclick()
        Totalinc_number = Totalinc_locator.inner_text()
        print(f"Total Inc vat extracted: {Totalinc_number}")
        b = Totalinc_number 

        # Handle invoice number interactions
        invoice_locator = page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,")
        
        take_screenshot(page, "after_invoice_number_extraction")
        invoice_locator.dblclick()  # Click to focus on the invoice number
        invoice_number = invoice_locator.inner_text()  # Get the invoice number text
        print(f"Invoice Number Extracted: {invoice_number}")  # Print the invoice number
        c = invoice_number  

        # Click multiple times to focus on the Invoice No.
        for _ in range(4):
            invoice_locator.click()

        # Navigate back
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Back").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Sales Invoices, Open").click()
        
        # Search for another invoice
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
        search_field = page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices")
        search_field.fill("204651")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 204651").click()
        
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_title("204651", exact=True).click()
        
        take_screenshot(page, "after_invoice_selection")

        print(c)
        print(b)

        if b == c:
            print("The values are equal.")
        else:
            print("The values are not equal.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        test_example(page)
        browser.close()

st.title("Invoice Search Automation")

if st.button("Run Invoice Search"):
    # Run the automation and get the screenshot
    screenshot_path = ""

    # Display the screenshot
    if os.path.exists(screenshot_path):
        st.image(screenshot_path, caption='Screenshot after Invoice Selection', use_column_width=True)
    else:
        st.error("Screenshot could not be created.")