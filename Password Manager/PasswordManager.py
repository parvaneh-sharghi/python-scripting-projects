import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import string
import pyperclip
from cryptography.fernet import Fernet

# File paths
DATA_FILE = 'passwords.json'
KEY_FILE = 'secret.key'

# Generate or load encryption key
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as file:
            file.write(key)
        return key

# Encrypt a message
def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

# Decrypt a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

# Save password to file
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showwarning("Warning", "Please fill out all fields.")
        return

    encrypted_password = encrypt_message(password, key)
    new_data = {website: {"username": username, "password": encrypted_password.decode()}}

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    data.update(new_data)

    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Password saved successfully.")

# Retrieve and show password
def find_password():
    website = website_entry.get()
    if not website:
        messagebox.showwarning("Warning", "Please enter a website.")
        return

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Data file is corrupted.")
                return
    else:
        messagebox.showinfo("Info", "No data file found.")
        return

    if website in data:
        username = data[website]['username']
        encrypted_password = data[website]['password']
        try:
            password = decrypt_message(encrypted_password.encode(), key)
        except:
            messagebox.showerror("Error", "Failed to decrypt password.")
            return
        messagebox.showinfo(website, f"Username: {username}\nPassword: {password}")
        pyperclip.copy(password)
    else:
        messagebox.showinfo("Info", f"No details found for '{website}'.")

# Generate random secure password
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# GUI setup
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Labels and entries
tk.Label(window, text="Website:").grid(row=0, column=0)
website_entry = tk.Entry(window, width=35)
website_entry.grid(row=0, column=1, columnspan=2)
website_entry.focus()

tk.Label(window, text="Username/Email:").grid(row=1, column=0)
username_entry = tk.Entry(window, width=35)
username_entry.grid(row=1, column=1, columnspan=2)

tk.Label(window, text="Password:").grid(row=2, column=0)
password_entry = tk.Entry(window, width=21)
password_entry.grid(row=2, column=1)

# Buttons
tk.Button(window, text="Generate Password", command=generate_password).grid(row=2, column=2)
tk.Button(window, text="Save", width=36, command=save_password).grid(row=3, column=1, columnspan=2)
tk.Button(window, text="Search", width=36, command=find_password).grid(row=4, column=1, columnspan=2)

# Load encryption key
key = load_key()

window.mainloop()
