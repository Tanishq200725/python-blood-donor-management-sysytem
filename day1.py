# day 1 consisting of foundation database and gui(tkinter)
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3

# --- DATABASE MANAGER ---
class BloodDatabase:
    def __init__(self, db_name="blood_donors.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS donors(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, address TEXT, phone TEXT, 
                age INTEGER, blood_group TEXT, health TEXT, date TEXT
            )
        """)
        self.conn.commit()

    def run_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.fetchall()

# --- INITIAL APP STRUCTURE ---
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = BloodDatabase()
        self.title("Blood Donor System - Day 1")
        self.geometry("900x500")
        
        # Simple layout frames
        self.left_frame = ctk.CTkFrame(self, width=250)
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        # Basic Table setup
        cols = ("ID", "Name", "Blood", "Phone")
        self.tree = ttk.Treeview(self.right_frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()