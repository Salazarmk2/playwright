import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import Page, expect
import os
from playwright.sync_api import Page, sync_playwright

def take_screenshot(page, step_name):
    screenshot_dir = "screenshots13.1"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}.png")
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def run_playwright(email, password, invoice_number):
    with sync_playwright() as p:
        try:
            page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")
            

            page.get_by_placeholder("someone@example.com").click()

            page.get_by_placeholder("someone@example.com").fill(email)
            page.get_by_role("button", name="Next").click()

            page.get_by_placeholder("Password").click()
            page.get_by_placeholder("Password").fill(password)

            page.get_by_role("button", name="Sign in").click()
         
            page.goto("https://bctest.dayliff.com/BC160/")

        
            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Sales Role Center").click()
            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("menuitem", name="Posted Documents").click()
            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Posted Sales Credit Memos,").click()
            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_text("Search").click()

            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").click()
            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_placeholder("Search").fill(invoice_number)

            page.locator("iframe[title='Main Content']").locator(f"label:has-text({invoice_number})").click()

            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_role("button", name="Toggle FactBox").click()
            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Total Incl. VAT (UGX),").click()
            page.locator("iframe[title=\"Main Content\"]").content_frame.get_by_label("Invoice No.,").click()

            print("Test successfull")
        except Exception as e:
            print(f"An error occurred")
            take_screenshot(page, "error")  # Take a screenshot on error
        finally:
            browser.close()
        
def submit_form():
    email = email_entry.get()
    password = password_entry.get()
    invoice_number = invoice_entry.get()

    if not email or not password or not invoice_number:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    run_playwright(email, password, invoice_number)

root = tk.Tk()
root.title("Business Central Invoice Search")

# Create and place labels and entries
tk.Label(root, text="Email:").grid(row=0, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

tk.Label(root, text="Invoice Number:").grid(row=2, column=0)
invoice_entry = tk.Entry(root)
invoice_entry.grid(row=2, column=1)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=3, columnspan=2)

# Start the Tkinter event loop
root.mainloop()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        browser.close()
    

    