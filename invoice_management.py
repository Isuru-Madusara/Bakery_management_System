import sqlite3
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

# Main Window
window = Tk()
window.state('zoomed')
window.title("Invoice Management")

# Fonts
font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 15, 'bold')

# Title Label
Title_label = Label(
    window,
    text="Invoice Management",
    font=('Arial', 30, 'bold'),
    fg="#5D3D21",
)
Title_label.place(relx=0.5, rely=0.03, anchor='center')

def populate_treeview():

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT DISTINCT bill_id, bill_date, bill_time, shop_name FROM Bills')
        bill_items = cursor.fetchall()

        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
        return

    tree.delete(*tree.get_children())  # Clear previous entries

    for bill_id, bill_date, bill_time, shop_name in bill_items:
        tree.insert('', 'end', values=(bill_id, bill_date, bill_time, shop_name))

def show_order_details(event):

    selected_item = tree.focus()
    if not selected_item:
        return

    values = tree.item(selected_item, 'values')
    if len(values) < 4:
        return

    bill_id, bill_date, bill_time, shop_name = values

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT bill_id, item_name, quantity, total_price, net_total
            FROM Bills
            WHERE bill_id = ?
        ''', (bill_id,))
        order_items = cursor.fetchall()

        net_total = order_items[0][4] if order_items else 0

        conn.close()

        generate_bill(bill_id, shop_name, bill_date, bill_time, net_total, order_items)
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")

def generate_bill(bill_id, shop_name, bill_date, bill_time, net_total, order_items):

    bill_text.delete(1.0, END)

    bill = f"Shop Name: {shop_name}\n"
    bill += f"Bill ID : {bill_id}\n"
    bill += f"Date     : {bill_date}   Time : {bill_time}\n"
    bill += "\nItems:\n"
    bill += "-----------------------------------------\n"
    bill += f"{'Item Name':<15}{'Quantity':<15}{'Price':<10}\n"

    for item in order_items:
        _, item_name, quantity, total_price, _ = item
        bill += f"{item_name:<17}{quantity:<16}{total_price:<10.2f}\n"

    bill += "-----------------------------------------\n"
    bill += f"{'Total Amount:':<33}{net_total:<10.2f}\n"
    bill += "-----------------------------------------\n"

    bill_text.insert(END, bill)

def delete_bill():

    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a bill to delete!")
        return

    values = tree.item(selected_item, 'values')
    if len(values) < 1:
        return

    bill_id = values[0]

    confirmation = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete Bill ID {bill_id}?")
    if not confirmation:
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute("DELETE FROM Bills WHERE bill_id = ?", (bill_id,))
        conn.commit()
        conn.close()


        tree.delete(selected_item)
        bill_text.delete(1.0, END)

        messagebox.showinfo("Success", "Bill deleted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def back():

    print("Returning to welcome page...")
    window.destroy()
    subprocess.run(["python", "admin_panel.py"])

tree = ttk.Treeview(window, height=25)
tree['columns'] = ('bill_id', 'bill_date', 'bill_time', 'shop_name')

tree.column('#0', width=0, stretch=tk.NO)
tree.column('bill_id', anchor=tk.CENTER, width=150)
tree.column('bill_date', anchor=tk.CENTER, width=150)
tree.column('bill_time', anchor=tk.CENTER, width=150)
tree.column('shop_name', anchor=tk.CENTER, width=250)

tree.heading('#0', text='', anchor=tk.W)
tree.heading('bill_id', text='Bill ID', anchor=tk.CENTER)
tree.heading('bill_date', text='Order Date', anchor=tk.CENTER)
tree.heading('bill_time', text='Order Time', anchor=tk.CENTER)
tree.heading('shop_name', text='Shop Name', anchor=tk.CENTER)

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="#F8F8F8", foreground="#000", fieldbackground="#F8F8F8")
style.map("Treeview", background=[('selected', '#D3D3D3')])

tree.place(x=50, y=100, width=750, height=600)

bill_text = Text(window, wrap=WORD, font=('Courier', 12), bg="#F8F8F8", fg="#000")
bill_text.place(x=950, y=100, width=420, height=400)

tree.bind('<Double-1>', show_order_details)

populate_treeview()

refresh_button = Button(
    window,
    text="Refresh Data",
    font=font2,
    command=populate_treeview,
    width=15,
    height=1,
    fg="#5D3D21",
    relief="solid"
)
refresh_button.place(x=450, y=750)

# Delete Button
delete_button = Button(
    window,
    text="Delete Bill",
    font=font2,
    command=delete_bill,
    width=15,
    height=1,
    fg="red",
    relief="solid"
)
delete_button.place(x=650, y=750)

back_button = Button(window, text="Back", font=font2, command=back,
                     width=8, height=1, fg="#5D3D21", relief="solid")
back_button.place(x=1350, y=760)

window.mainloop()