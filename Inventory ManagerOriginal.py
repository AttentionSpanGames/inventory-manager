import tkinter as tk
from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔐 Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "plenary-edition-473122-u8-c99ae9b3cf97.json"  # Replace with your actual credentials file

def connect_to_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key("1DnDb6m1vZ5gTQvL4mEJ57hXA19F9OHA1bnDHzetMWng")
    return spreadsheet.worksheet("Inventory_Manager")


sheet = connect_to_sheet()

# 🧠 Core logic
def submit_data():
    location = location_entry.get().strip()
    barcode = barcode_entry.get().strip()
    try:
        quantity_adjustment = int(quantity_entry.get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Quantity must be an integer.")
        return

    if not barcode:
        messagebox.showerror("Missing Fields", "Barcode and Quantity must be filled.")
        return

    cell = sheet.find(barcode)
    if cell:
        row = cell.row
        current_location = sheet.cell(row, 2).value
        current_quantity = sheet.cell(row, 3).value

        # Only update location if a new one is provided
        if location and current_location != location:
            sheet.update_cell(row, 2, location)

        current_quantity = int(current_quantity) if current_quantity else 0
        new_quantity = current_quantity + quantity_adjustment
        sheet.update_cell(row, 3, str(new_quantity))
    else:
        # If location is blank, insert empty string
        sheet.append_row([barcode, location, str(quantity_adjustment)])

    barcode_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Data submitted successfully!")
    
# 🖼 GUI setup
root = tk.Tk()
root.title("Inventory Tracker")

tk.Label(root, text="Location").grid(row=0, column=0, padx=10, pady=5)
location_entry = tk.Entry(root, width=30)
location_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Barcode").grid(row=1, column=0, padx=10, pady=5)
barcode_entry = tk.Entry(root, width=30)
barcode_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Quantity Adjustment").grid(row=2, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(root, width=30)
quantity_entry.grid(row=2, column=1, padx=10, pady=5)

def validate_fields(*args):
    if barcode_entry.get().strip() and quantity_entry.get().strip():
        submit_btn.config(state=tk.NORMAL)
    else:
        submit_btn.config(state=tk.DISABLED)

location_entry.bind("<KeyRelease>", validate_fields)
barcode_entry.bind("<KeyRelease>", validate_fields)
quantity_entry.bind("<KeyRelease>", validate_fields)

submit_btn = tk.Button(root, text="Submit", command=submit_data, state=tk.DISABLED)
submit_btn.grid(row=3, column=0, columnspan=2, pady=10)
root.mainloop()

