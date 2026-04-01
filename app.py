from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

NUMERO_WHATSAPP = "50689872394"

# 🔐 contraseña admin
PASSWORD_ADMIN = "1234"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    fechas_ocupadas = set()
    mensaje = ""
    link_whatsapp = ""

    if os.path.exists("reservas.txt"):
        with open("reservas.txt", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(" - ")
                if len(partes) == 2:
                    fechas_ocupadas.add(partes[1])

    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha = request.form["fecha"]

        if fecha in fechas_ocupadas:
            mensaje = "Lo sentimos, esta fecha ya está reservada"
        else:
            with open("reservas.txt", "a") as archivo:
                archivo.write(f"{nombre} - {fecha}\n")

            mensaje = "Reserva guardada correctamente"
            link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text=Hola soy {nombre} y quiero confirmar mi reserva para {fecha}"

    return render_template("reserva.html", fechas=sorted(fechas_ocupadas), mensaje=mensaje, link_whatsapp=link_whatsapp)


# 🔐 LOGIN ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = ""

    if request.method == "POST":
        password = request.form["password"]

        if password == PASSWORD_ADMIN:
            return redirect(url_for("panel"))
        else:
            error = "Contraseña incorrecta"

    return render_template("login.html", error=error)


# 📊 PANEL ADMIN
@app.route("/panel")
def panel():
    reservas = []

    if os.path.exists("reservas.txt"):
        with open("reservas.txt", "r") as archivo:
            for linea in archivo:
                reservas.append(linea.strip())

    return render_template("admin.html", reservas=reservas)


# 🗑️ ELIMINAR RESERVA
@app.route("/eliminar/<int:index>")
def eliminar(index):
    if os.path.exists("reservas.txt"):
        with open("reservas.txt", "r") as archivo:
            lineas = archivo.readlines()

        if 0 <= index < len(lineas):
            lineas.pop(index)

        with open("reservas.txt", "w") as archivo:
            archivo.writelines(lineas)

    return redirect(url_for("panel"))


if __name__ == "__main__":
    app.run(debug=True)
