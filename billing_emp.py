import os
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter import Text, WORD

window = Tk()
window.state('zoomed')
window.title("Make Bill")

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 15, 'bold')

# Title Label
Title_label = Label(
    window,
    text="Billing Area",
    font=('Arial', 30, 'bold'),
    fg="#5D3D21",
)
Title_label.place(relx=0.5, rely=0.03, anchor='center')

# Global Variable
bill_id = None
order_items = []

def fetch_shop_name():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Shops")
        shop_names = [row[0] for row in cursor.fetchall()]
        conn.close()
        return shop_names
    except sqlite3.Error as e:
        print(f"Error fetching shop names: {e}")
        return []

def search_items():
    search_term = search_item_entry.get().strip()
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter a search term!")
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT item_id, name, price FROM Items WHERE name LIKE ?"
        cursor.execute(query, ('%' + search_term + '%',))
        results = cursor.fetchall()
        conn.close()


        for row in results_tree.get_children():
            results_tree.delete(row)


        for row in results:
            results_tree.insert('', 'end', values=row)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def generate_bill_id():
    global bill_id
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('SELECT MAX(bill_id) FROM Bills')
        result = cursor.fetchone()


        bill_id = 1 if result[0] is None else result[0] + 1

        while True:
            cursor.execute('SELECT 1 FROM Bills WHERE bill_id = ?', (bill_id,))
            if cursor.fetchone():
                bill_id += 1
            else:
                break
        conn.close()

        bill_id_entry.delete(0, END)
        bill_id_entry.insert(0, bill_id)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def add_item_to_tree_view():
    if bill_id is None:
        messagebox.showwarning("Order Error", "Please create an order first.")
        return

    selected_item = results_tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to add.")
        return

    item_data = results_tree.item(selected_item)['values']

    item_id, item_name, item_price = item_data

    quantity = quantity_entry.get().strip()


    if not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showerror("Input Error", "Quantity must be a positive integer.")
        return

    quantity = int(quantity)
    total_price = item_price * quantity


    order_items.append((item_id, item_name, quantity, total_price))


    update_order_treeview()


    quantity_entry.delete(0, END)

def update_order_treeview():

    for row in add_to_bill_tree.get_children():
        add_to_bill_tree.delete(row)


    for item in order_items:
        add_to_bill_tree.insert('', 'end', values=item)

def clear():
    global bill_id
    bill_id = None  # Reset bill_id
    bill_id_entry.delete(0, END)
    customer_name_entry.delete(0, END)
    customer_mobile_entry.delete(0, END)
    search_item_entry.delete(0, END)
    quantity_entry.delete(0, END)
    results_tree.delete(*results_tree.get_children())
    order_items.clear()
    update_order_treeview()

def new_bill():
    clear()
    generate_bill_id()
    generate_bill_format()

