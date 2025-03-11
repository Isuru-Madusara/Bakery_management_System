import sqlite3
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# Global variabl
order_items = []
order_id = None

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

def generate_order_id():
    global order_id
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('SELECT MAX(order_id) FROM orders')
        result = cursor.fetchone()


        order_id = 1 if result[0] is None else result[0] + 1


        while True:
            cursor.execute('SELECT 1 FROM orders WHERE order_id = ?', (order_id,))
            if cursor.fetchone():
                order_id += 1
            else:
                break

        conn.close()
        order_id_entry.delete(0, END)
        order_id_entry.insert(0, order_id)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def search_items():
    search_term = search_item_entry.get().strip()
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter a search term!")
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT item_id, name, price, stock FROM Items WHERE name LIKE ?"
        cursor.execute(query, ('%' + search_term + '%',))
        results = cursor.fetchall()
        conn.close()

        for row in results_tree.get_children():
            results_tree.delete(row)

        for row in results:
            results_tree.insert('', 'end', values=row)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def clear():
    global order_id
    order_id = None
    order_id_entry.delete(0, END)
    search_item_entry.delete(0, END)
    quantity_entry.delete(0, END)
    results_tree.delete(*results_tree.get_children())
    order_items.clear()
    update_order_treeview()

def make_order():
    global order_id

    shop_name = shop_name_combobox.get()

    if not shop_name or shop_name == "Select Name":
        messagebox.showwarning("Input Error", "Please select a shop.")
        return

    selected_items = order_tree.get_children()

    if not selected_items:
        messagebox.showwarning("Selection Error", "Please add items to the order.")
        return

    order_details = []
    net_total = 0

    order_date = datetime.now().strftime('%Y-%m-%d')

    for item in selected_items:
        item_data = order_tree.item(item)['values']
        item_id, item_name, quantity, total_price = item_data
        order_details.append({
            'item_id': item_id,
            'item_name': item_name,
            'quantity': quantity,
            'total_price': total_price
        })
        net_total += total_price

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        for item in order_details:
            cursor.execute(''' 
                SELECT stock FROM Items WHERE item_id = ?
            ''', (item['item_id'],))
            remaining_stock = cursor.fetchone()
            if remaining_stock is None or remaining_stock[0] < item['quantity']:
                messagebox.showerror("Stock Error", f"Insufficient stock for item ID {item['item_id']}.")
                conn.close()
                return


        for item in order_details:
            cursor.execute(''' 
                INSERT INTO Orders (order_id, shop_name, order_date, item_id, item_name, quantity, total_price, net_total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (order_id, shop_name, order_date, item['item_id'], item['item_name'], item['quantity'],
                  item['total_price'], net_total))

            # Update stock
            cursor.execute(''' 
                UPDATE Items 
                SET stock = stock - ? 
                WHERE item_id = ?
            ''', (item['quantity'], item['item_id']))

        conn.commit()
        conn.close()


        messagebox.showinfo("Success", "Order successfully created.")
        clear()
        generate_order_id()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def add_item_to_tree_view():
    if order_id is None:
        messagebox.showwarning("Order Error", "Please create an order first.")
        return

    selected_item = results_tree.focus()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to add.")
        return

    item_data = results_tree.item(selected_item)['values']


    item_id, item_name, item_price, stock = item_data

    quantity = quantity_entry.get().strip()


    if not quantity.isdigit() or int(quantity) <= 0:
        messagebox.showerror("Input Error", "Quantity must be a positive integer.")
        return

    quantity = int(quantity)
    total_price = item_price * quantity

    if quantity > stock:
        messagebox.showerror("Stock Error", "Insufficient stock available.")
        return


    order_items.append((item_id, item_name, quantity, total_price))


    update_order_treeview()


    quantity_entry.delete(0, END)

def update_order_treeview():
    for row in order_tree.get_children():
        order_tree.delete(row)

    for item in order_items:
        order_tree.insert('', 'end', values=item)

def new_order():
    clear()
    generate_order_id()

def back():
    print("Returning to welcome page...")
    window.destroy()
    subprocess.run(["python", "orders_main.py"])

def delete_order():
    selected_order = order_tree.focus()
    if not selected_order:
        messagebox.showwarning("Selection Error", "Please select an order to delete.")
        return

    item_data = order_tree.item(selected_order)['values']
    item_id, item_name, quantity, total_price = item_data

    order_id_to_delete = order_id

    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the order for {item_name}?")
    if not confirm:
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Orders WHERE order_id = ? AND item_id = ?', (order_id_to_delete, item_id))

        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Delete Error", "The order could not be deleted. It may have already been removed.")
        else:
            order_tree.delete(selected_order)
            messagebox.showinfo("Success", "Order successfully deleted.")

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Main Window
window = Tk()
window.state('zoomed')
window.title("Make Order")

# Fonts
font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 15, 'bold')

# Title Label
Title_label = Label(
    window,
    text="Make Order to Shop",
    font=('Arial', 30, 'bold'),
    fg="#5D3D21",
)
Title_label.place(relx=0.5, rely=0.03, anchor='center')

# Colors
entry_bg_color = "#3E3A39"
entry_fg_color = "white"
label_fg_color = "#5D3D21"

# Order ID Label and Entry
order_id_label = Label(window, font=font1, text='Order ID:', fg=label_fg_color)
order_id_label.place(x=20, y=150)

order_id_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=21, borderwidth=2)
order_id_entry.place(x=270, y=150)

generate_order_id()

# Shop Name Combobox
shop_name_label = Label(window, font=font1, text='Shop Name:', fg=label_fg_color)
shop_name_label.place(x=20, y=210)

shop_names = fetch_shop_name()
shop_name_combobox = ttk.Combobox(window, values=shop_names, font=font1, state="readonly")
shop_name_combobox.place(x=270, y=210)
shop_name_combobox.set("Select Name")

# Search Item Entry
search_item_entry = Entry(window, font=font1, bg="#FFFFFF", fg="#000000", width=21, borderwidth=2)
search_item_entry.place(x=270, y=270)

search_item_label = Label(window, font=font1, text='Item:', fg=label_fg_color)
search_item_label.place(x=20, y=270)

search_item_button = Button(window, text="Search Item", font=font2, bg="#5D3D21", fg="#FFFFFF", command=search_items)
search_item_button.place(x=610, y=270)

# Results Section
results_frame = Frame(window, bg="#3E3A39")
results_frame.place(x=270, y=330, width=468, height=100)

# Treeview for displaying results
columns = ('item_id', 'name', 'price', 'stock')
results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=5)

# Define headings
results_tree.heading('item_id', text='Item ID')
results_tree.heading('name', text='Item Name')
results_tree.heading('price', text='Price')
results_tree.heading('stock', text='Stock')

# Define column widths
results_tree.column('item_id', width=100, anchor='center')
results_tree.column('name', width=150, anchor='w')
results_tree.column('price', width=100, anchor='center')
results_tree.column('stock', width=100, anchor='center')

# Add the Treeview to the window
results_tree.pack(fill='both', expand=True)

# Quantity Entry
quantity_label = Label(window, font=font1, text='Quantity:', fg=label_fg_color)
quantity_label.place(x=20, y=440)

quantity_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
quantity_entry.place(x=270, y=440)

# Order Date Label and Entry
order_date_label = Label(window, font=font1, text='Order Date:', fg=label_fg_color)
order_date_label.place(x=20, y=500)

# Order Date Entry
order_date_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=21, borderwidth=2, state='normal')
order_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
order_date_entry.place(x=270, y=500)

# Buttons
add_button = Button(
    window,
    command=add_item_to_tree_view,
    text='Add Order',
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
add_button.place(x=90, y=550)

make_order_button = Button(
    window,
    command=make_order,
    text='Make Order',
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
make_order_button.place(x=90, y=600)

new_order_button = Button(
    window,
    command=new_order,
    text='New Order',
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
new_order_button.place(x=300, y=600)

delete_order_button = Button(
    window,
    command=delete_order,
    text='Delete Order',
    font=font2,
    fg="#5D3D21",
    activebackground="white",
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
delete_order_button.place(x=300, y=550)

order_frame = Frame(window, bg="#3E3A39")
order_frame.place(x=780, y=140, width=650, height=400)

order_columns = ('item_id', 'name', 'quantity', 'total_price')
order_tree = ttk.Treeview(order_frame, columns=order_columns, show='headings', height=15)

order_tree.heading('item_id', text='Item ID')
order_tree.heading('name', text='Item Name')
order_tree.heading('quantity', text='Quantity')
order_tree.heading('total_price', text='Total Price')

order_tree.column('item_id', width=100, anchor='center')
order_tree.column('name', width=150, anchor='w')
order_tree.column('quantity', width=100, anchor='center')
order_tree.column('total_price', width=100, anchor='center')

order_tree.pack(fill='both', expand=True)

back_button = Button(window, text="Back", font=font2, command=back,
                     width=8, height=1, fg="#5D3D21", relief="solid")
back_button.place(x=1350, y=760)


window.mainloop()