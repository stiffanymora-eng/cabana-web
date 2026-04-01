from flask import Flask, render_template, request
import os
import psycopg2

app = Flask(__name__)

NUMERO_WHATSAPP = "50689872394"

# 🔗 Obtener URL de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL")

# 🔧 Arreglar URL si viene como postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 🔌 Conexión segura
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn


# 🏠 Inicio
@app.route("/")
def home():
    return render_template("index.html")


# 📅 Reserva
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

        # Guardar reserva
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


# 👀 Admin (ver reservas)
@app.route("/admin")
def admin():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT nombre, fecha FROM reservas ORDER BY fecha")
    reservas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin.html", reservas=reservas)


# 🚀 Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
