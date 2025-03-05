import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from db_manager import DatabaseManager
from datetime import datetime

class FinanceTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finans Takip Uygulaması")
        self.setGeometry(100, 100, 600, 500)
        self.db = DatabaseManager() # database connection

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Giriş alanları
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Harcama Tutarı")
        layout.addWidget(self.amount_input)

        self.category_input = QComboBox(self)
        self.category_input.addItems(["Gıda", "Ulaşım", "Eğlence", "Fatura", "Diğer"])
        layout.addWidget(self.category_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Açıklama (Opsiyonel)")
        layout.addWidget(self.description_input)

        # Buttons
        btn_layout = QHBoxLayout()

        self.add_button = QPushButton("Harcama Ekle", self)
        self.add_button.clicked.connect(self.add_expense)
        btn_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Sil", self)
        self.delete_button.clicked.connect(self.delete_expense)
        btn_layout.addWidget(self.delete_button)

        layout.addLayout(btn_layout)

        # Table of Expense List
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tarih", "Kategori", "Tutar", "Açıklama"])
        self.table.cellClicked.connect(self.select_expense) # Table click
        layout.addWidget(self.table)

        self.load_expenses() # Load expenses to table
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_expense(self):
        amount = self.amount_input.text()
        category = self.category_input.currentText()
        description = self.description_input.toPlainText() 
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        if amount:
            self.db.add_expense(float(amount), category, date, description)
            self.amount_input.clear()
            self.description_input.clear()
            self.load_expenses() # Update list        

    def load_expenses(self):
        expenses = self.db.get_expenses()
        self.table.setRowCount(len(expenses))

        for row, expense in enumerate(expenses):
            for col, value in enumerate(expense): # Add whole data 
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def select_expense(self, row, col): 
        # Get enter area selected expense 
        self.selected_expense_id = int(self.table.item(row, 0).text())
        self.amount_input.setText(self.table.item(row, 3).text())
        self.category_input.setCurrentText(self.table.item(row, 2).text())            
        self.description_input.setText(self.table.item(row, 4).text())
                    
    def delete_expense(self):
        if hasattr(self, 'selected_expense_id'):
            self.db.delete_expense(self.selected_expense_id)
            self.amount_input.clear()
            self.description_input.clear()                
            self.load_expenses()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTracker()
    window.show()
    sys.exit(app.exec())           