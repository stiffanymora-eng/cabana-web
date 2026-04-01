from flask import Flask, render_template, request
import os
import psycopg2

app = Flask(__name__)

# 🔗 conexión a PostgreSQL desde Render
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

NUMERO_WHATSAPP = "50689872394"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    mensaje = ""
    link_whatsapp = ""

    conn = get_db_connection()
    cur = conn.cursor()

    # Crear tabla si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            fecha TEXT
        )
    """)
    conn.commit()

    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha = request.form["fecha"]

        # Guardar en BD
        cur.execute(
            "INSERT INTO reservas (nombre, fecha) VALUES (%s, %s)",
            (nombre, fecha)
        )
        conn.commit()

        mensaje = "Reserva guardada correctamente"

        link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text=Hola soy {nombre} y quiero confirmar mi reserva para {fecha}"

    cur.close()
    conn.close()

    return render_template(
        "reserva.html",
        mensaje=mensaje,
        link_whatsapp=link_whatsapp
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
