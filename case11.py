import re
from playwright.sync_api import Page, expect
from playwright.sync_api import Page, sync_playwright
import os

def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots11"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")


def test_example(page: Page) -> None:
    try:
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
        page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f&sso_reload=true")
        page.get_by_placeholder("someone@example.com").click()
        page.get_by_placeholder("someone@example.com").click(button="right")
        page.get_by_placeholder("someone@example.com").fill("ictqa@dayliff.com")
        page.get_by_role("button", name="Next").click()
        page.get_by_placeholder("Password").click(button="right")
        page.get_by_placeholder("Password").fill("P@s5VV0rD123!")
        page.get_by_role("button", name="Sign in").click()
        


        
        page.goto("https://bctest.dayliff.com/BC160/")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Posted Sales Credit Memos,").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("search").locator("div").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").fill("11175")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 11175").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").dblclick()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click(click_count=4)
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click(button="right")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.locator("div:nth-child(6) > div:nth-child(2) > .ms-nav-layout-main").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Back").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Sales Invoices, Open").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("UGANDA, Posted Documents, Posted Sales Invoices", exact=True).get_by_text("").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").click(button="right")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Search UGANDA, Posted Documents, Posted Sales Invoices").fill("203573")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 203573").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 203573").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 203573").click()
        page.goto("https://bctest.dayliff.com/BC160/?page=132&company=UGANDA&dc=0&bookmark=23%3bcAAAAAJ7BjIAMAAzADUANwAz")
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()
        page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Invoice Discount Amount Excl. VAT0.00Total Excl. VAT (UGX)219,491.52Total VAT (").click()
    
        print("test run successfully")
    except Exception as e:
        print(f"An error occurred: {e}")
        take_screenshot(page, "error")


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    test_example(page)
    browser.close()