import customtkinter as ctk
from PIL import Image
import psycopg2

ctk.set_appearance_mode("light")

from tkinter import messagebox

def save_farmer():
    if name_entry.get()=="" or aadhaar_entry.get()=="" or village_entry.get()=="" or phone_entry.get()=="":
        messagebox.showerror("Error","Please fill all fields")
        return

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="agrisense_pro",
            user="postgres",
            password="kali"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO farmers (name, aadhaar, village, phone) VALUES (%s,%s,%s,%s)",
            (name_entry.get(), aadhaar_entry.get(), village_entry.get(), phone_entry.get())
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success","Farmer Registered Successfully")

        name_entry.delete(0,'end')
        aadhaar_entry.delete(0,'end')
        village_entry.delete(0,'end')
        phone_entry.delete(0,'end')

    except Exception as e:
        messagebox.showwarning("Database Unavailable", f"Database not connected. Data shown in UI only.\n\nFarmer: {name_entry.get()}\nAadhaar: {aadhaar_entry.get()}\nVillage: {village_entry.get()}\nPhone: {phone_entry.get()}")

app = ctk.CTk()
app.geometry("1100x650")
app.title("AgriSense Pro")

# Background Image
try:
    bg_image = ctk.CTkImage(Image.open("farm_bg.jpg"), size=(1100,650))
    bg_label = ctk.CTkLabel(app, image=bg_image, text="")
    bg_label.place(x=0, y=0)
except:
    bg_label = ctk.CTkLabel(app, text="", fg_color="#E8F5E9")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Sidebar
sidebar = ctk.CTkFrame(app, width=220, fg_color="#1B5E20")
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(sidebar, text="🌱 AgriSense Pro", text_color="white",
                    font=("Segoe UI", 22, "bold"))
logo.pack(pady=40)

# Glass Style Card
card = ctk.CTkFrame(
    app,
    width=400,
    height=480,
    fg_color="#FAFFFB",
    corner_radius=30,
    border_width=2,
    border_color="#C8E6C9"
)
card.place(relx=0.62, rely=0.5, anchor="center")

title = ctk.CTkLabel(card, text="Farmer Registration",
                     font=("Segoe UI", 26, "bold"))
title.pack(pady=20)

# Name Field
name_frame = ctk.CTkFrame(card, fg_color="transparent")
name_frame.pack(pady=8)

ctk.CTkLabel(name_frame, text="👤").pack(side="left", padx=5)

name_entry = ctk.CTkEntry(
    name_frame,
    width=280,
    height=45,
    fg_color="#F1F8F4",
    border_color="#A5D6A7",
    corner_radius=12,
    placeholder_text="Farmer Name"
)
name_entry.pack(side="left")

# Aadhaar Field
aadhaar_frame = ctk.CTkFrame(card, fg_color="transparent")
aadhaar_frame.pack(pady=8)

ctk.CTkLabel(aadhaar_frame, text="🪪").pack(side="left", padx=5)

aadhaar_entry = ctk.CTkEntry(
    aadhaar_frame,
    width=280,
    height=45,
    fg_color="#F1F8F4",
    border_color="#A5D6A7",
    corner_radius=12,
    placeholder_text="Aadhaar Number"
)
aadhaar_entry.pack(side="left")

# Village Field
village_frame = ctk.CTkFrame(card, fg_color="transparent")
village_frame.pack(pady=8)

ctk.CTkLabel(village_frame, text="🌾").pack(side="left", padx=5)

village_entry = ctk.CTkEntry(
    village_frame,
    width=280,
    height=45,
    fg_color="#F1F8F4",
    border_color="#A5D6A7",
    corner_radius=12,
    placeholder_text="Village"
)
village_entry.pack(side="left")

# Phone Field
phone_frame = ctk.CTkFrame(card, fg_color="transparent")
phone_frame.pack(pady=8)

ctk.CTkLabel(phone_frame, text="📞").pack(side="left", padx=5)

phone_entry = ctk.CTkEntry(
    phone_frame,
    width=280,
    height=45,
    fg_color="#F1F8F4",
    border_color="#A5D6A7",
    corner_radius=12,
    placeholder_text="Phone"
)
phone_entry.pack(side="left")

# Button
btn = ctk.CTkButton(
    card,
    text="Register Farmer",
    fg_color="#2E7D32",
    hover_color="#66BB6A",
    corner_radius=25,
    height=50,
    width=240,
    command=save_farmer
)
btn.pack(pady=25)

app.mainloop()
