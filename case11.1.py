import os
import streamlit as st
from playwright.sync_api import Page, sync_playwright

def take_screenshot(page: Page, step: int) -> str:
    screenshot_path = f"screenshots/screenshot_{step}.png"
    page.screenshot(path=screenshot_path)
    return screenshot_path

def test_example(page: Page) -> list:
    os.makedirs("screenshots", exist_ok=True)  # Ensure the screenshots directory exists

    actions = 0
    screenshot_paths = []

    page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f&sso_reload=true")
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    page.get_by_placeholder("someone@example.com").click()
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    page.get_by_placeholder("someone@example.com").fill("ictqa@dayliff.com")
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    page.get_by_role("button", name="Next").click()
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    page.get_by_placeholder("Password").fill("P@s5VV0rD123!")
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    page.get_by_role("button", name="Sign in").click()
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    page.goto("https://bctest.dayliff.com/BC160/")
    actions += 1
    if actions % 4 == 0:
        screenshot_paths.append(take_screenshot(page, actions))

    print("Test run successful")
    return screenshot_paths  # Return the paths of the screenshots taken

def main():
    st.title("Playwright Screenshot Viewer")
    
    if st.button("Run Playwright Test"):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            screenshot_paths = test_example(page)
            browser.close()

        # Display the screenshots
        if screenshot_paths:
            st.write("Screenshots taken during the test run:")
            for screenshot in screenshot_paths:
                st.image(screenshot, caption=os.path.basename(screenshot), use_column_width=True)
        else:
            st.write("No screenshots found.")

if __name__ == "__main__":
    main()
