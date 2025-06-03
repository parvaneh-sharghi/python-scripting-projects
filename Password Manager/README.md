 🔐 Password Manager (with Encryption + Tkinter GUI)

A simple yet secure password manager built with Python. This app allows users to **generate**, **store**, and **search** passwords using a graphical interface. All passwords are **encrypted using Fernet symmetric encryption** before being saved to disk.

---
📂 Project Structure

```
password_manager/
├── passwords.json          Encrypted saved passwords
├── secret.key              Encryption key file
├── main.py                 Main application code
├── README.md               Project documentation (this file)
```

---

🔧 Features

✅ Generate strong random passwords
✅ Save and encrypt credentials
✅ Retrieve and decrypt stored credentials
✅ Search passwords by website keyword
✅ Copy password to clipboard automatically
✅ User-friendly Tkinter GUI

---

🔐 Encryption

* Uses **`cryptography.Fernet`** to **encrypt passwords** before saving.
* A **key file (`secret.key`)** is automatically created on first run.
* Never share your `secret.key` with anyone!

---

🧠 How It Works

1. Save Password

* Enter the website, username/email, and password.
* Click **"Save"** — the password is encrypted and saved in `passwords.json`.

2. Generate Password

* Click **"Generate Password"** — a secure 12-character password appears.
* It is automatically copied to your clipboard.

3. Search for Saved Passwords

* Enter a keyword for the website.
* Click **"Search"** — all matching records are decrypted and shown in a table.

---

🔤 Example JSON Format (Encrypted)

```json
{
  "github.com": {
    "username": "you@example.com",
    "password": "gAAAAABlYOg9f0M..."
  }
}
```

> The `password` is stored in encrypted form and decrypted when displayed in the GUI.

---

🖼️ GUI Preview (Widgets Layout)

```
[ Website:        (__________)              (Search)          ]
[ Username/Email: (_______________________)                   ]
[ Password:       (__________) (Generate Password)            ]
[                             (Save)                          ]

---------------------------------------------------------------
[      Website      |     Username      |     Password        ]
[  google.com       |  me@gmail.com     |  hunter2            ]
[  github.com       |  you@domain.com   |  supersecurepwd     ]
```

---

📦 Requirements

* Python 3.6+
* Install required packages:

```bash
pip install cryptography pyperclip
```

---

▶️ Running the App

```bash
python main.py
```

On first run:

* A `secret.key` will be generated
* A `passwords.json` file will be created on saving

---

📌 Notes

* All password data is local — no data is sent online.
* Always **backup** your `secret.key`. If it's lost, you can't decrypt saved passwords.
* Keep the GUI simple for usability.

---

✨ Future Ideas

* Add a master password at startup
* Export/Import encrypted data
* Auto-fill passwords in browsers (advanced)

