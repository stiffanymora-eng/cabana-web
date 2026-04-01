from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL").strip()

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# 🏠 HOME
@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Cabaña ME</title>
    </head>
    <body style="font-family:Arial;margin:0;background:linear-gradient(to right,#4facfe,#00f2fe);color:white;text-align:center;">

        <div style="padding:80px;">
            <h1 style="font-size:50px;">🏡 Cabaña ME</h1>
            <p style="font-size:20px;">Disfruta una experiencia única</p>

            <a href="/reserva" style="background:white;color:#007BFF;padding:15px 30px;border-radius:10px;text-decoration:none;font-size:18px;">
                Reservar ahora
            </a>

            <br><br>

            <a href="/ver-reservas" style="color:white;font-size:18px;">
                📅 Ver reservas
            </a>
        </div>

    </body>
    </html>
    """

# 📅 RESERVA
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

            # 🔴 Verificar si la fecha ya está ocupada
            cur.execute("SELECT * FROM reservas WHERE fecha = %s", (fecha,))
            existente = cur.fetchone()

            if existente:
                return """
                <html>
                <body style="font-family:Arial;text-align:center;background:#f4f4f4;">
                    <h2 style='color:red;'>❌ Fecha ya reservada</h2>
                    <a href='/reserva'>Intentar otra fecha</a>
                </body>
                </html>
                """

            # ✅ Guardar reserva
            cur.execute(
                "INSERT INTO reservas (nombre, fecha) VALUES (%s, %s)",
                (nombre, fecha)
            )

            conn.commit()
            cur.close()
            conn.close()

            return f"""
            <html>
            <body style="font-family:Arial;text-align:center;background:#f4f4f4;padding-top:50px;">

                <h2 style='color:green;'>✅ Reserva confirmada</h2>

                <a href='/reserva'>Nueva reserva</a><br><br>

                <a href='https://wa.me/50689872394?text=Hola,%20reserva%20confirmada%20a%20nombre%20de%20{nombre}%20para%20el%20{fecha}'
                   style='background:#25D366;color:white;padding:15px 30px;border-radius:10px;text-decoration:none;font-size:18px;'>
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
        <title>Reservar - Cabaña ME</title>
    </head>
    <body style="font-family:Arial;background:#f4f4f4;text-align:center;">

        <h1>🏡 Reserva en Cabaña ME</h1>

        <form method="POST" style="
            background:white;
            padding:30px;
            border-radius:15px;
            display:inline-block;
            box-shadow:0 0 20px rgba(0,0,0,0.1);
        ">
            <input name="nombre" placeholder="Tu nombre" required
                style="padding:10px;width:220px;"><br><br>

            <input name="fecha" type="date" required
                style="padding:10px;width:220px;"><br><br>

            <button type="submit"
                style="padding:12px 25px;background:#007BFF;color:white;border:none;border-radius:8px;font-size:16px;">
                Reservar
            </button>
        </form>

    </body>
    </html>
    """

# 📋 VER RESERVAS
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
        lista += f"""
        <div style='background:white;padding:15px;margin:10px;border-radius:10px;box-shadow:0 0 10px rgba(0,0,0,0.1);'>
            <b>{r[0]}</b><br>
            📅 {r[1]}
        </div>
        """

    return f"""
    <html>
    <head>
        <title>Reservas - Cabaña ME</title>
    </head>
    <body style="font-family:Arial;background:#f4f4f4;text-align:center;">

        <h1>📅 Reservas</h1>

        {lista if lista else "<p>No hay reservas aún</p>"}

        <br>
        <a href="/" style="text-decoration:none;color:#007BFF;">⬅ Volver</a>

    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
