import customtkinter as ctk
import psycopg2
from tkinter import messagebox

ctk.set_appearance_mode("light")

def load_farms():
    conn = psycopg2.connect(
        host="localhost",
        database="agrisense_pro",
        user="postgres",
        password="kali"
    )
    cur = conn.cursor()
    cur.execute("SELECT farm_id, crop_type FROM farms")
    data = cur.fetchall()
    conn.close()

    farm_list = []
    for f in data:
        farm_list.append(f"{f[0]} - {f[1]}")
    return farm_list

def load_diseases():
    conn = psycopg2.connect(
        host="localhost",
        database="agrisense_pro",
        user="postgres",
        password="kali"
    )
    cur = conn.cursor()
    cur.execute("SELECT disease_id, disease_name FROM diseases")
    data = cur.fetchall()
    conn.close()

    disease_list = []
    for d in data:
        disease_list.append(f"{d[0]} - {d[1]}")
    return disease_list

def save_detection():
    try:
        farm_id = farm_dropdown.get().split(" - ")[0]
        disease_id = disease_dropdown.get().split(" - ")[0]

        conn = psycopg2.connect(
            host="localhost",
            database="agrisense_pro",
            user="postgres",
            password="kali"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO crop_images (farm_id, disease_id, confidence_score, image_path) VALUES (%s,%s,%s,%s)",
            (farm_id, disease_id, confidence_entry.get(), "sample_leaf.jpg")
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Detection Saved")

    except Exception as e:
        messagebox.showerror("Error", str(e))

app = ctk.CTk()
app.geometry("600x500")
app.title("AgriSense Pro - Detection Entry")

title = ctk.CTkLabel(app, text="Crop Disease Detection Entry", font=("Arial", 22, "bold"))
title.pack(pady=20)

farm_dropdown = ctk.CTkComboBox(app, values=load_farms())
farm_dropdown.pack(pady=10)

disease_dropdown = ctk.CTkComboBox(app, values=load_diseases())
disease_dropdown.pack(pady=10)

confidence_entry = ctk.CTkEntry(app, placeholder_text="Confidence %")
confidence_entry.pack(pady=10)

btn = ctk.CTkButton(app, text="Save Detection", command=save_detection)
btn.pack(pady=20)

app.mainloop()