def generate_bill():
    global bill_id


    billed_employee_name = billed_by_entry.get().strip()  # Employee Name
    shop_name = shop_name_combobox.get().strip()  # Shop Name
    customer_name = customer_name_entry.get().strip()  # Customer Name
    customer_mobile_number = customer_mobile_entry.get().strip()  # Customer Mobile Number


    if not billed_employee_name or not shop_name or not customer_name or not customer_mobile_number:
        messagebox.showwarning("Warning", "Please fill in all required fields.")
        return

    if not order_items:
        messagebox.showwarning("Warning", "No items selected for billing.")
        return

    order_details = []
    net_total = 0.0
    order_date = datetime.now().strftime('%Y-%m-%d')  # Get current date
    order_time = datetime.now().strftime('%H:%M')  # Get current time

    # Collect order details from order_items
    for item in order_items:
        item_id, item_name, quantity, total_price = item

        order_details.append({
            'item_id': item_id,
            'item_name': item_name,
            'item_price': total_price / quantity,  # Calculate item price
            'quantity': quantity,
            'total_price': total_price
        })
        net_total += total_price

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        for item in order_details:
            cursor.execute('''INSERT INTO Bills 
                              (bill_id, shop_name, customer_name, customer_mobile_number, bill_date, bill_time, 
                              billing_emp_name, item_id, item_name, item_price, quantity, total_price, net_total)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (bill_id, shop_name, customer_name, customer_mobile_number, order_date, order_time,
                            billed_employee_name, item['item_id'], item['item_name'], item['item_price'],
                            item['quantity'], item['total_price'], net_total))

        conn.commit()
        messagebox.showinfo("Success", "Order successfully created.")

        generate_bill_format()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        conn.close()

def delete_order_item():
    selected_item = add_to_bill_tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to delete.")
        return


    order_items.pop(add_to_bill_tree.index(selected_item))
    update_order_treeview()

def back():
    print("Returning to welcome page...")
    window.destroy()
    os.system("python employee_panel.py")

def generate_bill_format():
    if bill_id is None:
        messagebox.showwarning("Order Error", "Please create an order first.")
        return

    shop_name = shop_name_combobox.get()  # Get selected shop name
    customer_name = customer_name_entry.get()  # Get customer name
    billed_time = datetime.now().strftime('%H:%M')  # Get the billed time
    order_id = bill_id
    date = datetime.now().strftime('%Y-%m-%d')

    # Calculate total amount
    total_amount = sum(item[3] for item in order_items)

    # bill content
    bill = f"Shop Name        : {shop_name}\n"
    bill += f"Order ID               : {order_id}\n"
    bill += f"Date                     : {date}\n"
    bill += f"Customer Name :  {customer_name}\n"
    bill += f"Billed Time          : {billed_time}\n"
    bill += "\nItems:\n"
    bill += "---------------------------------------------\n"
    bill += f"{'Item Name':<15}{'Quantity':<15}{'Price':<10}\n"


    for item in order_items:
        item_name, quantity, total_price = item[1], item[2], item[3]
        bill += f"{item_name:<17}{quantity:<16}{total_price:<10.2f}\n"

    bill += "---------------------------------------------\n"
    bill += f"{'Total Amount:':<33}{total_amount:<10.2f}\n"
    bill += "---------------------------------------------\n"


    bill_text.delete(1.0, END)
    bill_text.insert(END, bill)

# Colors
entry_bg_color = "#3E3A39"
entry_fg_color = "white"
label_fg_color = "#5D3D21"

# Bill ID
bill_id_label = Label(window, font=font1, text='Bill ID:', fg=label_fg_color)
bill_id_label.place(x=20, y=70)

bill_id_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
bill_id_entry.place(x=270, y=70)

# Customer Name
customer_name_label = Label(window, font=font1, text='Customer Name:', fg=label_fg_color)
customer_name_label.place(x=20, y=120)

customer_name_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
customer_name_entry.place(x=270, y=120)

# Customer Mobile
customer_mobile_label = Label(window, font=font1, text='Customer Mobile:', fg=label_fg_color)
customer_mobile_label.place(x=20, y=170)

customer_mobile_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
customer_mobile_entry.place(x=270, y=170)

# Shop Name
shop_name_label = Label(window, font=font1, text='Shop Name:', fg=label_fg_color)
shop_name_label.place(x=20, y=220)
shop_names = fetch_shop_name()
shop_name_combobox = ttk.Combobox(window, values=shop_names, font=font1, state="readonly", width=19)
shop_name_combobox.place(x=270, y=220)
shop_name_combobox.set("Select Name")

# Employee Name
billed_by_label = Label(window, font=font1, text='E.M.P Name:', fg=label_fg_color)
billed_by_label.place(x=20, y=270)

billed_by_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
billed_by_entry.place(x=270, y=270)

# Search Item
search_item_label = Label(window, font=font1, text='Search Item:', fg=label_fg_color)
search_item_label.place(x=20, y=320)

search_item_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
search_item_entry.place(x=270, y=320)

search_item_button = Button(window, text="Search Item", font=font2, bg="#5D3D21", fg="white", command=search_items)
search_item_button.place(x=590, y=320)

# Results Section
results_frame = Frame(window, bg="#3E3A39")
results_frame.place(x=270, y=370, width=450, height=100)

# Treeview for displaying results
columns = ('item_id', 'item_name', 'price')
results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=5)

# Define headings
results_tree.heading('item_id', text='Item ID')
results_tree.heading('item_name', text='Item Name')
results_tree.heading('price', text='Item Price')

# Define column widths
results_tree.column('item_id', width=100, anchor='center')
results_tree.column('item_name', width=150, anchor='w')
results_tree.column('price', width=100, anchor='center')

results_tree.pack(fill='both', expand=True)

# Quantity
quantity_label = Label(window, font=font1, text='Quantity:', fg=label_fg_color)
quantity_label.place(x=20, y=490)

quantity_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
quantity_entry.place(x=270, y=490)

# Buttons
add_button = Button(
    window,
    text='Add TO Cart',
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid",
    command=add_item_to_tree_view
)
add_button.place(x=130, y=560)

delete_order_button = Button(
    window,
    text='Delete From Cart',
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid",
    command=delete_order_item
)
delete_order_button.place(x=330, y=560)

new_order_button = Button(
    window,
    text='New Bill',
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid",
    command=new_bill
)
new_order_button.place(x=230, y=620)


add_to_bill_frame = Frame(window, bg="#3E3A39")
add_to_bill_frame.place(x=800, y=70, width=650, height=240)

add_to_bill_columns = ('item_id', 'item_name', 'quantity', 'total_price')
add_to_bill_tree = ttk.Treeview(add_to_bill_frame, columns=add_to_bill_columns, show='headings', height=15)

add_to_bill_tree.heading('item_id', text='Item ID')
add_to_bill_tree.heading('item_name', text='Item Name')
add_to_bill_tree.heading('quantity', text='Quantity')
add_to_bill_tree.heading('total_price', text='Total Price')

add_to_bill_tree.column('item_id', width=150, anchor='w')
add_to_bill_tree.column('item_name', width=150, anchor='w')
add_to_bill_tree.column('quantity', width=100, anchor='center')
add_to_bill_tree.column('total_price', width=100, anchor='center')

add_to_bill_tree.pack(fill='both', expand=True)

back_button = Button(window, text="Back", font=font2,
                     width=8, height=1, fg="#5D3D21", relief="solid", command=back)
back_button.place(x=1350, y=760)

bill_text = Text(window, font=('Arial', 12), bg="#f4f4f4", fg="#000000", wrap=WORD, height=15, width=30)
bill_text.place(x=800, y=320)

generate_bill_button = Button(
    window,
    text="Make Bill",
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid",
    command=generate_bill
)
generate_bill_button.place(x=840, y=600)

print_bill_button = Button(
    window,
    text="Print Bill",
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid",
)
print_bill_button.place(x=840, y=650)

window.mainloop()