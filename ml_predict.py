import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

ctk.set_appearance_mode("light")

# Load pretrained model (downloads automatically first time)
model = MobileNetV2(weights="imagenet")

selected_path = ""

def upload_image():
    global selected_path

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
    )

    if file_path:
        selected_path = file_path
        img_preview = ctk.CTkImage(Image.open(file_path), size=(300,200))
        image_label.configure(image=img_preview, text="")
        image_label.image = img_preview

def predict_image():
    if selected_path == "":
        result_label.configure(text="No image selected")
        return

    img = Image.open(selected_path).resize((224,224))
    arr = np.array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    preds = model.predict(arr)
    decoded = decode_predictions(preds, top=1)[0][0]

    label = decoded[1]
    confidence = round(decoded[2]*100,2)

    result_label.configure(text=f"Prediction: {label} ({confidence}%)")

app = ctk.CTk()
app.geometry("600x450")
app.title("AgriSense Pro - ML Prediction")

title = ctk.CTkLabel(app, text="Leaf Image Prediction", font=("Arial", 22, "bold"))
title.pack(pady=15)

image_label = ctk.CTkLabel(app, text="No Image Selected")
image_label.pack(pady=10)

upload_btn = ctk.CTkButton(app, text="Browse Image", command=upload_image)
upload_btn.pack(pady=10)

predict_btn = ctk.CTkButton(app, text="Predict", command=predict_image)
predict_btn.pack(pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=20)

app.mainloop()
