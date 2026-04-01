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
    <body style="font-family:Arial;text-align:center;background:#f4f4f4;">
        <h1>🏡 Cabaña Paraíso</h1>
        <p>Reserva tu experiencia</p>
        <a href="/reserva" style="background:#007BFF;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;">
            Reservar ahora
        </a><br><br>

        <a href="/ver-reservas">📅 Ver reservas</a>
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
                    fecha DATE UNIQUE
                )
            """)

            # 🔴 verificar si ya existe la fecha
            cur.execute("SELECT * FROM reservas WHERE fecha = %s", (fecha,))
            existente = cur.fetchone()

            if existente:
                return """
                <h2 style='color:red;'>❌ Fecha ya reservada</h2>
                <a href='/reserva'>Intentar otra fecha</a>
                """

            # guardar reserva
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
                <h2 style='color:green;'>✅ Reserva confirmada</h2>

                <a href='/reserva'>Nueva reserva</a><br><br>

                <a href='https://wa.me/50689872394?text=Hola,%20reserva%20confirmada%20a%20nombre%20de%20{nombre}%20para%20el%20{fecha}'
                   style='background:#25D366;color:white;padding:15px 25px;border-radius:10px;text-decoration:none;font-size:18px;'>
                   📲 Confirmar por WhatsApp
                </a>
            </body>
            </html>
            """

        except Exception as e:
            return f"ERROR: {e}"

    return """
    <html>
    <body style="font-family:Arial;text-align:center;background:#f4f4f4;">
        <h1>🏡 Reserva tu cabaña</h1>

        <form method="POST" style="background:white;padding:30px;border-radius:15px;display:inline-block;box-shadow:0 0 15px rgba(0,0,0,0.1);">
            <input name="nombre" placeholder="Tu nombre" required style="padding:10px;width:200px;"><br><br>
            <input name="fecha" type="date" required style="padding:10px;width:200px;"><br><br>

            <button type="submit" style="padding:10px 20px;background:#007BFF;color:white;border:none;border-radius:5px;">
                Reservar
            </button>
        </form>
    </body>
    </html>
    """

@app.route('/ver-reservas')
def ver_reservas():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT nombre, fecha FROM reservas ORDER BY fecha")
    reservas = cur.fetchall()

    cur.close()
    conn.close()

    lista = ""
    for r in reservas:
        lista += f"<li>{r[0]} - {r[1]}</li>"

    return f"""
    <html>
    <body style="font-family:Arial;text-align:center;">
        <h1>📅 Reservas</h1>
        <ul style="list-style:none;">
            {lista}
        </ul>
        <a href="/">Volver</a>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
