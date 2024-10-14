import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright
import os
import time

def take_screenshot(page, step_name):
    screenshot_dir = "screenshots13.0"
    os.makedirs(screenshot_dir, exist_ok=True)

    # Add a timestamp to make the filename unique
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(screenshot_dir, f"{step_name}_{timestamp}.png")
    
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken: {screenshot_path}")

def run_playwright(email, password, invoice_number):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to the login page
            page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")

            # Login steps
            page.get_by_placeholder("someone@example.com").click()
            page.get_by_placeholder("someone@example.com").fill(email)
            page.get_by_role("button", name="Next").click()

            page.get_by_placeholder("Password").click()
            page.get_by_placeholder("Password").fill(password)
            page.get_by_role("button", name="Sign in").click()

            # Navigate to the Business Central page
            page.goto("https://bctest.dayliff.com/BC160/")
            
            # Access the iframe
            frame = page.frame_locator("iframe[title='Main Content']").first
            
            # Perform actions within the iframe
            frame.get_by_label("Sales Role Center").click()
            frame.get_by_role("menuitem", name="Posted Documents").click()
            frame.get_by_label("Posted Sales Credit Memos,").click()
            frame.get_by_text("Search").click()
            
            # Search for the invoice number
            frame.get_by_placeholder("Search").click()
            frame.get_by_placeholder("Search").fill(invoice_number)
            frame.get_by_role("button", name=f"No., {invoice_number}").click()
                      
            
            # Extract data
            frame.get_by_role("button", name="Toggle FactBox").click()
            frame.get_by_label("Total Incl. VAT (UGX),").click()
            incl_vat1 = frame.get_by_label("Total Incl. VAT (UGX),").text_content()
            
            # Print the value to verify
            print(f"Total Incl. VAT value: {incl_vat1}")

            # Take a screenshot after the click action
            take_screenshot(page, "1total_incl_vat_clicked")
            
            frame.get_by_label("Invoice No.,").click()
            inv_no2 = frame.get_by_label("Invoice No.,").text_content()

            # Print the value to verify
            print(f"Invoice Number: {inv_no2}")

            page.goto("https://bctest.dayliff.com/BC160/?node=0000c51d-c39c-0000-0c41-d500836bd2d2&page=143&company=UGANDA&dc=0&bookmark=23%3bcAAAAAJ7BjIAMwAwADcAMQA3")

            frame.get_by_text("Search").click()  # Click the search icon or button
            frame.get_by_placeholder("Search").click()  # Click the search input
            frame.get_by_placeholder("Search").fill(inv_no2)  # Fill the search input with variable b
            frame.get_by_role("button", name=f"No., {inv_no2}").click()  # Click the button corresponding to the search term

            frame.get_by_role("button", name="Toggle FactBox").click()
            take_screenshot(page, "toggle_factbox_clicked") 

            # Click the label to bring up the value
            label = frame.get_by_label("Total Incl. VAT (UGX),")
            label.click()
            take_screenshot(page, "2total inc")  

            # Extract the value of the label and assign it to variable c
            incl_vat2 = label.inner_text()  
            print(f'Extracted value: {incl_vat2}')  

            print("Test successful")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            take_screenshot(page, "error")  # Take a screenshot on error
        
        
            browser.close()
        finally:
            if incl_vat1 is None or incl_vat2 is None:
                if incl_vat1 is None and incl_vat2 is None:
                    print("Both values are missing.")
                elif incl_vat1 is None:
                    print("Invoice number is missing.")
                else:
                    print("Total Incl. VAT value is missing.")
            else:
                if incl_vat1 == incl_vat2:
                    print("The values are equal.")
                else:
                    print("The values are not equal.")   
             

def submit_form():
    email = email_entry.get()
    password = password_entry.get()
    invoice_number = invoice_entry.get()

    if not email or not password or not invoice_number:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    run_playwright(email, password, invoice_number)

# Create the GUI
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
