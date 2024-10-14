import os
from playwright.sync_api import Page, expect
from playwright.sync_api import Page, sync_playwright
import streamlit as st

def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots12"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def test_example(page: Page, email: str, password: str, invoice_number: str) -> None:
    """Automates the invoice search process."""
    try:
        # Login
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f&sso_reload=true")
        
        page.get_by_placeholder("someone@example.com").fill(email)
        page.get_by_role("button", name="Next").click()
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Sign in").click()
        page.goto("https://bctest.dayliff.com/BC160/")

        # Interact with the Sales Role Center: get posted sales invoice
        # Use page instead of frame
        page.locator("iframe[title='Main Content']").wait_for_element_state("attached")  # Wait for the iframe to load
        page.locator("iframe[title='Main Content']").content_frame().get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_label("Posted Sales Credit Memos,").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_placeholder("Search").fill(invoice_number)  # Fill user inputted invoice number

        page.locator("iframe[title='Main Content']").content_frame().get_by_label("Customer Name, SANCTUM HOTEL").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_label("No., 11175").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_role("button", name="Toggle FactBox").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_label("Total Incl. VAT (UGX),").click()

        # Take screenshot after clicking
        take_screenshot(page, "after_click")

        page.locator("iframe[title='Main Content']").content_frame().get_by_label("Invoice No.,").click(button="right")
        page.locator("iframe[title='Main Content']").content_frame().get_by_role("button", name="Back").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_role("menuitem", name="Posted Sales Invoices, Open").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_placeholder("Search").click()

        # Fill searchbar with invoice number retrieved by clicking the label
        page.locator("iframe[title='Main Content']").content_frame().get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").fill("203573")
        page.locator("iframe[title='Main Content']").content_frame().get_by_label("No., 203573").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_role("button", name="Toggle FactBox").click()
        page.locator("iframe[title='Main Content']").content_frame().get_by_label("Total Incl. VAT (UGX),").click()

    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

# Streamlit UI
st.title("Invoice Search Automation")
email = st.text_input("Enter Email:")
password = st.text_input("Enter Password:", type="password")  # Mask the password
invoice_number = st.text_input("Enter Invoice Number:")

if st.button("Run Invoice Search"):
    if not email or not password or not invoice_number:
        st.error("Please enter all fields: Email, Password, and Invoice Number.")
    else:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            test_example(page, email, password, invoice_number)  # Pass all user inputs to the function
            browser.close()
