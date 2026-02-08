import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="agrisense_pro",
        user="postgres",
        password="kali"
    )

    cur = conn.cursor()

    cur.execute("SELECT * FROM farmers;")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)
