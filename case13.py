import re
from playwright.sync_api import Page, expect
import os
from playwright.sync_api import Page, sync_playwright

def test_example(page: Page) -> None:
    try:
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f&sso_reload=true")
        page.get_by_placeholder("someone@example.com").click()
        page.get_by_placeholder("someone@example.com").fill("ictqa@dayliff.com")
        page.get_by_role("button", name="Next").click()
        page.get_by_placeholder("Password").click()
        page.get_by_placeholder("Password").fill("P@s5VV0rD123!")
        page.get_by_role("button", name="Sign in").click()
        page.get_by_role("button", name="No").click()
        page.goto("https://bctest.dayliff.com/BC160/")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Sales Role Center").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Posted Sales Credit Memos,").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").fill("11185")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 11185").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click()



        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click(click_count=3)
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click(button="right")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Back").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Sales Invoices, Open").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").click(button="right")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").fill("204651")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 204651").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.locator("#b23s").click()


        #page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()


        print("Test successfull")
    except Exception as e:
        print(f"An error occurred")



        

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        test_example(page)
        browser.close()
