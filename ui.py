# ui.py
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from datetime import datetime

class FinanceTrackerUI(QMainWindow):
    def __init__(self, backend):
        super().__init__()

        self.backend = backend  # Veritabanı yönetimi backend dosyasından gelir

        self.setWindowTitle("Finans Takip Uygulaması")
        self.setGeometry(100, 100, 700, 600)

        self.initUI()
        self.load_styles()

    def initUI(self):
        layout = QVBoxLayout()

        self.header_label = QLabel("💰 Finans Takip Uygulaması", self)
        layout.addWidget(self.header_label)

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Harcama Tutarı")
        layout.addWidget(self.amount_input)

        self.category_input = QComboBox(self)
        self.category_input.addItems(["Gıda", "Ulaşım", "Eğlence", "Fatura", "Diğer"])
        layout.addWidget(self.category_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Açıklama (Opsiyonel)")
        layout.addWidget(self.description_input)

        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("➕ Harcama Ekle", self)
        self.add_button.clicked.connect(self.add_expense)
        btn_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("🗑 Sil", self)
        self.delete_button.clicked.connect(self.delete_expense)
        btn_layout.addWidget(self.delete_button)

        layout.addLayout(btn_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tarih", "Kategori", "Tutar", "Açıklama"])
        self.table.cellClicked.connect(self.select_expense)
        layout.addWidget(self.table)

        self.load_expenses()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_styles(self):
        """QSS dosyasını yükleyerek stilleri uygular"""
        with open("styles.qss", "r") as file:
            self.setStyleSheet(file.read())

    def add_expense(self):
        amount = self.amount_input.text()
        category = self.category_input.currentText()
        description = self.description_input.toPlainText()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        if amount:
            self.backend.add_expense(float(amount), category, date, description)
            self.amount_input.clear()
            self.description_input.clear()
            self.load_expenses()

    def load_expenses(self):
        expenses = self.backend.get_expenses()
        self.table.setRowCount(len(expenses))

        for row, expense in enumerate(expenses):
            for col, value in enumerate(expense):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def select_expense(self, row, col):
        self.selected_expense_id = int(self.table.item(row, 0).text())
        self.amount_input.setText(self.table.item(row, 3).text())
        self.category_input.setCurrentText(self.table.item(row, 2).text())
        self.description_input.setText(self.table.item(row, 4).text())

    def delete_expense(self):
        if hasattr(self, 'selected_expense_id'):
            self.backend.delete_expense(self.selected_expense_id)
            self.amount_input.clear()
            self.description_input.clear()
            self.load_expenses()
