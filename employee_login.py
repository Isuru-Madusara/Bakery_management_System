from tkinter import *
import sqlite3
import os

def login():
    username = UserNameEntry.get()
    password = PasswordEntry.get()

    if validate_login(username, password):
        feedbackLabel.config(text="Login Successful", fg="green")
        print("Valid Login")
        window.destroy()
        os.system("python employee_panel.py")
    else:
        feedbackLabel.config(text="Invalid Username or Password", fg="red")
        print("Invalid Login")

#check the user name are passwords are correct according employee table
def validate_login(username, password):
    try:

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Employees WHERE user_name = ? AND password = ?''', (username, password))
            employee = cursor.fetchone()

            if employee:
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return False

def back():
    print("Returning to welcome page...")
    window.destroy()
    os.system("python Welcome_Login.py")

# Window setup
window = Tk()
window.title("Employee Login Page")
window.state('zoomed')
window.geometry("500x400")
window.config(background="White")

# Border setup
border_frame = Frame(window, bg="#8A685C", padx=2, pady=2)
border_frame.place(relx=0.5, rely=0.5, anchor="center")

# Inner frame with content
frame = Frame(border_frame, pady=50, padx=20)
frame.pack()

# Login title
label = Label(frame, text="Employee Login", fg="#5D3D21", font=("Arial", 25, 'bold'), pady=15)
label.grid(row=0, column=0, columnspan=2)

# Username input
UserNameLabel = Label(frame, text="Username", fg="#5D3D21", pady=20, padx=20, font=("Arial", 17))
UserNameLabel.grid(row=1, column=0)

UserNameEntry = Entry(frame)
UserNameEntry.grid(row=1, column=1, padx=20)

# Password input
PasswordLabel = Label(frame, text="Password", fg="#5D3D21", pady=15, font=("Arial", 17))
PasswordLabel.grid(row=2, column=0)

PasswordEntry = Entry(frame, show="*")
PasswordEntry.grid(row=2, column=1)

# Feedback Label
feedbackLabel = Label(frame, text="", fg="White", font=("Arial", 12, "italic"))
feedbackLabel.grid(row=3, column=0, columnspan=2, pady=10)

# Login Button
login_frame = Frame(frame, bg="#8A685C", padx=2, pady=2)
login_frame.grid(row=4, column=0, columnspan=2, pady=20)

login_button = Button(login_frame, text="Login", command=login, width=10, height=2, fg="#5D3D21", relief="flat")
login_button.pack()

# Back Button
back_frame = Frame(frame, bg="#8A685C", padx=2, pady=2)
back_frame.grid(row=5, column=0, columnspan=2, pady=10)

back_button = Button(back_frame, text="Back", command=back, width=10, height=2, fg="#5D3D21", relief="flat")
back_button.pack()

window.mainloop()