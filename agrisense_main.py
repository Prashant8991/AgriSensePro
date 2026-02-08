import customtkinter as ctk
import subprocess
import sys
import os
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def open_farmer():
    subprocess.Popen([sys.executable, "farmer_register.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

def open_farm():
    subprocess.Popen([sys.executable, "farm_register.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

def open_detection():
    subprocess.Popen([sys.executable, "ml_disease_predict.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

def open_report():
    messagebox.showinfo("Info", "Report module not yet implemented")

def open_dashboard():
    subprocess.Popen([sys.executable, "dashboard.py"], cwd=os.path.dirname(os.path.abspath(__file__)))

app = ctk.CTk()
app.geometry("900x600")
app.title("AgriSense Pro")

# Sidebar
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(sidebar, text="AgriSense Pro", font=("Arial", 22, "bold"))
logo.pack(pady=25)

ctk.CTkButton(sidebar, text="Farmer Registration", command=open_farmer).pack(pady=10, padx=20)
ctk.CTkButton(sidebar, text="Farm Registration", command=open_farm).pack(pady=10, padx=20)
ctk.CTkButton(sidebar, text="Disease Detection", command=open_detection).pack(pady=10, padx=20)
ctk.CTkButton(sidebar, text="Reports", command=open_report).pack(pady=10, padx=20)
ctk.CTkButton(sidebar, text="Dashboard", command=open_dashboard).pack(pady=10, padx=20)

# Main Area
main_area = ctk.CTkFrame(app)
main_area.pack(fill="both", expand=True)

welcome = ctk.CTkLabel(
    main_area,
    text="Welcome",
    font=("Arial", 28, "bold")
)
welcome.pack(pady=60)

subtitle = ctk.CTkLabel(
    main_area,
    text="Select an option from the left menu.",
    font=("Arial", 16)
)
subtitle.pack()

app.mainloop()
