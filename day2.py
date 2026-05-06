#day2 functionality and security login
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
# (Assuming BloodDatabase class from Day 1 is present)

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")
        
        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=10)
        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=10)
        ctk.CTkButton(self, text="Login", command=self.check_login).pack()

    def check_login(self):
        if self.username.get() == "admin" and self.password.get() == "1234":
            self.destroy()
            # In a real scenario, you'd launch MainApp here
            print("Login Successful")
        else:
            messagebox.showerror("Error", "Invalid Credentials")

# Logic added to MainApp for Day 2:
# - add_donor()
# - delete_donor()
# - set_today()