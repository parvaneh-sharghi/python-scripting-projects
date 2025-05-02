import os
import shutil
import customtkinter as ctk  # Modern themed widgets
from tkinter import filedialog, messagebox, Listbox, MULTIPLE, END  # Use tkinter listbox for multi-select

ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

# Function to organize files by their extension (type)
def organize_files_by_type(source_folder, target_folder_name, extensions):
    if not os.path.exists(source_folder):
        messagebox.showerror("Error", f"Source folder '{source_folder}' does not exist.")
        return

    extensions = {ext.strip().lower().strip('.') for ext in extensions.split(',') if ext.strip()}
    if not extensions:
        messagebox.showwarning("Warning", "No valid file extensions provided.")
        return

    target_folder = os.path.join(source_folder, target_folder_name)
    os.makedirs(target_folder, exist_ok=True)

    moved_files = 0
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path):
            _, extension = os.path.splitext(filename)
            extension = extension.lower().strip('.')
            if extension in extensions:
                shutil.move(file_path, os.path.join(target_folder, filename))
                moved_files += 1

    if moved_files == 0:
        messagebox.showinfo("Result", "No matching files found to move.")
    else:
        messagebox.showinfo("Result", f"Successfully moved {moved_files} file(s) to '{target_folder_name}'.")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, ctk.END)
        folder_entry.insert(0, folder_selected)

def select_all():
    listbox.select_set(0, END)

def deselect_all():
    listbox.selection_clear(0, END)

def start_organizing():
    source = folder_entry.get().strip()
    target = target_entry.get().strip()
    selected_items = listbox.curselection()
    selected_extensions = [listbox.get(i) for i in selected_items]
    custom_extensions = custom_extension_entry.get().strip()

    if not source or not target:
        messagebox.showwarning("Warning", "Please fill in both folder fields.")
        return

    all_extensions = selected_extensions[:]
    if custom_extensions:
        all_extensions += [ext.strip() for ext in custom_extensions.split(',') if ext.strip()]

    if not all_extensions:
        messagebox.showwarning("Warning", "Please select or enter at least one file extension.")
        return

    extensions_string = ','.join(all_extensions)
    organize_files_by_type(source, target, extensions_string)

# GUI setup
app = ctk.CTk()
app.title("Custom File Organizer")
app.geometry("560x650")

# Folder selection
ctk.CTkLabel(app, text="Select folder to search:").pack(pady=(10, 0))
folder_frame = ctk.CTkFrame(app)
folder_frame.pack(pady=5)
folder_entry = ctk.CTkEntry(folder_frame, width=400)
folder_entry.pack(side="left", padx=5)
ctk.CTkButton(folder_frame, text="Browse", command=browse_folder).pack(side="left")

# Target folder name
ctk.CTkLabel(app, text="Folder name to move files into:").pack(pady=(10, 0))
target_entry = ctk.CTkEntry(app, width=450)
target_entry.pack(pady=5)

# Multi-select listbox for file types
ctk.CTkLabel(app, text="Select one or more file types:").pack(pady=(10, 0))
listbox = Listbox(app, selectmode=MULTIPLE, width=60, height=12)
listbox.pack(pady=5)
file_extensions = sorted([
    '7z', 'aac', 'apk', 'avi', 'bmp', 'css', 'csv', 'doc', 'docx', 'exe', 'flv', 'gif', 'gz', 'html', 'ico', 'jpeg', 'jpg',
    'js', 'json', 'mkv', 'mov', 'mp3', 'mp4', 'msi', 'odt', 'ogg', 'pdf', 'png', 'ppt', 'pptx', 'py', 'rar', 'rtf',
    'tar', 'tsv', 'tiff', 'txt', 'wav', 'webp', 'xls', 'xlsx', 'xml', 'zip'
])
for ext in file_extensions:
    listbox.insert(END, ext)

# Select/Deselect all checkboxes
buttons_frame = ctk.CTkFrame(app)
buttons_frame.pack(pady=5)
ctk.CTkButton(buttons_frame, text="Select All", command=select_all).pack(side="left", padx=10)
ctk.CTkButton(buttons_frame, text="Deselect All", command=deselect_all).pack(side="left", padx=10)

# Custom extension entry
ctk.CTkLabel(app, text="Or type custom file extensions (comma-separated):").pack(pady=(10, 0))
custom_extension_entry = ctk.CTkEntry(app, width=450)
custom_extension_entry.pack(pady=5)

# Organize button
ctk.CTkButton(app, text="Organize Files", command=start_organizing).pack(pady=20)

app.mainloop()
