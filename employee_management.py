import sqlite3
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Treeview

def generate_employee_id():
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()


            cursor.execute('SELECT COALESCE(MAX(id), 0) + 1 FROM Employees')
            id = cursor.fetchone()[0]


        if 'id_entry' in globals():
            id_entry.delete(0, "end")
            id_entry.insert(0, id)

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def insert():
    name = name_entry.get()
    contact_no = contact_no_entry.get()
    nic = nic_entry.get()
    role = role_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Check
    if not (name and contact_no and nic and role and username and password):
        messagebox.showerror('Error', 'Enter all fields.')
        return

    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute(''' 
            INSERT INTO Employees (id, name, contact_no, nic, role, user_name, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id_entry.get(), name, contact_no, nic, role, username, password))
        conn.commit()

        messagebox.showinfo('Success', 'Employee has been inserted.')


        add_to_treeview()

    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()

def add_to_treeview():
    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('SELECT * FROM Employees')
        employees = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
        return
    finally:

        conn.close()


    tree.delete(*tree.get_children())

    for employee in employees:
        tree.insert('', 'end', values=employee)

def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())

    id_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_no_entry.delete(0, END)
    nic_entry.delete(0, END)
    role_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)

def delete():

    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an employee to delete.')
        return


    values = tree.item(selected_item, 'values')
    if not values:  # Ensure the item has values
        messagebox.showerror('Error', 'Failed to get employee ID.')
        return

    employee_id = values[0]

    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('DELETE FROM Employees WHERE id = ?', (employee_id,))
        conn.commit()


        add_to_treeview()
        clear()

        messagebox.showinfo('Success', 'Data has been deleted.')
    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()

def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an employee to update.')
        return


    employee_id = id_entry.get()
    name = name_entry.get()
    contact_no = contact_no_entry.get()
    nic = nic_entry.get()
    role = role_entry.get()
    username = username_entry.get()
    password = password_entry.get()


    if not all([employee_id, name, contact_no, nic, role, username, password]):
        messagebox.showerror('Error', 'All fields must be filled.')
        return

    try:

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()


        cursor.execute('SELECT COUNT(1) FROM Employees WHERE id = ?', (employee_id,))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Error", "Employee with this ID doesn't exist.")
            return


        cursor.execute('''
            UPDATE Employees
            SET name = ?, contact_no = ?, nic = ?, role = ?, user_name = ?, password = ?
            WHERE id = ?
        ''', (name, contact_no, nic, role, username, password, employee_id))
        conn.commit()


        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Data has been updated.')

    except sqlite3.Error as e:
        messagebox.showerror('Database Error', f"An error occurred: {e}")
    finally:
        conn.close()

def new_employee():
    clear()
    generate_employee_id()

def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        contact_no_entry.insert(0, row[2])
        nic_entry.insert(0, row[3])
        role_entry.insert(0, row[4])
        username_entry.insert(0, row[5])
        password_entry.insert(0, row[6])

def back():
    print("Returning to welcome page...")
    window.destroy()
    subprocess.run(["python", "admin_panel.py"])


# Main Window
window = Tk()
window.state('zoomed')
window.title("Bakery Employee Management")
window.config()

# Fonts
font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 15, 'bold')

# Title Label
Title_label = Label(
    window,
    text="Bakery Employee Management",
    font=('Arial', 30, 'bold'),
    fg="#5D3D21",
)
Title_label.place(relx=0.5, rely=0.03, anchor='center')

# Colors Frames and Labels
entry_bg_color = "#3E3A39"  # Dark brown
entry_fg_color = "white"
label_fg_color = "#5D3D21"

# Frame 1 - Employee Information
id_label = Label(window, font=font1, text='Employee ID:', fg=label_fg_color)
id_label.place(x=20, y=160)

id_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
id_entry.place(x=270, y=160)


generate_employee_id()

# Name
name_label = Label(window, font=font1, text='Name:', fg=label_fg_color)
name_label.place(x=20, y=220)

name_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
name_entry.place(x=270, y=220)

# Contact Number
contact_no_label = Label(window, font=font1, text='Contact Number:', fg=label_fg_color)
contact_no_label.place(x=20, y=280)

contact_no_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
contact_no_entry.place(x=270, y=280)

# NIC
nic_label = Label(window, font=font1, text='NIC Number:', fg=label_fg_color)
nic_label.place(x=20, y=340)

nic_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
nic_entry.place(x=270, y=340)

# Role
role_label = Label(window, font=font1, text='Role:', fg=label_fg_color)
role_label.place(x=20, y=400)

role_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
role_entry.place(x=270, y=400)

# Username
username_label = Label(window, font=font1, text='Username:', fg=label_fg_color)
username_label.place(x=20, y=460)

username_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
username_entry.place(x=270, y=460)

# Password
password_label = Label(window, font=font1, text='Password:', fg=label_fg_color)
password_label.place(x=20, y=520)

password_entry = Entry(window, font=font1, bg=entry_bg_color, fg=entry_fg_color, width=20, borderwidth=2)
password_entry.place(x=270, y=520)

# Button Styles
button_fg_color = "#5D3D21"
button_hover_color = "white"

# Buttons
add_button = Button(
    window,
    command=insert,
    text='Add Employee',
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
    command=new_employee,
    text='New Employee',
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
    text='Update Employee',
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
    text='Delete Employee',
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
tree['columns'] = ('ID', 'Name', 'Contact_No', 'NIC', 'Role', 'User _name', 'Password')  # Corrected column name

tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', anchor=tk.CENTER, width=120)
tree.column('Name', anchor=tk.CENTER, width=120)
tree.column('Contact_No', anchor=tk.CENTER, width=120)
tree.column('NIC', anchor=tk.CENTER, width=120)
tree.column('Role', anchor=tk.CENTER, width=120)
tree.column('User _name', anchor=tk.CENTER, width=120)
tree.column('Password', anchor=tk.CENTER, width=120)

tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('Contact_No', text='Contact_No')
tree.heading('NIC', text='NIC')
tree.heading('Role', text='Role')
tree.heading('User _name', text='User  Name')
tree.heading('Password', text='Password')
# Apply style to the Treeview
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview")
style.map('Treeview', background=[('selected', '#000')])
tree.place(x=650, y=160)

back_button = Button(window, text="Back", font=font2, command=back,
                     width=8, height=1, fg="#5D3D21", relief="solid")
back_button.place(x=1350, y=760)

tree.bind('<ButtonRelease>', display_data)
add_to_treeview()

window.mainloop()