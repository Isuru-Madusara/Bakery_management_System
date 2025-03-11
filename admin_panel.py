from tkinter import *
import os

window = Tk()
window.state('zoomed')
window.title("Admin Panel")
window.config(background="white")

# Configure grid to center all elements
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)


def employee_management():
    print("Logout")
    window.destroy()
    os.system("python employee_management.py")
    window.deiconify()

def item_management():
    print("Logout")
    window.destroy()
    os.system("python Item_management.py")
    window.deiconify()

def shop_management():
    print("Logout")
    window.destroy()
    os.system("python Shops_management.py")
    window.deiconify()

def orders():
    print("Logout")
    window.destroy()
    os.system("python orders_main.py")
    window.deiconify()

def bills():
    print("Logout")
    window.destroy()
    os.system("python invoice_management.py")
    window.deiconify()

def logout_click():
    print("Logout")
    window.destroy()
    os.system("python admin_login.py")
    window.deiconify()

#window label
label = Label(window,
              text="Dashboard",
              font=('Arial',40 ,'bold'),
              fg="#8A685C",
              bg="white"
              )
label.grid(row=0,column=0)

#window main frame
frame = Frame(window,bg="white")
frame.grid(row=1,column=0)

#item frame
item_frame = Frame(frame, bg="#8A685C", padx=5, pady=5)  # Border
item_frame.pack(side=LEFT, padx=40)

#item button
photo_Item = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/Item.png")
item_button = Button(item_frame,
                     command=item_management,
                     text="Item Management",
                     image=photo_Item,
                     font=('Arial',20,'bold'),
                     fg="#8A685C",
                     compound='bottom',
                     padx=40,
                     pady=10)

item_button.pack()

#Employee button
employee_frame = Frame(frame, bg="#8A685C", padx=5, pady=5)  # Border
employee_frame.pack(side=LEFT, padx=40)

photo_employee = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/emplo.png")
employee_button = Button(employee_frame,
                         command=employee_management,
                         text="Employee Management",
                         font=('Arial',20,'bold'),
                         fg="#8A685C",
                         image=photo_employee,
                         compound='bottom',
                         padx = 5,
                         pady = 10)
employee_button.pack()

#Shops button
shop_frame = Frame(frame, bg="#8A685C", padx=5, pady=5)  # Border
shop_frame.pack(side=LEFT, pady=40,padx=40)

photo_shop = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/shop.png")
shop_button = Button(shop_frame,
                         text="Shops Management",
                         command=shop_management,
                         font=('Arial',20,'bold'),
                         fg="#8A685C",
                         image=photo_shop,
                         compound='bottom',
                         padx=30,
                         pady=18
                         )
shop_button.pack()

#_________________________________________________________________________________________________________#
# Down frame
frame2 = Frame(window, bg="white")
frame2.grid(row=2, column=0)

# Receipt management
receipt_frame = Frame(frame2, bg="#8A685C", padx=5, pady=5)  # Border
receipt_frame.pack(side=LEFT, pady=40, padx=40)

# Button inside Receipt Frame
photo_invoice = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/invoice.png")
receipt_button = Button(receipt_frame,
                        text="Invoice Management",
                        command=bills,
                        font=('Arial', 20, 'bold'),
                        fg="#8A685C",
                        image=photo_invoice,
                        compound='bottom',
                        padx=25,
                        pady=10
                         )
receipt_button.pack()

# Delivery management
delivery_frame = Frame(frame2, bg="#8A685C", padx=5, pady=5)  # Border
delivery_frame.pack(side=LEFT, pady=40, padx=40)

# Button inside Delivery Frame
photo_delivery = PhotoImage(file="C:/Users/isuru/PycharmProjects/Bakery_and_shop_management/images/delivery.png")
delivery_button = Button(delivery_frame,
                         text="Make Orders to Shops",
                         command=orders,
                         font=('Arial', 20, 'bold'),
                         fg="#8A685C",
                         image=photo_delivery,
                         compound='bottom',
                         padx=20,
                         pady=40
                         )
delivery_button.pack()

#####################################
logout_frame = Frame(window, bg="white")
logout_frame.grid(row=3, column=0)

# Admin button
logout_frame = Frame(logout_frame, bg="#8A685C", padx=2, pady=2)  # Border
logout_frame.grid()


logout_button = Button(logout_frame,
                      text="Logout",

                      command=logout_click,
                      fg="#8A685C",
                      font=('Arial', 20, 'bold'),compound='bottom',
                      borderwidth=0,
                      )
logout_button.pack()

window.mainloop()