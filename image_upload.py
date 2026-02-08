import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import psycopg2

ctk.set_appearance_mode("light")

selected_path = ""

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
    return [f"{f[0]} - {f[1]}" for f in data]

def upload_image():
    global selected_path

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
    )

    if file_path:
        selected_path = file_path
        img = ctk.CTkImage(Image.open(file_path), size=(300,200))
        image_label.configure(image=img, text="")
        image_label.image = img

def save_image_record():
    try:
        farm_id = farm_dropdown.get().split(" - ")[0]

        conn = psycopg2.connect(
            host="localhost",
            database="agrisense_pro",
            user="postgres",
            password="kali"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO crop_images (farm_id, image_path, confidence_score) VALUES (%s,%s,%s)",
            (farm_id, selected_path, 0)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Image Path Saved")

    except Exception as e:
        messagebox.showerror("Error", str(e))

app = ctk.CTk()
app.geometry("650x500")
app.title("AgriSense Pro - Upload Leaf Image")

title = ctk.CTkLabel(app, text="Upload Crop Leaf Image", font=("Arial", 22, "bold"))
title.pack(pady=10)

farm_dropdown = ctk.CTkComboBox(app, values=load_farms())
farm_dropdown.pack(pady=10)

image_label = ctk.CTkLabel(app, text="No Image Selected")
image_label.pack(pady=10)

upload_btn = ctk.CTkButton(app, text="Browse Image", command=upload_image)
upload_btn.pack(pady=10)

save_btn = ctk.CTkButton(app, text="Save Image Record", command=save_image_record)
save_btn.pack(pady=10)

app.mainloop()
