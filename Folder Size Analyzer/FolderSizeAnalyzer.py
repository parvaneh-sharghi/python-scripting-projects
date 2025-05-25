import os
import csv
import concurrent.futures
import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from openpyxl import Workbook
import threading
import matplotlib
import subprocess
import sys
import arabic_reshaper
from bidi.algorithm import get_display

# Use a generic font
matplotlib.rcParams['font.family'] = ['DejaVu Sans']

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

folder_sizes_global = {}  # Store for Excel export
progress_label = None

# Function to calculate size of a folder in bytes
def get_folder_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                if os.path.isfile(fp):
                    total += os.path.getsize(fp)
            except:
                continue
    return total

# Function to update chart and UI after thread finishes
def display_chart(folder_sizes):
    global folder_sizes_global

    if not folder_sizes:
        messagebox.showinfo("Result", "No subfolders found.")
        return

    # Sort and filter folders larger than 1 KB
    sorted_sizes = {k: v for k, v in sorted(folder_sizes.items(), key=lambda item: item[1], reverse=True) if v > 1024}
    if not sorted_sizes:
        messagebox.showinfo("Result", "No folders larger than 1KB.")
        return

    folder_sizes_global = sorted_sizes  # Save for Excel export

    # Display Bar Chart with better spacing and visible small sizes
    labels = [get_display(arabic_reshaper.reshape(k)) for k in sorted_sizes.keys()]
    sizes = [max(s / (1024**2), 0.1) for s in sorted_sizes.values()]  # Convert to MB, show at least 0.1 MB
    plt.figure(figsize=(10, len(labels) * 0.5 + 1))
    bars = plt.barh(labels, sizes, color='skyblue')
    plt.xlabel('Size (MB)')
    plt.title('Folder Size Distribution')
    plt.tight_layout()
    plt.gca().invert_yaxis()
    for bar, size in zip(bars, sizes):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f"{size:.2f} MB", va='center')
    plt.show()

    if progress_label:
        progress_label.configure(text="")

# Background thread function
def background_analysis(folder_path):
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    full_paths = [os.path.join(folder_path, f) for f in subfolders]
    folder_sizes = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_folder = {executor.submit(get_folder_size, path): name for path, name in zip(full_paths, subfolders)}
        for future in concurrent.futures.as_completed(future_to_folder):
            name = future_to_folder[future]
            try:
                size = future.result()
                folder_sizes[name] = size
            except:
                continue

    app.after(0, lambda: display_chart(folder_sizes))

# Function to analyze sizes and start background thread
def analyze_folder():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    if progress_label:
        progress_label.configure(
            text="Analyzing, please wait...",
            text_color="#0D47A1",
            fg_color="#BBDEFB"
        )

    thread = threading.Thread(target=background_analysis, args=(folder_path,))
    thread.start()

# Function to export folder sizes to Excel
def export_to_excel():
    if not folder_sizes_global:
        messagebox.showwarning("Warning", "Please analyze a folder first.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not save_path:
        return

    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Folder Sizes"
        ws.append(["Folder Name", "Size (MB)"])

        for name, size in folder_sizes_global.items():
            ws.append([name, round(size / (1024**2), 2)])

        wb.save(save_path)
        messagebox.showinfo("Success", f"Excel file saved at:\n{save_path}")

        try:
            os.startfile(save_path) if os.name == 'nt' else subprocess.call(['open', save_path])
        except:
            pass
    except PermissionError:
        messagebox.showerror("Error", "Failed to save Excel file. Please close it if it is already open.")

# GUI Setup
app = ctk.CTk()
app.title("Folder Size Analyzer")
app.geometry("420x270")

ctk.CTkLabel(app, text="Analyze Folder Sizes", font=("Arial", 20)).pack(pady=15)
ctk.CTkButton(app, text="Select Folder and Analyze", command=analyze_folder).pack(pady=5)
ctk.CTkButton(app, text="Export to Excel", command=export_to_excel).pack(pady=5)
ctk.CTkButton(app, text="Exit", command=app.quit).pack(pady=5)
progress_label = ctk.CTkLabel(app, text="")
progress_label.pack(pady=5)

app.mainloop()
