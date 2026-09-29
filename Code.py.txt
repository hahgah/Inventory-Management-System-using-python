import json
import tkinter as tk
from tkinter import messagebox

# -------- FILE HANDLING --------
def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            return json.load(file)
    except:
        return {}

def save_inventory():
    with open("inventory.txt", "w") as file:
        json.dump(inventory, file)

inventory = load_inventory()

# -------- LOGIN --------
def check_login():
    if username_entry.get() == "admin" and password_entry.get() == "1234":
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Invalid credentials")

# -------- MAIN WINDOW --------
def open_main_window():
    global root
    root = tk.Tk()
    root.title("Inventory Management System - Hasnain")
    root.geometry("500x500")

    # Labels & Entries
    tk.Label(root, text="Item Name").pack()
    global name_entry
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Quantity").pack()
    global quantity_entry
    quantity_entry = tk.Entry(root)
    quantity_entry.pack()

    tk.Label(root, text="Price").pack()
    global price_entry
    price_entry = tk.Entry(root)
    price_entry.pack()

    # Buttons
    tk.Button(root, text="Add Item", command=add_item).pack(pady=5)
    tk.Button(root, text="Update Item", command=update_item).pack(pady=5)
    tk.Button(root, text="Delete Item", command=delete_item).pack(pady=5)
    tk.Button(root, text="Search Item", command=search_item).pack(pady=5)
    tk.Button(root, text="Show Inventory", command=show_items).pack(pady=5)
    tk.Button(root, text="Save & Exit", command=exit_app).pack(pady=5)

    # Display box
    global display
    display = tk.Text(root, height=10, width=50)
    display.pack()

    root.mainloop()

# -------- FUNCTIONS --------
def add_item():
    name = name_entry.get().lower()
    try:
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
    except:
        messagebox.showerror("Error", "Invalid input")
        return

    inventory[name] = {"quantity": quantity, "price": price}
    messagebox.showinfo("Success", "Item added")

def update_item():
    name = name_entry.get().lower()
    if name in inventory:
        try:
            inventory[name]["quantity"] = int(quantity_entry.get())
            inventory[name]["price"] = float(price_entry.get())
            messagebox.showinfo("Success", "Item updated")
        except:
            messagebox.showerror("Error", "Invalid input")
    else:
        messagebox.showerror("Error", "Item not found")

def delete_item():
    name = name_entry.get().lower()
    if name in inventory:
        del inventory[name]
        messagebox.showinfo("Success", "Item deleted")
    else:
        messagebox.showerror("Error", "Item not found")

def search_item():
    name = name_entry.get().lower()
    display.delete(1.0, tk.END)

    if name in inventory:
        item = inventory[name]
        display.insert(tk.END, f"{name} | Qty: {item['quantity']} | Price: {item['price']}\n")
    else:
        display.insert(tk.END, "Item not found\n")

def show_items():
    display.delete(1.0, tk.END)

    for name, details in inventory.items():
        line = f"{name} | Qty: {details['quantity']} | Price: {details['price']}"
        
        # LOW STOCK WARNING
        if details['quantity'] < 5:
            line += " ⚠ Low Stock"
        
        display.insert(tk.END, line + "\n")

def exit_app():
    save_inventory()
    root.destroy()

# -------- LOGIN WINDOW --------
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

login_window.mainloop()