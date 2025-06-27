import sys
import json
import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QListWidget, QHBoxLayout, QInputDialog
)
from PySide6.QtCore import Qt

DATA_FILE = "habits.json"

class HabitTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Habit Tracker")
        self.setMinimumSize(400, 300)
        self.layout = QVBoxLayout(self)
        self.habits = {}
        self.load_data()
        self.build_ui()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.habits = json.load(f)
        else:
            self.habits = {}

    def build_ui(self):
        self.list = QListWidget()
        self.layout.addWidget(QLabel("Your Habits:"))
        self.layout.addWidget(self.list)
        self.refresh_list()

        btns = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add Habit")
        self.mark_btn = QPushButton("✅ Mark Today")
        btns.addWidget(self.add_btn)
        btns.addWidget(self.mark_btn)
        self.layout.addLayout(btns)

        self.add_btn.clicked.connect(self.add_habit)
        self.mark_btn.clicked.connect(self.mark_today)

    def refresh_list(self):
        self.list.clear()
        for habit, info in self.habits.items():
            self.list.addItem(f"{habit} – Streak: {info.get('streak', 0)}")

    def add_habit(self):
        name, ok = QInputDialog.getText(self, "New Habit", "Enter habit name:")
        if not ok or not name.strip():
            return
        name = name.strip()

        self.habits[name] = {
            "streak": 0,
            "last_mark": ""
        }
        self.save_data()
        self.refresh_list()

    def mark_today(self):
        current_item = self.list.currentItem()
        if not current_item:
            return

        habit_name = current_item.text().split(" – ")[0]
        habit = self.habits[habit_name]
        today = datetime.now().date().isoformat()
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()

        if habit["last_mark"] == today:
            return  # Already marked today

        if habit["last_mark"] == yesterday:
            habit["streak"] += 1
        else:
            habit["streak"] = 1

        habit["last_mark"] = today
        self.save_data()
        self.refresh_list()

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.habits, f, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HabitTracker()
    win.show()
    sys.exit(app.exec())
