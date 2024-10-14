import re
from playwright.sync_api import Page, sync_playwright

def test_example(page: Page) -> None:
   
    page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
    
   
    page.locator('[placeholder="someone@example.com"]').fill("ictqa@dayliff.com")
    page.locator('[role="button"][name="Next"]').click()
    page.screenshot(path="before_click.png")
    
    page.locator('[placeholder="Password"]').fill("P@s5VV0rD123!")
    page.locator('[role="button"][name="Sign in"]').click()
    page.locator('[role="button"][name="Yes"]').click()

    
    page.goto("https://bctest.dayliff.com/BC160/")
    
   
    frame = page.frame_locator('iframe[title="Main Content"]')

  
    frame.locator('[role="menuitem"][name="Posted Documents"]').click()

   
    frame.locator('[label="Posted Sales Credit Memos"]').click()

   
    frame.locator('[aria-label="Search"]').fill("10")

   
    page.goto("https://bctest.dayliff.com/BC160/?node=0000c51d-4792-0000-0c72-2500836bd2d2&page=144&company=UGANDA&dc=0&bookmark=21%3bcgAAAAJ7BTEAMQA3ADcANA%3d%3d")
    
    
    frame.locator('[placeholder="Search"]').fill("11095")
    frame.locator('[role="gridcell"][name="No., 11095"]').click()

    
    frame.locator('[role="button"][name="Adjustment Details"]').click()

  
    frame.locator('[title="17451"]').click()
    frame.locator('[role="gridcell"][name="Description, Invoice No."]').dblclick()

   
    frame.locator('[role="button"][name="Clear search"]').click()
    frame.locator('[label="Search UGANDA, Posted Documents, Posted Sales Invoices"]').fill("Invoice No. 201249")
    frame.locator('[role="button"][name="Clear search"]').click()

   
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    test_example(page)
    browser.close()
