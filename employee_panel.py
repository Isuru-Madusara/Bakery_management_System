from tkinter import *
import os
import subprocess

# Initialize the main window
window = Tk()
window.state('zoomed')
window.title("Employee Panel")
window.config(background="white")

# Configure grid for centering
window.grid_rowconfigure(0, weight=0)  # Top label
window.grid_rowconfigure(1, weight=1)  # Main frame
window.grid_rowconfigure(2, weight=0)  # Logout frame
window.grid_columnconfigure(0, weight=1)

def billing_history():
    print("Opening Available Stock...")
    window.destroy()
    try:
        subprocess.run(["python", r"C:\Users\isuru\PycharmProjects\Bakery_and_shop_management\biliing_history.py"], check=True)
    except FileNotFoundError:
        print("Error: The employee_available_stock.py file was not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def billing():
    print("Returning to billing page...")
    window.destroy()
    try:
        subprocess.run(["python", r"C:\Users\isuru\PycharmProjects\Bakery_and_shop_management\billing_emp.py"], check=True)
    except FileNotFoundError:
        print("Error: The billing_by_employee.py file was not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def logout_click():
    print("Logging out...")
    window.destroy()
    try:
        subprocess.run(["python", r"C:\Users\isuru\PycharmProjects\Bakery_and_shop_management\employee_login.py"], check=True)
    except FileNotFoundError:
        print("Error: The employee_login.py file was not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Window label
label = Label(
    window,
    text="Dashboard",
    font=('Arial', 60, 'bold'),
    fg="#8A685C",
    bg="white"
)
label.grid(row=0, column=0, pady=20)

# Main frame for the dashboard content
frame = Frame(window, bg="white")
frame.grid(row=1, column=0)

# Employee frame (Example: Billing System)
employee_frame = Frame(frame, bg="#8A685C", padx=5, pady=5)  # Border
employee_frame.grid(row=0, column=0, padx=30, pady=10, sticky='nsew')

# Load and display the Billing System button with image
try:
    photo_employee = PhotoImage(file=r"C:\Users\isuru\PycharmProjects\Bakery_and_shop_management\images\chachier.png")
except TclError:
    print("Error: Billing image not found.")

employee_button = Button(
    employee_frame,
    text="Billing System",
    command=billing,
    font=('Arial', 20, 'bold'),
    fg="#8A685C",
    image=photo_employee,
    compound='bottom',
    padx=55,
    pady=25
)
employee_button.pack()

# Delivery frame (Example: Delivery Management)
delivery_frame = Frame(frame, bg="#8A685C", padx=5, pady=5)  # Border
delivery_frame.grid(row=0, column=1, padx=30, pady=10, sticky='nsew')

# Load and display the Delivery Management button with image
try:
    photo_delivery = PhotoImage(file=r"C:\Users\isuru\PycharmProjects\Bakery_and_shop_management\images\chachier.png")
except TclError:
    print("Error: Delivery image not found.")

delivery_button = Button(
    delivery_frame,
    text="Bills History",
    command=billing_history,
    font=('Arial', 20, 'bold'),
    fg="#8A685C",
    image=photo_delivery,
    compound='bottom',
    padx=35,
    pady=25
)
delivery_button.pack()

# Logout frame
logout_frame = Frame(window, bg="Black")
logout_frame.grid(row=2, column=0)

# Logout button
logout_button = Button(
    logout_frame,
    text="Logout",
    command=logout_click,
    fg="#8A685C",
    font=('Arial', 20, 'bold'),
    compound='bottom',
    borderwidth=0,
)
logout_button.pack()

# Start the GUI event loop
window.mainloop()