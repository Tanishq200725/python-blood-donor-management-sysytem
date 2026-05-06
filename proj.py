import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --- DATABASE MANAGER CLASS ---
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

# --- LOGIN SCREEN CLASS ---
class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Blood Donation Login")
        self.geometry("300x250")

        ctk.CTkLabel(self, text="Login System", font=("Arial", 20)).pack(pady=10)
        
        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=5)
        
        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=5)
        
        ctk.CTkButton(self, text="Login", command=self.check_login).pack(pady=10)

    def check_login(self):
        if self.username.get() == "admin" and self.password.get() == "1234":
            self.withdraw()  # Hide login window
            MainApp()        # Open Main Application
        else:
            messagebox.showerror("Error", "Invalid username/Password")

# --- MAIN APPLICATION CLASS ---
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = BloodDatabase()
        
        self.title("Blood Donor Management System")
        self.geometry("1100x600")
        
        self.create_widgets()
        self.show_data()

    def create_widgets(self):
        # Layout Frames
        self.left_frame = ctk.CTkFrame(self, width=300, fg_color="#b71c1c")
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        # --- Left Side: Input Form ---
        ctk.CTkLabel(self.left_frame, text="Donor Form", text_color="white", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.name_entry = self.make_entry(self.left_frame, "Name")
        self.address_entry = self.make_entry(self.left_frame, "Address")
        self.phone_entry = self.make_entry(self.left_frame, "Phone")
        self.age_entry = self.make_entry(self.left_frame, "Age")
        
        self.blood_var = ctk.StringVar(value="A+")
        ctk.CTkOptionMenu(self.left_frame, variable=self.blood_var,
                          values=["A+","A-","B+","B-","AB+","AB-","O+","O-"]).pack(pady=5)
        
        self.health_entry = self.make_entry(self.left_frame, "Health Issues")
        self.date_entry = self.make_entry(self.left_frame, "Date")

        # Buttons
        ctk.CTkButton(self.left_frame, text="Today", command=self.set_today).pack(pady=3)
        ctk.CTkButton(self.left_frame, text="Add", command=self.add_donor).pack(pady=3)
        ctk.CTkButton(self.left_frame, text="Update", command=self.update_donor).pack(pady=3)
        ctk.CTkButton(self.left_frame, text="Delete", command=self.delete_donor).pack(pady=3)
        ctk.CTkButton(self.left_frame, text="Export CSV", command=self.export_csv).pack(pady=3)
        ctk.CTkButton(self.left_frame, text="Show Graph", command=self.show_graph).pack(pady=3)

        # --- Right Side: Search & Table ---
        self.search_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Search...")
        self.search_entry.pack(pady=10)
        ctk.CTkButton(self.right_frame, text="Search", command=self.search_donor).pack(pady=5)

        cols = ("ID", "Name", "Address", "Phone", "Age", "Blood", "Health", "Date")
        self.tree = ttk.Treeview(self.right_frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def make_entry(self, parent, placeholder):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.pack(pady=5)
        return entry

    # --- LOGIC METHODS ---
    def set_today(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def show_data(self, records=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        data = records if records else self.db.run_query("SELECT * FROM donors")
        for row in data:
            self.tree.insert("", "end", values=row)

    def add_donor(self):
        try:
            age = int(self.age_entry.get())
            if age < 18 or len(self.phone_entry.get()) != 10:
                raise ValueError("Check Age (18+) or Phone (10 digits)")
            
            query = "INSERT INTO donors(name,address,phone,age,blood_group,health,date) VALUES(?,?,?,?,?,?,?)"
            params = (self.name_entry.get(), self.address_entry.get(), self.phone_entry.get(), 
                      age, self.blood_var.get(), self.health_entry.get(), self.date_entry.get())
            
            self.db.run_query(query, params)
            self.show_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_donor(self):
        selected = self.tree.focus()
        if not selected: return
        donor_id = self.tree.item(selected)['values'][0]
        
        query = "UPDATE donors SET name=?, address=?, phone=?, age=?, blood_group=?, health=?, date=? WHERE id=?"
        params = (self.name_entry.get(), self.address_entry.get(), self.phone_entry.get(), 
                  self.age_entry.get(), self.blood_var.get(), self.health_entry.get(), 
                  self.date_entry.get(), donor_id)
        
        self.db.run_query(query, params)
        self.show_data()

    def delete_donor(self):
        selected = self.tree.focus()
        if not selected: return
        donor_id = self.tree.item(selected)['values'][0]
        self.db.run_query("DELETE FROM donors WHERE id=?", (donor_id,))
        self.show_data()

    def search_donor(self):
        query = f"%{self.search_entry.get().strip()}%"
        results = self.db.run_query("SELECT * FROM donors WHERE name LIKE ? OR blood_group LIKE ?", (query, query))
        self.show_data(results)

    def export_csv(self):
        df = pd.read_sql_query("SELECT * FROM donors", self.db.conn)
        df.to_csv("donors.csv", index=False)
        messagebox.showinfo("Exported", "Saved as donors.csv")

    def show_graph(self):
        df = pd.read_sql_query("SELECT * FROM donors", self.db.conn)
        if df.empty: return
        
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        df['blood_group'].value_counts().plot.pie(autopct='%1.1f%%')
        plt.subplot(1, 2, 2)
        sns.countplot(x="blood_group", data=df)
        plt.tight_layout()
        plt.show()
    def show_ds(self):
        print({self.name_entry},{self.phone_entry},{self.health_entry},{self.age_entry})
    a= show_data()
    print(a)
# --- ENTRY POINT ---
if __name__ == "__main__":
    login_app = LoginScreen()
    login_app.mainloop()