import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

class FinanceTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finans Takip Uygulaması")
        self.setGeometry(100, 100, 600, 400)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Hoş geldiniz! Harcamalarınızı takip edin.", self)
        layout.addWidget(self.label)

        self.button = QPushButton("Harcama Ekle", self)
        self.button.clicked.connect(self.add_expense)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_expense(self):
        self.label.setText("Yeni harcama eklendi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTracker()
    window.show()
    sys.exit(app.exec())
