from tkinter import *
import os
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_db():
    with sqlite3.connect("admin_credentials.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                          )''')
        conn.commit()

def sign_up():
    username = UserNameEntry.get()
    password = PasswordEntry.get()

    if not username or not password:
        feedbackLabel.config(text="Username & Password required!", fg="red")
        return

    hashed_password = hash_password(password)  # Hash

    with sqlite3.connect("admin_credentials.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM admin WHERE username=?", (username,))

        if cursor.fetchone():
            feedbackLabel.config(text="Username already exists!", fg="red")
        else:
            cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, hashed_password))
            feedbackLabel.config(text="Sign Up Successful!", fg="green")
            print("Sign Up Successful!")
        conn.commit()

def login():
    username = UserNameEntry.get()
    password = PasswordEntry.get()

    if not username or not password:
        feedbackLabel.config(text="Username & Password required!", fg="red")
        return

    hashed_password = hash_password(password)  # Hash input password

    with sqlite3.connect("admin_credentials.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, hashed_password))
        admin = cursor.fetchone()

    if admin:
        feedbackLabel.config(text="Login Successful", fg="green")
        print("Valid Login")
        window.withdraw()
        os.system("python admin_panel.py")
    else:
        feedbackLabel.config(text="Invalid Username or Password", fg="red")
        print("Invalid Login")

def back():
    print("Returning to welcome page...")
    window.destroy()
    os.system("python welcome_Login.py")

create_db()

window = Tk()
window.state('zoomed')
window.config(background="White")
window.title("Admin Login Page")

# Border setup
border_frame = Frame(window, bg="#8A685C", padx=2, pady=2)
border_frame.place(relx=0.5, rely=0.5, anchor="center")

# Inner fram
frame = Frame(border_frame, pady=50, padx=20)
frame.pack()

# Login title
label = Label(frame, text="Admin Login", fg="#5D3D21", font=("Arial", 25, 'bold'), pady=15)
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
login_frame.grid(row=4, column=0, columnspan=1, pady=20)

login_button = Button(login_frame, text="Login", command=login, width=10, height=2, fg="#5D3D21", relief="flat")
login_button.pack()

# Back Button
back_frame = Frame(frame, bg="#8A685C", padx=2, pady=2)
back_frame.grid(row=4, column=1, columnspan=2, pady=20)

back_button = Button(back_frame, text="Back", command=back, width=10, height=2, fg="#5D3D21", relief="flat")
back_button.pack()

# Label for "Don't have an account?"
dont_have_account_label = Label(frame, text="Don't have an account?", fg="#5D3D21", font=("Arial", 12, "italic"))
dont_have_account_label.grid(row=5, column=0, columnspan=2, pady=10)

# Sign Up Button
sign_up_frame = Frame(frame, bg="#8A685C", padx=2, pady=2)
sign_up_frame.grid(row=6, column=0, columnspan=2, pady=20)

sign_up_button = Button(sign_up_frame, text="Sign Up", command=sign_up, width=10, height=2, fg="#5D3D21", relief="flat")
sign_up_button.pack()


window.mainloop()