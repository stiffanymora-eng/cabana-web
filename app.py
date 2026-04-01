from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL").strip()

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def index():
    return """
    <html>
    <body style="font-family:Arial;text-align:center;">
        <h1>🏡 Bienvenido a la Cabaña</h1>
        <a href="/reserva">👉 Hacer Reserva</a>
    </body>
    </html>
    """

@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS reservas (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT,
                    fecha DATE
                )
            """)

            cur.execute(
                "INSERT INTO reservas (nombre, fecha) VALUES (%s, %s)",
                (nombre, fecha)
            )

            conn.commit()
            cur.close()
            conn.close()

            return f"""
            <html>
            <body style="font-family:Arial;text-align:center;background:#f4f4f4;">
                <h2 style='color:green;'>✅ Reserva guardada correctamente</h2>

                <a href='/reserva'>Hacer otra reserva</a><br><br>

                <a href='https://wa.me/50689872394?text=Hola,%20hice%20una%20reserva%20a%20nombre%20de%20{nombre}%20para%20el%20{fecha}'
                   style='background:#25D366;color:white;padding:15px 25px;text-decoration:none;border-radius:10px;font-size:18px;'>
                   📲 Confirmar por WhatsApp
                </a>
            </body>
            </html>
            """

        except Exception as e:
            return f"ERROR: {e}"

    return """
    <html>
    <head>
        <title>Reservar</title>
    </head>
    <body style="font-family:Arial;text-align:center;background:#f4f4f4;">
        <h1>🏡 Reserva tu Cabaña</h1>

        <form method="POST" style="background:white;padding:30px;border-radius:15px;display:inline-block;box-shadow:0 0 10px rgba(0,0,0,0.1);">
            <input name="nombre" placeholder="Tu nombre" required style="padding:10px;width:200px;"><br><br>
            <input name="fecha" type="date" required style="padding:10px;width:200px;"><br><br>

            <button type="submit" style="padding:10px 20px;background:#007BFF;color:white;border:none;border-radius:5px;font-size:16px;">
                Reservar
            </button>
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
