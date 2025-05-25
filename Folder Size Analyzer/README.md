# 📁 Folder Size Analyzer

This Python GUI application analyzes and visualizes the size of all subfolders in a selected directory. It uses a bar chart for easy comparison and allows exporting results to an Excel file.

---

## 🚀 Features

* Select any folder to analyze its subdirectories.
* Display a horizontal bar chart of folder sizes (in MB).
* Supports right-to-left (RTL) languages including Persian/Arabic.
* Export results to Excel (`.xlsx`) format.
* Shows a live timer during analysis.
* Automatically disables the "Analyze" button while processing.
* Opens the Excel file after saving (on Windows).

---

## 🛠️ Installation

1. **Clone the repository**

```bash
https://github.com/yourusername/folder-size-analyzer.git
cd folder-size-analyzer
```

2. **Create and activate a virtual environment** (Windows example):

```bash
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

If you face issues with `numpy`, install it using:

```bash
pip install numpy matplotlib openpyxl customtkinter arabic_reshaper python-bidi
```

---

## 🖼️ Fonts for RTL Support

To render Persian/Arabic folder names correctly in the chart:

* Install a font like `Vazirmatn` or `B Nazanin`.
* Make sure it is recognized by your system and available to Matplotlib.

> **Windows**: Copy `.ttf` file into `C:\Windows\Fonts` and restart.

If the font is not found, fallback to `DejaVu Sans` will be used, which may not display RTL scripts correctly.

---

## 🧪 How to Use

1. Run the app:

```bash
python FolderSizeAnalyzer.py
```

2. Click **"Select Folder and Analyze"**.
3. Wait while analysis and chart rendering occurs.
4. Click **"Export to Excel"** to save results.
5. The Excel file opens automatically (if on Windows).

---

## 🐛 Troubleshooting

* If you get a `PermissionError` when saving Excel, close the file if it's already open.
* If folder names are not readable, check if proper RTL font is installed and supported.
* If GUI freezes during long analysis, ensure you're using Python 3.9+ and that threading is working correctly.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Created by [Parvaneh Sharghi](https://github.com/parvaneh-sharghi). Contributions are welcome!
