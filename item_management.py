import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Treeview
import sqlite3

# Main Window
window = Tk()
window.state('zoomed')
window.title("Bakery Item Management")
window.config()

# Fonts
font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 15, 'bold')

# Title Label
Title_label = Label(
    window,
    text="Bakery Item Management",
    font=('Arial', 30, 'bold'),
    fg="#5D3D21",
)
Title_label.place(relx=0.5, rely=0.03, anchor='center')


def generate_item_id():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('SELECT MAX(item_id) FROM Items')
        result = cursor.fetchone()


        item_id = 1 if result[0] is None else result[0] + 1


        while True:
            cursor.execute('SELECT 1 FROM Items WHERE item_id = ?', (item_id,))
            if cursor.fetchone():
                item_id += 1
            else:
                break


        if 'item_id_entry' in globals():
            item_id_entry.delete(0, END)
            item_id_entry.insert(0, item_id)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def new_item():
    clear()
    generate_item_id()

def insert():
    name = name_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()

    if not (name and price and stock):
        messagebox.showerror('Error', 'Enter all fields.')
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO Items (name, price, stock)
            VALUES (?, ?, ?)
        ''', (name, price, stock))
        conn.commit()

        item_id = cursor.lastrowid
        item_id_entry.delete(0, END)
        item_id_entry.insert(0, str(item_id))

        messagebox.showinfo('Success', f'Item has been inserted with ID {item_id}.')


        add_to_treeview(tree)

    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()

def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        item_id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        price_entry.insert(0, row[2])
        stock_entry.insert(0, row[3])

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())

    item_id_entry.delete(0, END)
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    stock_entry.delete(0, END)

def delete():

    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an item to delete.')
        return


    values = tree.item(selected_item, 'values')
    if not values:
        messagebox.showerror('Error', 'Failed to get item ID.')
        return

    item_id = values[0]

    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Items WHERE item_id = ?', (item_id,))
        conn.commit()


        add_to_treeview(tree)
        clear()

        messagebox.showinfo('Success', 'Data has been deleted.')
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:

        conn.close()

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Please select an item to update.')
        return

    item_id = item_id_entry.get().strip()
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    stock = stock_entry.get().strip()

    # Validate inputs
    if not all([item_id, name, price, stock]):
        messagebox.showerror('Error', 'All fields must be filled.')
        return
    if not price.isdigit() or not stock.isdigit():
        messagebox.showerror('Error', 'Price and Stock must be numeric values.')
        return

    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(''' 
            UPDATE Items
            SET name = ?, price = ?, stock = ?
            WHERE item_id = ?
        ''', (name, price, stock, item_id))
        conn.commit()


        add_to_treeview(tree)
        clear()

        messagebox.showinfo('Success', f"Item with ID {item_id} has been updated successfully.")

    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()

def back():
    print("Returning to welcome page...")
    window.destroy()
    subprocess.run(["python", "admin_panel.py"])

def add_to_treeview(tree):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Items')
        items = cursor.fetchall()

        tree.delete(*tree.get_children())


        for item in items:
            tree.insert('', 'end', values=item)

    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()


# Fields and Labels
entry_bg_color = "#3E3A39"
entry_fg_color = "white"
label_fg_color = "#5D3D21"

# Item ID
item_id_label = Label(window, font=font1, text='Item ID:', fg=label_fg_color )
item_id_label.place(x=20, y=160)
item_id_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
item_id_entry.place(x=270, y=160)
generate_item_id()

# Name
name_label = Label(window, font=font1, text='Name:', fg=label_fg_color)
name_label.place(x=20, y=220)
name_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
name_entry.place(x=270, y=220)

# Price
price_label = Label(window, font=font1, text='Price:', fg=label_fg_color)
price_label.place(x=20, y=280)
price_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
price_entry.place(x=270, y=280)

# Stock
stock_label = Label(window, font=font1, text='Stock:', fg=label_fg_color)
stock_label.place(x=20, y=340)
stock_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
stock_entry.place(x=270, y=340)

# Buttons
button_fg_color = "#5D3D21"
button_hover_color = "white"

add_button = Button(window, command=insert, text='Add Item', font=font2, fg=button_fg_color,
                    activebackground=button_hover_color, cursor='hand2', width=15, height=1, relief="solid")
add_button.place(x=90, y=500)

new_item_button = Button(window, command=new_item, text='New Item', font=font2, fg=button_fg_color,
                          activebackground=button_hover_color, cursor='hand2', width=15, height=1,
                          relief="solid")
new_item_button.place(x=300, y=500)

update_button = Button(window, command=update, text='Update Item', font=font2, fg=button_fg_color,
                       activebackground=button_hover_color, cursor='hand2', width=15, height=1, relief="solid")
update_button.place(x=90, y=560)

delete_button = Button(window, command=delete, text='Delete Item', font=font2, fg=button_fg_color,
                       activebackground=button_hover_color, cursor='hand2', width=15, height=1, relief="solid")
delete_button.place(x=300, y=560)

# Treeview
tree = Treeview(window, height=25)
tree['columns'] = ('Item_ID', 'Name', 'Price', 'Stock')

tree.column('#0', width=0, stretch=tk.NO)
tree.column('Item_ID', anchor=tk.CENTER, width=170)
tree.column('Name', anchor=tk.CENTER, width=170)
tree.column('Price', anchor=tk.CENTER, width=170)
tree.column('Stock', anchor=tk.CENTER, width=170)

tree.heading('Item_ID', text='Item ID')
tree.heading('Name', text='Name')
tree.heading('Price', text='Price')
tree.heading('Stock', text='Stock')

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview")
style.map('Treeview', background=[('selected', '#000')])
tree.place(x=700, y=160)

tree.bind('<ButtonRelease>', display_data)
add_to_treeview(tree)

back_button = Button(window, text="Back", font=font2, command=back,
                     width=10, height=2, fg="#5D3D21", relief="solid")
back_button.place(x=1350, y=760)


window.mainloop()
