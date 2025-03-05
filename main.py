# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui import FinanceTrackerUI
from db_manager import DatabaseManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    window = FinanceTrackerUI(db_manager)
    window.show()
    sys.exit(app.exec())
