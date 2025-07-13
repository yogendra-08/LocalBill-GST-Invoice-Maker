import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

# Global list to store invoice data
invoice_items = []

# GST % options
gst_options = [5, 12, 18, 28]

def add_item():
    item = item_entry.get()
    try:
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        gst = int(gst_var.get())
    except ValueError:
        messagebox.showerror("Input Error", "Enter valid numeric values.")
        return

    gst_amount = (price * gst / 100)
    total_price = (price + gst_amount) * quantity

    invoice_items.append([item, price, quantity, gst, round(total_price, 2)])

    update_table()
    clear_fields()

def update_table():
    for row in bill_table.get_children():
        bill_table.delete(row)
    total_amt = 0
    for idx, row in enumerate(invoice_items):
        bill_table.insert("", "end", values=row)
        total_amt += row[4]
    total_var.set(f"₹ {round(total_amt, 2)}")

def clear_fields():
    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    gst_var.set(gst_options[0])

def generate_invoice():
    if not invoice_items:
        messagebox.showwarning("Empty Bill", "Add at least one item.")
        return
    filename = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(f"data/{filename}", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Price", "Quantity", "GST%", "Total"])
        for row in invoice_items:
            writer.writerow(row)
        writer.writerow(["", "", "", "Total", total_var.get()])
    messagebox.showinfo("Success", f"Invoice saved as {filename}")
    invoice_items.clear()
    update_table()

# ===================== GUI SETUP ============================
root = tk.Tk()
root.title("LocalBill – GST Invoice Maker")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

title = tk.Label(root, text="🧾 LocalBill – GST Invoice Maker", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
title.pack(pady=10)

frame = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
frame.pack(padx=10, pady=5, fill="x")

# Customer Details (optional)
cust_frame = tk.Frame(frame, bg="#ffffff")
cust_frame.pack(fill="x")

tk.Label(cust_frame, text="Customer Name:", bg="#ffffff").grid(row=0, column=0, padx=5, pady=2)
cust_name = tk.Entry(cust_frame)
cust_name.grid(row=0, column=1, padx=5)

tk.Label(cust_frame, text="Contact No.:", bg="#ffffff").grid(row=0, column=2, padx=5)
cust_contact = tk.Entry(cust_frame)
cust_contact.grid(row=0, column=3, padx=5)

# Item Entry
item_frame = tk.Frame(frame, bg="#ffffff")
item_frame.pack(fill="x", pady=5)

tk.Label(item_frame, text="Item:", bg="#ffffff").grid(row=0, column=0, padx=5)
item_entry = tk.Entry(item_frame)
item_entry.grid(row=0, column=1, padx=5)

tk.Label(item_frame, text="Price:", bg="#ffffff").grid(row=0, column=2)
price_entry = tk.Entry(item_frame)
price_entry.grid(row=0, column=3, padx=5)

tk.Label(item_frame, text="Qty:", bg="#ffffff").grid(row=0, column=4)
quantity_entry = tk.Entry(item_frame, width=5)
quantity_entry.grid(row=0, column=5, padx=5)

tk.Label(item_frame, text="GST%:", bg="#ffffff").grid(row=0, column=6)
gst_var = tk.StringVar(value=gst_options[0])
gst_menu = ttk.Combobox(item_frame, textvariable=gst_var, values=gst_options, width=5, state="readonly")
gst_menu.grid(row=0, column=7, padx=5)

tk.Button(item_frame, text="Add Item", command=add_item, bg="#007bff", fg="white").grid(row=0, column=8, padx=10)

# Invoice Table
table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=10, fill="both", expand=True)

cols = ("Item", "Price", "Quantity", "GST%", "Total")
bill_table = ttk.Treeview(table_frame, columns=cols, show="headings")
for col in cols:
    bill_table.heading(col, text=col)
    bill_table.column(col, anchor=tk.CENTER)
bill_table.pack(fill="both", expand=True)

# Total + Button
bottom_frame = tk.Frame(root, bg="#f0f0f0")
bottom_frame.pack(fill="x", padx=10, pady=10)

total_var = tk.StringVar(value="₹ 0.00")
tk.Label(bottom_frame, text="Total:", font=("Helvetica", 12), bg="#f0f0f0").pack(side="left")
tk.Label(bottom_frame, textvariable=total_var, font=("Helvetica", 12, "bold"), bg="#f0f0f0").pack(side="left", padx=10)

tk.Button(bottom_frame, text="Generate Invoice", bg="#28a745", fg="white", command=generate_invoice).pack(side="right", padx=10)

root.mainloop()
