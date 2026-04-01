from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

NUMERO_WHATSAPP = "50689872394"
PASSWORD_ADMIN = "1234"

# 📦 CREAR BASE DE DATOS
def init_db():
    conn = sqlite3.connect("reservas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    conn = sqlite3.connect("reservas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT fecha FROM reservas")
    fechas_ocupadas = [row[0] for row in cursor.fetchall()]

    mensaje = ""
    link_whatsapp = ""

    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha = request.form["fecha"]

        if fecha in fechas_ocupadas:
            mensaje = "Lo sentimos, esta fecha ya está reservada"
        else:
            cursor.execute("INSERT INTO reservas (nombre, fecha) VALUES (?, ?)", (nombre, fecha))
            conn.commit()

            mensaje = "Reserva guardada correctamente"
            link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text=Hola soy {nombre} y quiero confirmar mi reserva para {fecha}"

    conn.close()

    return render_template(
        "reserva.html",
        fechas=fechas_ocupadas,
        mensaje=mensaje,
        link_whatsapp=link_whatsapp
    )


# 🔐 LOGIN ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = ""

    if request.method == "POST":
        if request.form["password"] == PASSWORD_ADMIN:
            return redirect(url_for("panel"))
        else:
            error = "Contraseña incorrecta"

    return render_template("login.html", error=error)


# 📊 PANEL ADMIN
@app.route("/panel")
def panel():
    conn = sqlite3.connect("reservas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, fecha FROM reservas")
    reservas = cursor.fetchall()

    conn.close()

    return render_template("admin.html", reservas=reservas)


# 🗑️ ELIMINAR
@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = sqlite3.connect("reservas.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reservas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("panel"))


if __name__ == "__main__":
    app.run(debug=True)
