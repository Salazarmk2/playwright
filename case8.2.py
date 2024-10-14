import os
import streamlit as st
from playwright.sync_api import Page, sync_playwright

# Function to take a screenshot
def take_screenshot(page: Page, step_name: str) -> None:
    """Takes a screenshot of the current page."""
    screenshot_dir = "screenshots8"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    st.write(f"Screenshot taken: {screenshot_path}")

# Function to perform the main automation tasks
def test_example(page: Page, url: str, email: str, password: str, search_term: str) -> None:
    try:
        # Go to the provided URL
        page.goto(url)
        
        # Fill in login details and submit
        page.fill("input[placeholder='someone@example.com']", email)
        page.click("button:has-text('Next')")
        page.fill("input[placeholder='Password']", password)
        page.click("button:has-text('Sign in')");
        page.click("button:has-text('No')");
        
        # Navigate to the desired page after login
        page.goto("https://bctest.dayliff.com/BC160/")
        
        # Interact with the Sales Role Center
        page.click("iframe[title='Main Content'] >> text=Sales Role Center")
        page.click("iframe[title='Main Content'] >> text=Posted Documents")
        page.click("iframe[title='Main Content'] >> text=Posted Sales Credit Memos,")
        page.click("iframe[title='Main Content'] >> text=Search")
        
        # Dynamically search for the term (Invoice Number)
        page.fill("iframe[title='Main Content'] >> input[placeholder='Search']", search_term)
        page.wait_for_timeout(2000)  # Allow time for search results to appear
        
        # Click on the first search result
        first_result = page.locator("iframe[title='Main Content'] >> tr").first
        first_result.click()
        
        # Extract relevant details from the first result
        Totalinc_locator = page.locator("iframe[title='Main Content'] >> text=Total Incl. VAT (UGX),")
        Totalinc_locator.dblclick()
        Totalinc_number = Totalinc_locator.inner_text()
        st.write(f"Total Inc VAT extracted: {Totalinc_number}")
        
        invoice_locator = page.locator("iframe[title='Main Content'] >> text=Invoice No.,")
        invoice_locator.dblclick()
        invoice_number = invoice_locator.inner_text()
        st.write(f"Invoice Number Extracted: {invoice_number}")
        
        take_screenshot(page, "after_first_result_click")
        
        # Perform further actions based on the extracted data
        if Totalinc_number == invoice_number:
            st.write("The values are equal.")
        else:
            st.write("The values are not equal.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        take_screenshot(page, "error")

# Streamlit app to get user inputs
st.title("Automated Business Central Interaction")

# Collect user inputs dynamically
url = st.text_input("Enter the Business Central URL", "https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
email = st.text_input("Enter your email", "ictqa@dayliff.com")
password = st.text_input("Enter your password", type="password")
search_term = st.text_input("Enter the Invoice Number",)

# Trigger Playwright automation when the button is clicked
if st.button("Run Automation"):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        test_example(page, url, email, password, search_term)
        browser.close()
