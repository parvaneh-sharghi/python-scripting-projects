import os
import shutil
import platform
import customtkinter as ctk
from tkinter import messagebox
import ctypes  # For memory info on Windows
import datetime
import time  # For CPU usage measurement

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Ensure logs are stored in a 'logs' subfolder in the project directory
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "cleanup_report.txt")

# Function to write messages to a log file
def log_report(message):
    with open(log_file_path, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")

# Function to clear temporary files using fast system commands
def clear_temp():
    deleted_files = 0
    temp_path = os.getenv("TEMP")
    if temp_path and os.path.exists(temp_path):
        for root, dirs, files in os.walk(temp_path):
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
    messagebox.showinfo("Cleaner", f"Cleaned {deleted_files} files from temp folder.")
    log_report(f"Deleted {deleted_files} temp files.")

# Function to empty the Recycle Bin using ctypes
def empty_recycle_bin():
    try:
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
        messagebox.showinfo("Recycle Bin", "Recycle Bin emptied successfully.")
        log_report("Recycle Bin emptied successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to empty Recycle Bin: {e}")
        log_report(f"Error emptying Recycle Bin: {e}")

# Function to show system info (without CPU temperature)
def show_system_info():
    try:
        sys_info = platform.uname()

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        memory = MEMORYSTATUSEX()
        memory.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))

        ram_used = (memory.ullTotalPhys - memory.ullAvailPhys) // (1024 ** 2)
        ram_total = memory.ullTotalPhys // (1024 ** 2)

        idle_time_start = ctypes.c_ulonglong()
        kernel_time_start = ctypes.c_ulonglong()
        user_time_start = ctypes.c_ulonglong()

        ctypes.windll.kernel32.GetSystemTimes(
            ctypes.byref(idle_time_start),
            ctypes.byref(kernel_time_start),
            ctypes.byref(user_time_start)
        )

        time.sleep(1)

        idle_time_end = ctypes.c_ulonglong()
        kernel_time_end = ctypes.c_ulonglong()
        user_time_end = ctypes.c_ulonglong()

        ctypes.windll.kernel32.GetSystemTimes(
            ctypes.byref(idle_time_end),
            ctypes.byref(kernel_time_end),
            ctypes.byref(user_time_end)
        )

        idle = idle_time_end.value - idle_time_start.value
        kernel = kernel_time_end.value - kernel_time_start.value
        user = user_time_end.value - user_time_start.value
        total = kernel + user
        cpu_usage = 100 - ((idle * 100) // total if total != 0 else 0)

        info = (
            f"System: {sys_info.system}\n"
            f"Node Name: {sys_info.node}\n"
            f"Release: {sys_info.release}\n"
            f"Version: {sys_info.version}\n"
            f"Machine: {sys_info.machine}\n"
            f"Processor: {sys_info.processor}\n"
            f"RAM Usage: {ram_used} MB / {ram_total} MB\n"
            f"CPU Usage: {cpu_usage}%"
        )
        messagebox.showinfo("System Info", info)
        log_report("Viewed system info.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch system info: {e}")
        log_report(f"Error fetching system info: {e}")

# GUI setup
app = ctk.CTk()
app.title("Lightweight System Cleaner")
app.geometry("420x400")

ctk.CTkLabel(app, text="System Cleaner (Fast & Light)", font=("Arial", 20)).pack(pady=20)
ctk.CTkButton(app, text="Clean Temp Files", command=clear_temp).pack(pady=10)
ctk.CTkButton(app, text="Empty Recycle Bin", command=empty_recycle_bin).pack(pady=10)
ctk.CTkButton(app, text="Show System Info", command=show_system_info).pack(pady=10)
ctk.CTkButton(app, text="Exit", command=app.quit).pack(pady=20)

app.mainloop()
