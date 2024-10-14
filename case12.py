import re
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
    #login
    try:
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f&sso_reload=true")
        page.get_by_placeholder("someone@example.com").click()
        page.get_by_placeholder("someone@example.com").click()
        page.get_by_placeholder("someone@example.com").fill(email)
        page.get_by_role("button", name="Next").click()
        page.get_by_role("heading", name="Enter password").click()
        page.get_by_placeholder("Password").click()
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Sign in").click()
        page.goto("https://bctest.dayliff.com/BC160/")
        #End of Login

        #Interact with the Sales Role Center:get posted sales invoice
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Posted Sales Credit Memos,").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").click()
        #Send user input:posted sales credit memo
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").fill(invoice_number)#take user inputed invoice number 

        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Customer Name, SANCTUM HOTEL").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Sell-to Customer No.,").click()

        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 11175").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()

        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()
        #take screenshot after above action
        page.screenshot(path="screenshot_after_click.png")

        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click()
        #get invoice N.O by reading label clicked
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").dblclick()
        
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click(button="right")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Back").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Sales Invoices, Open").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").click(button="right")

        #fill searchbar with invoice number retrieved by clickinging label
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").fill("203573")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 203573").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()

        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            test_example(page)
            browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")

st.title("Invoice Search Automation")
email = st.text_input("Enter Email:")
password = st.text_input("Enter Password:", type="password")
invoice_number = st.text_input("Enter Invoice Number:")


if st.button("Run Invoice Search"):

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        test_example(page)
        browser.close()