import sys
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QListWidget, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PIL import Image

DATA_FILE = "habits.json"

class HabitTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Habit Tracker")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.load_data()
        self.build_ui()
        
    def load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                self.data = json.load(f)
        except:
            self.data = {"habits": {}}
            
    def build_ui(self):
        self.list = QListWidget()
        self.layout.addWidget(self.list)
        for name, habit in self.data["habits"].items():
            self.list.addItem(f"{name} – streak: {habit.get('streak',0)}")
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add Habit")
        self.btn_add.clicked.connect(self.add_habit)
        btn_layout.addWidget(self.btn_add)
        self.btn_mark = QPushButton("Mark Today")
        self.btn_mark.clicked.connect(self.mark_today)
        btn_layout.addWidget(self.btn_mark)
        self.layout.addLayout(btn_layout)
        
    def add_habit(self):
        name, _ = QFileDialog.getText(self, "Habit Name", "Enter new habit name:")
        if not name: return
        icon, _ = QFileDialog.getOpenFileName(self, "Select Icon", filter="Images (*.png *.jpg)")
        if not icon: return
        self.data["habits"][name] = {
            "icon": icon,
            "streak": 0,
            "last_mark": ""
        }
        self.list.addItem(f"{name} – streak: 0")
        self.save()
        
    def mark_today(self):
        item = self.list.currentItem()
        if not item:
            return
        name = item.text().split(" – ")[0]
        h = self.data["habits"][name]
        today = datetime.now().date().isoformat()
        if h["last_mark"] == today:
            return  # Already marked
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        if h["last_mark"] == yesterday:
            h["streak"] += 1
        else:
            h["streak"] = 1
        h["last_mark"] = today
        self.list.currentItem().setText(f"{name} – streak: {h['streak']}")
        self.save()
        
    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HabitTracker()
    win.show()
    sys.exit(app.exec())
