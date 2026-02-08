import customtkinter as ctk
import psycopg2
from tkinter import messagebox

ctk.set_appearance_mode("light")

def load_farmers():
    conn = psycopg2.connect(
        host="localhost",
        database="agrisense_pro",
        user="postgres",
        password="kali"
    )
    cur = conn.cursor()
    cur.execute("SELECT farmer_id, name FROM farmers")
    data = cur.fetchall()
    conn.close()

    farmer_list = []
    for f in data:
        farmer_list.append(f"{f[0]} - {f[1]}")
    return farmer_list

def save_farm():
    try:
        selected = farmer_dropdown.get()
        farmer_id = selected.split(" - ")[0]

        conn = psycopg2.connect(
            host="localhost",
            database="agrisense_pro",
            user="postgres",
            password="kali"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO farms (farmer_id, crop_type, area_acres, soil_type) VALUES (%s,%s,%s,%s)",
            (farmer_id, crop_entry.get(), area_entry.get(), soil_entry.get())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Farm Added Successfully")

    except Exception as e:
        messagebox.showerror("Error",str(e))

app = ctk.CTk()
app.geometry("600x500")
app.title("AgriSense Pro - Farm Registration")

title = ctk.CTkLabel(app, text="Register Farm", font=("Arial", 26, "bold"))
title.pack(pady=20)

farmer_dropdown = ctk.CTkComboBox(app, values=load_farmers())
farmer_dropdown.pack(pady=10)

crop_entry = ctk.CTkEntry(app, placeholder_text="Crop Type")
crop_entry.pack(pady=10)

area_entry = ctk.CTkEntry(app, placeholder_text="Area (Acres)")
area_entry.pack(pady=10)

soil_entry = ctk.CTkEntry(app, placeholder_text="Soil Type")
soil_entry.pack(pady=10)

btn = ctk.CTkButton(app, text="Save Farm", command=save_farm)
btn.pack(pady=20)

app.mainloop()
