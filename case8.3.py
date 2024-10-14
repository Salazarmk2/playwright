import os
import streamlit as st
from playwright.sync_api import sync_playwright, Page

def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots8.3"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def test_example(page: Page) -> None:
    try:
        # Navigate to the login page
        page.goto("https://login.microsoftonline.com/dayliffcloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffcloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fbc160%2fsignin%3freturnurl%3d%252fbc160%252f")

        # Fill in credentials and login
        page.get_by_placeholder("someone@example.com").fill("ictqa@dayliff.com")
        page.get_by_role("button", name="next").click()
        page.get_by_placeholder("password").fill("p@s5vv0rd123!")
        page.get_by_role("button", name="sign in").click()
        page.get_by_role("button", name="no").click()

        page.goto("https://bctest.dayliff.com/bc160/")

        # Interact with the sales role center
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_label("sales role center").click()
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_role("menuitem", name="posted documents").click()
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_label("posted sales credit memos,").click()

        # Searching for an invoice
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_text("search").click()
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_placeholder("search").fill("11185")
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_label("no., 11185").click()

        totalinc_locator = page.locator("iframe[title=\"main content\"]").content_frame.get_by_label("total incl. vat (ugx),")
        totalinc_locator.dblclick()
        totalinc_number = totalinc_locator.inner_text()
        print(f"Total inc VAT extracted: {totalinc_number}")

        invoice_locator = page.locator("iframe[title=\"main content\"]").content_frame.get_by_label("invoice no.,")
        take_screenshot(page, "after_invoice_number_extraction")
        invoice_locator.dblclick()
        invoice_number = invoice_locator.inner_text()
        print(f"Invoice number extracted: {invoice_number}")

        # Back navigation
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_role("button", name="back").click()
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_role("menuitem", name="posted documents").click()
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_role("menuitem", name="posted sales invoices, open").click()

        # Another search after going back
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_text("search").click()
        search_field = page.locator("iframe[title=\"main content\"]").content_frame.get_by_label("search uganda, posted documents, posted sales invoices")
        search_field.fill("204651")
        page.locator("iframe[title=\"main content\"]").content_frame.get_by_label("no., 204651").click()

        page.locator("iframe[title=\"main content\"]").content_frame.get_by_title("204651", exact=True).click()

        take_screenshot(page, "after_invoice_selection")

        print(invoice_number, totalinc_number)
        # Here you could check the values if needed

    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

# Streamlit UI
st.title("Invoice Search Automation")

if st.button("Run Invoice Search"):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        test_example(page)
        browser.close()

    # After running, list the screenshots generated
    if os.path.exists("screenshots8.3"):
        screenshot_files = os.listdir("screenshots8.3")
        for screenshot_file in screenshot_files:
            if screenshot_file.endswith(".png"):
                st.image(os.path.join("screenshots8.3", screenshot_file), caption=screenshot_file, use_column_width=True)