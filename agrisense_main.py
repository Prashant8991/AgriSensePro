import customtkinter as ctk
import subprocess

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def open_farmer():
    subprocess.Popen(["python", "farmer_register.py"])

def open_farm():
    subprocess.Popen(["python", "farm_register.py"])

def open_detection():
    subprocess.Popen(["python", "ml_disease_predict.py"])

def open_report():
    subprocess.Popen(["python", "view_report.py"])

def open_dashboard():
    subprocess.Popen(["python", "dashboard.py"])

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
