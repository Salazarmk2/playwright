import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
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
    page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Posted Sales Invoices, Open").click()
    page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()
    page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").click()
    page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("No., 230717").click()
    page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()
    page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()
