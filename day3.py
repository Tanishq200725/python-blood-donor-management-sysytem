#day 3 analytics and refinement
import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import messagebox

from day2 import BloodDatabase, LoginScreen # Modular imports

class FinalMainApp(ctk.CTk):
    # ... (Referencing the full code provided in your source)
    
    def export_csv(self):
        """Feature added on Day 3 for data portability"""
        df = pd.read_sql_query("SELECT * FROM donors", self.db.conn)
        df.to_csv("donors_report.csv", index=False)
        messagebox.showinfo("Success", "Data exported to CSV")

    def show_graph(self):
        """Feature added on Day 3 for visual insights"""
        df = pd.read_sql_query("SELECT * FROM donors", self.db.conn)
        if not df.empty:
            plt.figure(figsize=(8, 4))
            sns.countplot(x="blood_group", data=df, palette="Reds")
            plt.title("Donor Distribution by Blood Group")
            plt.show()

# Final entry point logic
if __name__ == "__main__":
    login = LoginScreen()
    login.mainloop()