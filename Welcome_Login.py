import os
from tkinter import *


window = Tk()
window.state('zoomed')
window.title("Main Window")


window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

label = Label(window,
              text="Welcome",
              font=('Arial', 70, 'bold'),
              fg="#5D3D21",
              pady=10)
label.grid(row=0, column=0)


# Functions
def user_click():
    print("User clicked")
    window.destroy()
    os.system("python employee_login.py")

def admin_click():
    print("Admin clicked")
    window.destroy()
    os.system("python admin_login.py")

# Frame for two users
button_frame = Frame(window,)
button_frame.grid(row=1, column=0)

# Admin button
admin_frame = Frame(button_frame, bg="#8A685C", padx=5, pady=5)  # Border
admin_frame.pack(side=LEFT, padx=50)

photo_admin = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/admin.png")
admin_button = Button(admin_frame,
                      text="Admin",
                      command=admin_click,
                      fg="#8A685C",
                      font=('Arial', 20, 'bold'),
                      image=photo_admin,
                      compound='bottom',
                      borderwidth=0,
                      padx=74,
                      pady=54)
admin_button.pack()


# User=Employee / button
user_frame = Frame(button_frame, bg="#8A685C", padx=5, pady=5)  # Border
user_frame.pack(side=RIGHT, padx=30)

photo_user = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/employee.png")
user_button = Button(user_frame,
                     text="Employee",
                     command=user_click,
                     fg="#8A685C",
                     font=('Arial', 20, 'bold'),
                     image=photo_user,
                     compound='bottom',
                     borderwidth=0,
                     padx=65,
                     pady=55)
user_button.pack()

window.mainloop()