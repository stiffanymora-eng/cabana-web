from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

NUMERO_WHATSAPP = "50689872394"

# 🔗 Conexión a la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


# 🏠 Inicio
@app.route("/")
def home():
    return render_template("index.html")


# 📅 Reserva
@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    mensaje = ""
    link_whatsapp = ""

    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha = request.form["fecha"]

        conn = get_db_connection()
        cur = conn.cursor()

        # Crear tabla si no existe
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id SERIAL PRIMARY KEY,
                nombre TEXT,
                fecha DATE
            )
        """)

        # Guardar reserva
        cur.execute(
            "INSERT INTO reservas (nombre, fecha) VALUES (%s, %s)",
            (nombre, fecha)
        )

        conn.commit()
        cur.close()
        conn.close()

        mensaje = "Reserva guardada correctamente"

        link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text=Hola soy {nombre} y quiero confirmar mi reserva para {fecha}"

    return render_template(
        "reserva.html",
        mensaje=mensaje,
        link_whatsapp=link_whatsapp
    )


# 🛠️ Admin
@app.route("/admin")
def admin():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT nombre, fecha FROM reservas ORDER BY fecha")
    reservas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin.html", reservas=reservas)


# ⚠️ Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
