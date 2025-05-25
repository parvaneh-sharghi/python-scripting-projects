import os
import concurrent.futures
import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from openpyxl import Workbook
import threading
import matplotlib
import subprocess
import arabic_reshaper
from bidi.algorithm import get_display
import time

# Set default appearance and theme for CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Global variables
folder_sizes_global = {}  # Stores folder size data for Excel export
progress_label = None  # Label to show progress status
analyze_button = None  # Analyze button to be disabled during processing
timer_label = None  # Label to show timer during analysis

# Set default font for charts
matplotlib.rcParams['font.family'] = ['DejaVu Sans']

# Function to calculate size of a folder (in bytes)
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

# Display chart after folder size calculation is complete
def display_chart(folder_sizes):
    global folder_sizes_global

    if not folder_sizes:
        messagebox.showinfo("Result", "No subfolders found.")
        return

    # Sort and filter folders with size > 1KB
    sorted_sizes = {k: v for k, v in sorted(folder_sizes.items(), key=lambda item: item[1], reverse=True) if v > 1024}
    if not sorted_sizes:
        messagebox.showinfo("Result", "No folders larger than 1KB.")
        return

    folder_sizes_global = sorted_sizes  # Save data for export

    # Prepare data for bar chart
    labels = [get_display(arabic_reshaper.reshape(k)) for k in sorted_sizes.keys()]
    sizes = [max(s / (1024**2), 0.1) for s in sorted_sizes.values()]  # Convert to MB, minimum 0.1 MB for visibility

    # Plot horizontal bar chart
    plt.figure(figsize=(10, len(labels) * 0.5 + 1))
    bars = plt.barh(labels, sizes, color='skyblue')
    plt.xlabel('Size (MB)')
    plt.title('Folder Size Distribution')
    plt.tight_layout()
    plt.gca().invert_yaxis()  # Show largest folder on top

    # Add size labels to bars
    for bar, size in zip(bars, sizes):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f"{size:.2f} MB", va='center')

    plt.show()

    # Reset UI labels and buttons
    if progress_label:
        progress_label.configure(text="")
    if timer_label:
        timer_label.configure(text="")
    if analyze_button:
        analyze_button.configure(state="normal")

# Run folder analysis in a background thread
def background_analysis(folder_path):
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    full_paths = [os.path.join(folder_path, f) for f in subfolders]
    folder_sizes = {}

    # Use thread pool for concurrent folder size computation
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

# Trigger analysis when user selects a folder
def analyze_folder():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    # Show progress message
    if progress_label:
        progress_label.configure(
            text="Analyzing, please wait...",
            text_color="#0D47A1",
            fg_color="#BBDEFB"
        )

    # Initialize and display timer
    if timer_label:
        timer_label.configure(text="Timer: 0 sec")
    if analyze_button:
        analyze_button.configure(state="disabled")

    def update_timer():
        start_time = time.time()
        while analyze_button.cget("state") == "disabled":
            elapsed = int(time.time() - start_time)
            app.after(0, lambda e=elapsed: timer_label.configure(text=f"Timer: {e} sec"))
            time.sleep(1)

    threading.Thread(target=update_timer, daemon=True).start()
    threading.Thread(target=background_analysis, args=(folder_path,), daemon=True).start()

# Export analysis result to Excel file
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

        # Write folder size data to sheet
        for name, size in folder_sizes_global.items():
            ws.append([name, round(size / (1024**2), 2)])

        wb.save(save_path)
        messagebox.showinfo("Success", f"Excel file saved at:\n{save_path}")

        # Attempt to open saved Excel file
        try:
            os.startfile(save_path) if os.name == 'nt' else subprocess.call(['open', save_path])
        except:
            pass
    except PermissionError:
        messagebox.showerror("Error", "Failed to save Excel file. Please close it if it is already open.")

# GUI Setup
app = ctk.CTk()
app.title("Folder Size Analyzer")
app.geometry("450x340")

# Title label
ctk.CTkLabel(app, text="Analyze Folder Sizes", font=("Arial", 20)).pack(pady=10)

# Main buttons
analyze_button = ctk.CTkButton(app, text="Select Folder and Analyze", command=analyze_folder)
analyze_button.pack(pady=5)
ctk.CTkButton(app, text="Export to Excel", command=export_to_excel).pack(pady=5)
ctk.CTkButton(app, text="Exit", command=app.quit).pack(pady=5)

# Labels for progress and timer
progress_label = ctk.CTkLabel(app, text="")
progress_label.pack(pady=5)
timer_label = ctk.CTkLabel(app, text="")
timer_label.pack(pady=5)

app.mainloop()
