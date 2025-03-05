import sqlite3

DB_NAME = "data/finance.db"

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """create table for expenses"""
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_expense(self, amount, category, date, description):
        # ADD new expense
        query = "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)"    
        self.cursor.execute(query, (amount, category, date, description))
        self.conn.commit()

    def get_expenses(self):
        # GET all expenses
        query = "SELECT * FROM expenses ORDER BY date DESC"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def delete_expense(self, expense_id):
        """Belirtilen harcamayı siler"""
        query = "DELETE FROM expenses WHERE id = ?"
        self.cursor.execute(query, (expense_id,))
        self.conn.commit()   

    def close_connection(self):
        # CLOSE connect
        self.conn.close()
