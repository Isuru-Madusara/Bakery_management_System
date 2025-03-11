import subprocess
from tkinter import *
import os


window = Tk()
window.state('zoomed')
window.title("Shops Orders")
window.config(background="white")

# Configure grid for center
window.grid_rowconfigure(0, weight=0)  # Top label
window.grid_rowconfigure(1, weight=1)  # Main frame
window.grid_rowconfigure(2, weight=0)  # Logout frame
window.grid_columnconfigure(0, weight=1)

def back():
    print("Returning to welcome page...")
    window.destroy()
    subprocess.run(["python", "admin_panel.py"])

def make_order():
    print("Logout")
    window.destroy()
    os.system("python make_orders.py")
    window.deiconify()

def order_management():
    print("Logout")
    window.destroy()
    os.system("python order_history.py")
    window.deiconify()

# Window label
label = Label(
    window,
    text="Shops Orders",
    font=('Arial', 60, 'bold'),
    fg="#8A685C",
    bg="white"
)
label.grid(row=0, column=0, pady=20)

frame = Frame(window, bg="white")
frame.grid(row=1, column=0)

employee_frame = Frame(frame, bg="#8A685C", padx=5, pady=5)  # Border
employee_frame.grid(row=0, column=0, padx=30, pady=10, sticky='nsew')

photo_employee = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/delivery2.png")
employee_button = Button(
    employee_frame,
    command=make_order,
    text="Make Order",
    font=('Arial', 20, 'bold'),
    fg="#8A685C",
    image=photo_employee,
    compound='bottom',
    padx=55,
    pady=25
)
employee_button.pack()
##########################################################################################################

delivery_frame = Frame(frame, bg="#8A685C", padx=5, pady=5)  # Border
delivery_frame.grid(row=0, column=1, padx=30, pady=10, sticky='nsew')

photo_delivery = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/delivery2.png")
delivery_button = Button(
    delivery_frame,
    command=order_management,
    text="Orders History",
    font=('Arial', 20, 'bold'),
    fg="#8A685C",
    image=photo_delivery,
    compound='bottom',
    padx=25,
    pady=25
)
delivery_button.pack()
#########################################
# Logout frame
logout_frame = Frame(window, bg="Black")
logout_frame.grid(row=2, column=0)

font2 = ('Arial', 15, 'bold')

back_button = Button(window, text="Back",font=font2, command=back,
                       width=8, height=1, fg="#5D3D21", relief="solid")
back_button.place(x=1350,y=760)

window.mainloop()