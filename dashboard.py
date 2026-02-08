import customtkinter as ctk
import psycopg2

ctk.set_appearance_mode("light")

def load_stats():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="agrisense_pro",
            user="postgres",
            password="kali"
        )
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM crop_images;")
        total = cur.fetchone()[0]

        cur.execute("""
            SELECT COUNT(*) FROM crop_images
            WHERE DATE(detected_at) = CURRENT_DATE;
        """)
        today = cur.fetchone()[0]

        cur.execute("""
            SELECT d.disease_name, COUNT(*) AS c
            FROM crop_images ci
            JOIN diseases d ON ci.disease_id = d.disease_id
            GROUP BY d.disease_name
            ORDER BY c DESC
            LIMIT 1;
        """)
        row = cur.fetchone()
        common = row[0] if row else "N/A"

        cur.execute("""
            SELECT d.disease_name
            FROM crop_images ci
            JOIN diseases d ON ci.disease_id = d.disease_id
            ORDER BY ci.detected_at DESC
            LIMIT 1;
        """)
        row = cur.fetchone()
        last = row[0] if row else "N/A"

        conn.close()

        total_label.configure(text=f"Total Detections: {total}")
        today_label.configure(text=f"Detections Today: {today}")
        common_label.configure(text=f"Most Common Disease: {common}")
        last_label.configure(text=f"Last Detected Disease: {last}")
    except:
        total_label.configure(text=f"Total Detections: 0 (DB not connected)")
        today_label.configure(text=f"Detections Today: 0")
        common_label.configure(text=f"Most Common Disease: N/A")
        last_label.configure(text=f"Last Detected Disease: N/A")

app = ctk.CTk()
app.geometry("500x350")
app.title("AgriSense Pro - Dashboard")

title = ctk.CTkLabel(app, text="Analytics Dashboard", font=("Arial", 22, "bold"))
title.pack(pady=15)

total_label = ctk.CTkLabel(app, text="")
total_label.pack(pady=5)

today_label = ctk.CTkLabel(app, text="")
today_label.pack(pady=5)

common_label = ctk.CTkLabel(app, text="")
common_label.pack(pady=5)

last_label = ctk.CTkLabel(app, text="")
last_label.pack(pady=5)

refresh_btn = ctk.CTkButton(app, text="Refresh Stats", command=load_stats)
refresh_btn.pack(pady=15)

load_stats()

app.mainloop()
