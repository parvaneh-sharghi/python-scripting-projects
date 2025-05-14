import os
import shutil
import psutil
import customtkinter as ctk
from tkinter import messagebox
import winshell  # For handling Recycle Bin
import datetime  # For timestamps and reports

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Log file for cleanup reports
log_file_path = os.path.join(os.getcwd(), "cleanup_report.txt")

# Function to write to log file
def log_report(message):
    with open(log_file_path, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")

# Function to get size of a folder
def get_folder_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total

# Function to clear temp files
def clear_temp():
    temp_paths = [os.getenv("TEMP"), os.path.join(os.getenv("SystemRoot"), "Temp")]
    deleted_files = 0
    for path in temp_paths:
        if path and os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                        deleted_files += 1
                    except:
                        continue
                for dir in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                    except:
                        continue
    messagebox.showinfo("Cleaner", f"Cleaned {deleted_files} files from temp folders.")
    log_report(f"Deleted {deleted_files} temp files.")

# Function to empty Recycle Bin
def empty_recycle_bin():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        messagebox.showinfo("Recycle Bin", "Recycle Bin emptied successfully.")
        log_report("Recycle Bin emptied successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to empty Recycle Bin: {e}")
        log_report(f"Error emptying Recycle Bin: {e}")

# Function to show system info
def show_system_info():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    info = (
        f"CPU Usage: {cpu}%\n"
        f"RAM Usage: {ram.percent}% ({ram.used // (1024 ** 2)}MB / {ram.total // (1024 ** 2)}MB)\n"
        f"Disk Usage: {disk.percent}% ({disk.used // (1024 ** 3)}GB / {disk.total // (1024 ** 3)}GB)"
    )
    messagebox.showinfo("System Info", info)
    log_report("Viewed system info.")

# GUI setup
app = ctk.CTk()
app.title("System Cleaner & Optimizer")
app.geometry("420x380")

ctk.CTkLabel(app, text="System Cleaner & Optimizer", font=("Arial", 20)).pack(pady=20)
ctk.CTkButton(app, text="Clean Temp Files", command=clear_temp).pack(pady=10)
ctk.CTkButton(app, text="Empty Recycle Bin", command=empty_recycle_bin).pack(pady=10)
ctk.CTkButton(app, text="Show System Info", command=show_system_info).pack(pady=10)
ctk.CTkButton(app, text="Exit", command=app.quit).pack(pady=20)

# Auto execution hint (for Task Scheduler)
info_label = ctk.CTkLabel(app, text="Tip: Schedule this app using Windows Task Scheduler\nfor automatic cleaning.", font=("Arial", 10))
info_label.pack(pady=(10, 0))

app.mainloop()
