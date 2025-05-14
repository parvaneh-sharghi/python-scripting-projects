# 💾 Auto File Backup Tool (Python GUI)

This is a simple and modern **Python GUI tool** to help you easily back up files and folders with just a few clicks. It automatically creates a timestamped backup of the selected source folder into your chosen destination.

Built with Python and [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for a sleek and user-friendly interface.

---

## ✅ Features

- Select any folder as source.
- Choose a destination where the backup will be saved.
- Creates a new folder with the current date and time as the name.
- Copies all files and subfolders to the backup folder.
- User-friendly interface — no technical knowledge required.

---

## 📦 Technologies Used

- Python 3.x
- `customtkinter` for GUI
- `shutil` and `os` for file system operations
- `datetime` for timestamping backups

---

## 🔧 How to Use

1. Run the program (or open the `.exe` installer version if available).
2. Click **Browse** to select the folder you want to back up.
3. Click **Browse** again to choose the destination folder.
4. Click **Start Backup**.
5. A new folder like `backup_20240514_154520` will be created with all the contents of the source folder.

---

## 🧩 Installation

### Option 1: Run from Python

```bash
pip install customtkinter
python backup_tool.py
