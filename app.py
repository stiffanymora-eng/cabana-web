from flask import Flask, render_template, request
import os

app = Flask(__name__)

NUMERO_WHATSAPP = "50689872394"  # tu número

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    fechas_ocupadas = set()
    mensaje = ""
    link_whatsapp = ""

    # Leer reservas guardadas
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

            # Link de WhatsApp
            link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text=Hola soy {nombre} y quiero confirmar mi reserva para {fecha}"

    return render_template(
        "reserva.html",
        fechas=sorted(fechas_ocupadas),
        mensaje=mensaje,
        link_whatsapp=link_whatsapp
    )


# ⚠️ IMPORTANTE PARA RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))