from playwright.sync_api import sync_playwright
import tkinter as tk
from tkinter import messagebox, Listbox, Frame, scrolledtext, END

def take_screenshot(page, invoice_number, prefix=""):
    """Take a screenshot and save it with a specified prefix."""
    filename = f"{prefix}invoice_{invoice_number}_screenshot.png"
    page.screenshot(path=filename)
    print(f"Screenshot saved: {filename}")

def extract_invoice_data(frame, invoice_number):
    """Extract the Total Incl. VAT and Invoice No from the given frame."""
    frame.get_by_role("button", name="Toggle FactBox").click()
    incl_vat = frame.get_by_label("Total Incl. VAT (UGX),").text_content()
    invoice_no = frame.get_by_label("Invoice No.,").text_content()
    return incl_vat, invoice_no

def run_playwright(email, password, invoice_number):
    """Main function to run Playwright and extract invoice data."""
    result = ""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to the login page
            page.goto("https://login.microsoftonline.com/dayliffCloud.onmicrosoft.com/wsfed?wa=wsignin1.0&wtrealm=https%3a%2f%2fdayliffCloud.onmicrosoft.com%2fbusinesscentral&wreply=https%3a%2f%2fbctest.dayliff.com%2fBC160%2fSignIn%3fReturnUrl%3d%252fBC160%252f")

            # Login steps
            page.get_by_placeholder("someone@example.com").fill(email)
            page.get_by_role("button", name="Next").click()
            page.get_by_placeholder("Password").fill(password)
            page.get_by_role("button", name="Sign in").click()

            # Navigate to Business Central
            page.goto("https://bctest.dayliff.com/BC160/")
            frame = page.frame_locator("iframe[title='Main Content']").first

            # Search for the first invoice number
            frame.get_by_label("Sales Role Center").click()
            frame.get_by_role("menuitem", name="Posted Documents").click()
            frame.get_by_label("Posted Sales Credit Memos,").click()
            frame.get_by_text("Search").click()
            frame.get_by_placeholder("Search").fill(invoice_number)
            frame.get_by_role("button", name=f"No., {invoice_number}").click()

            # Extract data for the first invoice
            incl_vat1, invoice2 = extract_invoice_data(frame, invoice_number)
            take_screenshot(page, invoice_number)

            # Search for the second invoice number
            frame.get_by_label("Sales Role Center").click()
            frame.get_by_role("menuitem", name="Posted Documents").click()
            frame.get_by_label("Posted Sales Invoices, Open").click()
            frame.get_by_text("Search").click()
            frame.get_by_placeholder("Search").fill(invoice2)     
            frame.get_by_role("button", name=f"No., {invoice2}").click()

            # Extract the Total Incl. VAT for invoice2
            incl_vat2, _ = extract_invoice_data(frame, invoice2)
            take_screenshot(page, invoice2)

            # Compare the two values
            if incl_vat1 == incl_vat2:
                result = f"Invoices match: Both Invoice No: {invoice_number} and Invoice No: {invoice2} have Total Incl. VAT: {incl_vat1}"
            else:
                result = f"Invoices do not match: Invoice No: {invoice_number} Total Incl. VAT: {incl_vat1}, Invoice No: {invoice2} Total Incl. VAT: {incl_vat2}"

        except Exception as e:
            result = f"Error processing Invoice No: {invoice_number}. Error: {str(e)}"
            take_screenshot(page, invoice_number, prefix="error_")

        finally:
            browser.close()
    
    return result

def process_invoices(email, password, invoice_numbers):
    """Process a list of invoice numbers and update results in the GUI."""
    results = []
    for invoice_number in invoice_numbers:
        result = run_playwright(email, password, invoice_number)
        results.append(result)

        # Update the GUI after each invoice is processed
        result_list.delete(0, END)
        for res in results:
            result_list.insert(END, res)
        root.update()  # Refresh the GUI to show updates immediately

def submit_form():
    """Handle the form submission to process invoices."""
    email = email_entry.get()
    password = password_entry.get()
    invoice_numbers = invoice_entry.get("1.0", tk.END).strip().splitlines()

    if not email or not password or not invoice_numbers:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    result_list.delete(0, END)  # Clear previous results
    process_invoices(email, password, invoice_numbers)

# Create the main window
root = tk.Tk()
root.title("Business Central Invoice Search")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Create a frame for input
input_frame = Frame(root, bg="#ffffff", padx=10, pady=10)
input_frame.pack(pady=10, padx=10, fill=tk.X)

# Email input
tk.Label(input_frame, text="Email:", bg="#ffffff").grid(row=0, column=0, sticky='w')
email_entry = tk.Entry(input_frame, width=30)
email_entry.grid(row=0, column=1, pady=5)

# Password input
tk.Label(input_frame, text="Password:", bg="#ffffff").grid(row=1, column=0, sticky='w')
password_entry = tk.Entry(input_frame, show="*", width=30)
password_entry.grid(row=1, column=1, pady=5)

# Invoice numbers input
tk.Label(input_frame, text="Invoice Numbers (one per line):", bg="#ffffff").grid(row=2, column=0, sticky='w')
invoice_entry = scrolledtext.ScrolledText(input_frame, height=8, width=30, wrap=tk.WORD)
invoice_entry.grid(row=2, column=1, pady=5)

# Create a submit button
submit_button = tk.Button(input_frame, text="Submit", command=submit_form, bg="#4CAF50", fg="white")
submit_button.grid(row=3, columnspan=2, pady=10)

# Create a frame for results
result_frame = Frame(root, bg="#ffffff", padx=10, pady=10)
result_frame.pack(pady=10, padx=10, fill=tk.X)

# Create a Listbox to display results
tk.Label(result_frame, text="Results:", bg="#ffffff").pack(anchor='w')
result_list = Listbox(result_frame, width=70, height=10)
result_list.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
