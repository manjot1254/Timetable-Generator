import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3
from tkinter import *

global username
global password

def destroy():
    exit()

def hashPassword(password):
    # convert password to bytes (strings in Python are Unicode by default, while hash functions expect byte data)
    passwordBytes = password.encode('utf-8')

    # hash password using SHA-256
    hashedPassword = hashlib.sha256(passwordBytes).hexdigest()

    return hashedPassword

def signup():
    lower, upper, digit = 0, 0, 0

    username = usernameInput.get()
    password = passwordInput.get()
    x = 0

    for char in password:
        # counting lowercase alphabets
        if (char.islower()):
            lower += 1
        # counting uppercase alphabets
        if (char.isupper()):
            upper += 1
        # counting digits
        if (char.isdigit()):
            digit += 1
    while not (lower >= 1 and upper >= 1 and digit >= 1):
        password_error = messagebox.showerror("Error", "Invalid password - include a number, lowercase and uppercase letter")
        if password_error:
            destroy()
    if lower >= 1 and upper >= 1 and digit >= 1:
        x = x + 1

        while len(username) < 4 or len(username) > 20:
            messagebox.showerror("Error", "Username must be between 4 and 20 characters long")
            username = usernameInput.get()
        # if the entered username and password are valid, they are written to a database
        else:
            x = x + 1

        if x == 2:
            messagebox.showinfo("Success", "Valid username and password")
            conn = sqlite3.connect("login.db")
            cursor = conn.cursor()

            enteredPassword = passwordInput.get()
            hashedPassword = hashPassword(enteredPassword)

            # creates table in database, which is now in comments after first run as already created
            #cursor.execute("""CREATE TABLE users (
            #                username text,
            #                password text
            #        )""")
            cursor.execute('INSERT INTO users VALUES (:username, :password)',
                    {
                       'username': username,
                       'password': hashedPassword
                    })
            conn.commit()
            conn.close()

def login():
    username = usernameInput.get()
    password = passwordInput.get()

    # requires a username and password to be inputted to compare with database
    if username and password:
        # variable used and incremented if a record matched so error only outputted if no record matched
        x = 0
        # queries database and fetches all records
        conn = sqlite3.connect("login.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        records = cursor.fetchall()

        # if fetched records match, login is successful as the inputted details are valid
        for i in records:
            if username and hashPassword(password) in i:
                messagebox.showinfo("Success", "Login successful")
                x = x + 1
        if x == 0:
            messagebox.showerror("Error", "Invalid login details")
        conn.commit()
        conn.close()
    else:
        messagebox.showerror("Error", "Please enter a username and password")

# root allows configuration of background colour and displays window, which is then titled
root = tk.Tk()
root.title("Sign-Up and Log-in")
root.configure(background="papaya whip")

# creates entry widgets to write username and passwords in for signing up/logging in
label_username = tk.Label(root, bg="lemon chiffon", text="Username:")
label_password = tk.Label(root, bg="lemon chiffon", text="Password:")
usernameInput = Entry(root, bg="linen", width=40)
passwordInput = Entry(root, show="*", bg="linen", width=40)

# puts labels and buttons on the grid, linking to the relevant subroutines
label_username.grid(row=0, column=0)
label_password.grid(row=1, column=0)
usernameInput.grid(row=0, column=1)
passwordInput.grid(row=1, column=1)
button_register = tk.Button(root, bg="lavender blush", text="Sign-Up", command=signup)
button_register.grid(row=3, column=0, columnspan=2)
button_login = tk.Button(root, bg="lavender blush", text="Login", command=login)
button_login.grid(row=2, column=0, columnspan=2)


root.mainloop()
