import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import numpy as np
import tensorflow as tf
import os
import psycopg2

ctk.set_appearance_mode("light")

# Load trained model
model = tf.keras.models.load_model("plant_disease_model.h5")

# Dataset path (for class names)
dataset_path = r"C:\Users\Prabhat Singh\Downloads\archive\PlantVillage\PlantVillage"

class_names = sorted([
    d for d in os.listdir(dataset_path)
    if os.path.isdir(os.path.join(dataset_path, d))
])

selected_path = ""

def upload_image():
    global selected_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if file_path:
        selected_path = file_path
        img_preview = ctk.CTkImage(Image.open(file_path), size=(300,200))
        image_label.configure(image=img_preview, text="")
        image_label.image = img_preview

def predict_image():
    global selected_path

    if not selected_path:
        result_label.configure(text="No image selected")
        return

    img = Image.open(selected_path).resize((224,224))
    arr = np.array(img)/255.0
    arr = np.expand_dims(arr, axis=0)

    preds = model.predict(arr)
    idx = np.argmax(preds)
    confidence = float(round(preds[0][idx]*100,2))
    disease_name = class_names[idx]

    result_label.configure(text=f"Disease: {disease_name} ({confidence}%)")

    # DATABASE CONNECTION
    conn = psycopg2.connect(
        host="localhost",
        database="agrisense_pro",
        user="postgres",
        password="kali"
    )
    cur = conn.cursor()

    # Get disease_id
    cur.execute("SELECT disease_id FROM diseases WHERE disease_name=%s", (disease_name,))
    result = cur.fetchone()

    if result is None:
        cur.execute("""
            INSERT INTO diseases (disease_name, treatment, medicine, dosage)
            VALUES (%s,'Auto detected','Consult expert','N/A')
            RETURNING disease_id
        """, (disease_name,))
        disease_id = cur.fetchone()[0]
    else:
        disease_id = result[0]

    # Save detection record
    cur.execute(
        "INSERT INTO crop_images (farm_id, disease_id, confidence_score, image_path) VALUES (%s,%s,%s,%s)",
        (1, disease_id, confidence, selected_path)
    )

    # Fetch treatment info
    cur.execute("""
        SELECT treatment, medicine, dosage
        FROM diseases
        WHERE disease_id=%s
    """, (disease_id,))

    info = cur.fetchone()

    if info:
        treatment, medicine, dosage = info
        treatment_label.configure(
            text=f"Treatment: {treatment}\nMedicine: {medicine}\nDosage: {dosage}"
        )

    conn.commit()
    conn.close()

app = ctk.CTk()
app.geometry("600x500")
app.title("AgriSense Pro - Disease Detection")

title = ctk.CTkLabel(app, text="Crop Disease Detection", font=("Arial", 22, "bold"))
title.pack(pady=15)

image_label = ctk.CTkLabel(app, text="No Image Selected")
image_label.pack(pady=10)

upload_btn = ctk.CTkButton(app, text="Browse Image", command=upload_image)
upload_btn.pack(pady=10)

predict_btn = ctk.CTkButton(app, text="Predict Disease", command=predict_image)
predict_btn.pack(pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)

treatment_label = ctk.CTkLabel(app, text="", justify="left")
treatment_label.pack(pady=10)

app.mainloop()
