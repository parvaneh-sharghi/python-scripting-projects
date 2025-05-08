import os  # Used for interacting with the operating system (checking paths, listing files)
import shutil  # Provides file operations like move, copy, etc.
import customtkinter as ctk  # Provides modern-looking themed widgets for the GUI
from tkinter import filedialog, messagebox, Listbox, MULTIPLE, END  # Standard tkinter widgets used with customtkinter

# Set appearance and theme of the GUI
ctk.set_appearance_mode("System")  # Use system theme (can be changed to "Dark" or "Light")
ctk.set_default_color_theme("blue")  # Use blue as the default theme color

# Function to organize files based on their extensions
def organize_files_by_type(source_folder, target_folder_name, extensions):
    if not os.path.exists(source_folder):  # Check if the source folder exists
        messagebox.showerror("Error", f"Source folder '{source_folder}' does not exist.")
        return

    # Clean and prepare a set of extensions
    extensions = {ext.strip().lower().strip('.') for ext in extensions.split(',') if ext.strip()}
    if not extensions:
        messagebox.showwarning("Warning", "No valid file extensions provided.")
        return

    # Create target folder if it doesn't exist
    target_folder = os.path.join(source_folder, target_folder_name)
    os.makedirs(target_folder, exist_ok=True)

    moved_files = 0  # Count how many files are moved
    for filename in os.listdir(source_folder):  # Loop over all files in source folder
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path):  # Process only files
            _, extension = os.path.splitext(filename)
            extension = extension.lower().strip('.')
            if extension in extensions:
                shutil.move(file_path, os.path.join(target_folder, filename))  # Move matching file
                moved_files += 1

    # Show result message
    if moved_files == 0:
        messagebox.showinfo("Result", "No matching files found to move.")
    else:
        messagebox.showinfo("Result", f"Successfully moved {moved_files} file(s) to '{target_folder_name}'.")

# Opens folder dialog and sets the selected path in entry field
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_entry.delete(0, ctk.END)
        folder_entry.insert(0, folder_selected)

# Select all items in the listbox
def select_all():
    listbox.select_set(0, END)

# Deselect all items in the listbox
def deselect_all():
    listbox.selection_clear(0, END)

# Called when the user clicks the Organize button
def start_organizing():
    source = folder_entry.get().strip()  # Get folder to search
    target = target_entry.get().strip()  # Get target folder name
    selected_items = listbox.curselection()  # Get selected extensions
    selected_extensions = [listbox.get(i) for i in selected_items]
    custom_extensions = custom_extension_entry.get().strip()  # Get custom typed extensions

    if not source or not target:
        messagebox.showwarning("Warning", "Please fill in both folder fields.")
        return

    # Combine both listbox and custom extensions
    all_extensions = selected_extensions[:]
    if custom_extensions:
        all_extensions += [ext.strip() for ext in custom_extensions.split(',') if ext.strip()]

    if not all_extensions:
        messagebox.showwarning("Warning", "Please select or enter at least one file extension.")
        return

    # Call main function
    extensions_string = ','.join(all_extensions)
    organize_files_by_type(source, target, extensions_string)

# GUI application window
app = ctk.CTk()
app.title("Custom File Organizer")
app.geometry("560x650")  # Set fixed window size

# Folder selection area
ctk.CTkLabel(app, text="Select folder to search:").pack(pady=(10, 0))
folder_frame = ctk.CTkFrame(app)
folder_frame.pack(pady=5)
folder_entry = ctk.CTkEntry(folder_frame, width=400)
folder_entry.pack(side="left", padx=5)
ctk.CTkButton(folder_frame, text="Browse", command=browse_folder).pack(side="left")

# Entry for target folder name
ctk.CTkLabel(app, text="Folder name to move files into:").pack(pady=(10, 0))
target_entry = ctk.CTkEntry(app, width=450)
target_entry.pack(pady=5)

# File types list
ctk.CTkLabel(app, text="Select one or more file types:").pack(pady=(10, 0))
listbox = Listbox(app, selectmode=MULTIPLE, width=60, height=12)
listbox.pack(pady=5)
file_extensions = sorted([
    '7z', 'aac', 'apk', 'avi', 'bmp', 'css', 'csv', 'doc', 'docx', 'exe', 'flv', 'gif', 'gz', 'html', 'ico', 'jpeg', 'jpg',
    'js', 'json', 'mkv', 'mov', 'mp3', 'mp4', 'msi', 'odt', 'ogg', 'pdf', 'png', 'ppt', 'pptx', 'py', 'rar', 'rtf',
    'tar', 'tsv', 'tiff', 'txt', 'wav', 'webp', 'xls', 'xlsx', 'xml', 'zip'
])
for ext in file_extensions:
    listbox.insert(END, ext)  # Add each extension to listbox

# Buttons for select/deselect all
buttons_frame = ctk.CTkFrame(app)
buttons_frame.pack(pady=5)
ctk.CTkButton(buttons_frame, text="Select All", command=select_all).pack(side="left", padx=10)
ctk.CTkButton(buttons_frame, text="Deselect All", command=deselect_all).pack(side="left", padx=10)

# Custom extension field
ctk.CTkLabel(app, text="Or type custom file extensions (comma-separated):").pack(pady=(10, 0))
custom_extension_entry = ctk.CTkEntry(app, width=450)
custom_extension_entry.pack(pady=5)

# Final action button
ctk.CTkButton(app, text="Organize Files", command=start_organizing).pack(pady=20)

# Start the app loop
app.mainloop()