import sqlite3
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Treeview

# Main Window
window = Tk()
window.state('zoomed')
window.title("Shops Management")
window.config()

# Fonts
font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 15, 'bold')

# Title Label
Title_label = Label(
    window,
    text="Shops Management",
    font=('Arial', 30, 'bold'),
    fg="#5D3D21",
)
Title_label.place(relx=0.5, rely=0.03, anchor='center')


def fetch_worker_id():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM Employees")
    worker_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]

    conn.close()
    return worker_list

def add_to_treeview():
    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('SELECT * FROM Shops')
        shops = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
        return
    finally:
        conn.close()


    tree.delete(*tree.get_children())


    for shop in shops:
        tree.insert('', 'end', values=shop)

def generate_shop_id():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('SELECT MAX(shop_id) FROM Shops')
        result = cursor.fetchone()


        new_id = 1 if result[0] is None else int(result[0]) + 1


        if 'shop_id_entry' in globals():
            shop_id_entry.delete(0, END)
            shop_id_entry.insert(0, new_id)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()

def insert():
    name = name_entry.get()
    contact_num = contact_num_entry.get()
    address = address_entry.get()
    worker_id = worker_id_combobox.get()

    if not (name and contact_num and address and worker_id):
        messagebox.showerror('Error', 'Enter all fields.')
        return

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    shop_id = shop_id_entry.get()

    cursor.execute(''' 
        INSERT INTO Shops (shop_id, name, contact_num, address, worker_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (shop_id, name, contact_num, address, worker_id))
    conn.commit()

    messagebox.showinfo('Success', 'Shop has been inserted.')


    add_to_treeview()

def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        shop_id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        contact_num_entry.insert(0, row[2])
        address_entry.insert(0, row[3])
        worker_id_combobox.set(row[4])
    else:
        pass

def clear(*clicked):
    shop_id_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_num_entry.delete(0, END)
    address_entry.delete(0, END)
    worker_id_combobox.set("")

def delete():

    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a shop to delete.')
        return


    values = tree.item(selected_item, 'values')
    shop_id = values[0]

    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('DELETE FROM Shops WHERE shop_id = ?', (shop_id,))
        conn.commit()


        add_to_treeview()
        clear()

        messagebox.showinfo('Success', 'Data has been deleted.')
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()

def new_shop():
    clear()
    generate_shop_id()

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a shop to update.')
        return


    shop_id = shop_id_entry.get()
    name = name_entry.get()
    contact_num = contact_num_entry.get()
    address = address_entry.get()
    worker_id = worker_id_combobox.get()

    if not (shop_id and name and contact_num and address and worker_id):
        messagebox.showerror('Error', 'All fields are required.')
        return

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute(''' 
            UPDATE Shops
            SET name = ?, contact_num = ?, address = ?, worker_id = ?
            WHERE shop_id = ?
        ''', (name, contact_num, address, worker_id, shop_id))
        conn.commit()

        add_to_treeview()
        clear()

        messagebox.showinfo('Success', 'Data has been updated.')
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()

def back():
    print("Returning to welcome page...")
    window.destroy()
    subprocess.run(["python", "admin_panel.py"])

entry_bg_color = "#3E3A39"
entry_fg_color = "white"
label_fg_color = "#5D3D21"

shop_id_label = Label(window, font=font1, text='Shop ID:', fg=label_fg_color)
shop_id_label.place(x=20, y=160)

shop_id_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
shop_id_entry.place(x=270, y=160)

generate_shop_id()

# Name
name_label = Label(window, font=font1, text='Name:', fg=label_fg_color)
name_label.place(x=20, y=220)

name_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
name_entry.place(x=270, y=220)

# Contact Number
contact_num_label = Label(window, font=font1, text='Contact Number:', fg=label_fg_color)
contact_num_label.place(x=20, y=280)

contact_num_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
contact_num_entry.place(x=270, y=280)

# Address
address_label = Label(window, font=font1, text='Address:', fg=label_fg_color)
address_label.place(x=20, y=340)

address_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
address_entry.place(x=270, y=340)

# Worker ID Label
worker_id_label = Label(window, font=font1, text='Worker ID:', fg=label_fg_color)
worker_id_label.place(x=20, y=400)

# Fetch worker IDs
worker_data = fetch_worker_id()
worker_id_combobox = ttk.Combobox(window, values=worker_data, font=font1, state="readonly", width=19)
worker_id_combobox.place(x=270, y=400)
worker_id_combobox.set("Select")

# Button Styles
button_fg_color = "#5D3D21"
button_hover_color = "white"

# Buttons
add_button = Button(
    window,
    command=insert,
    text='Add Shop',
    font=font2,
    fg=button_fg_color,
    activebackground=button_hover_color,
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
add_button.place(x=90, y=600)

clear_button = Button(
    window,
    command=new_shop,
    text='New Shop',
    font=font2,
    fg=button_fg_color,
    activebackground=button_hover_color,
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
clear_button.place(x=300, y=600)

update_button = Button(
    window,
    command=update,
    text='Update Shop',
    font=font2,
    fg=button_fg_color,
    activebackground=button_hover_color,
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
update_button.place(x=90, y=660)

delete_button = Button(
    window,
    command=delete,
    text='Delete Shop',
    font=font2,
    fg=button_fg_color,
    activebackground=button_hover_color,
    cursor='hand2',
    width=15,
    height=1,
    relief="solid"
)
delete_button.place(x=300, y=660)

# Treeview
tree = Treeview(window, height=25)
tree['columns'] = ('Shop_ID', 'Name', 'Contact_Num', 'Address', 'Worker_ID')

tree.column('#0', width=0, stretch=tk.NO)
tree.column('Shop_ID', anchor=tk.CENTER, width=150)
tree.column('Name', anchor=tk.CENTER, width=150)
tree.column('Contact_Num', anchor=tk.CENTER, width=150)
tree.column('Address', anchor=tk.CENTER, width=150)
tree.column('Worker_ID', anchor=tk.CENTER, width=150)

tree.heading('Shop_ID', text='Shop ID')
tree.heading('Name', text='Name')
tree.heading('Contact_Num', text='Contact_Num')
tree.heading('Address', text='Address')
tree.heading('Worker_ID', text='Worker_ID')

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview")
style.map('Treeview',background=[('selected','#000')])
tree.place(x=650, y=160)

tree.bind('<ButtonRelease>', display_data)
add_to_treeview()

back_button = Button(window, text="Back",font=font2, command=back,
                       width=8, height=1, fg="#5D3D21", relief="solid")
back_button.place(x=1350,y=760)

window.mainloop()