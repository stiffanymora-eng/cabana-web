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
    <body style="
        margin:0;
        font-family:Arial;
        background:url('https://images.unsplash.com/photo-1505693416388-ac5ce068fe85') no-repeat center/cover;
        color:white;
        text-align:center;
    ">

    <div style="background:rgba(0,0,0,0.6);height:100vh;padding-top:100px;">

        <h1 style="font-size:60px;">🏡 Cabaña ME</h1>
        <p style="font-size:22px;">Escápate a la naturaleza</p>

        <a href="/reserva" style="
            background:#25D366;
            padding:15px 30px;
            border-radius:10px;
            color:white;
            text-decoration:none;
            font-size:20px;
        ">
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

            cur.execute("SELECT * FROM reservas WHERE fecha = %s", (fecha,))
            if cur.fetchone():
                return """
                <html>
                <body style="font-family:Arial;text-align:center;background:#111;color:white;padding-top:50px;">
                    <h2 style='color:red;'>❌ Fecha ya reservada</h2>
                    <a href='/reserva' style='color:#25D366;'>Intentar otra fecha</a>
                </body>
                </html>
                """

            cur.execute(
                "INSERT INTO reservas (nombre, fecha) VALUES (%s, %s)",
                (nombre, fecha)
            )

            conn.commit()
            cur.close()
            conn.close()

            return f"""
            <html>
            <body style="font-family:Arial;text-align:center;background:#111;color:white;padding-top:50px;">

                <h2 style='color:#25D366;'>✅ Reserva confirmada</h2>

                <a href='/reserva' style='color:white;'>Nueva reserva</a><br><br>

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
    <body style="
        margin:0;
        font-family:Arial;
        background:#111;
        color:white;
        text-align:center;
    ">

    <h1 style="padding-top:30px;">🏡 Reserva en Cabaña ME</h1>

    <form method="POST" style="
        background:#222;
        padding:30px;
        border-radius:15px;
        display:inline-block;
        box-shadow:0 0 20px rgba(0,0,0,0.5);
    ">
        <input name="nombre" placeholder="Tu nombre" required
            style="padding:10px;width:220px;"><br><br>

        <input name="fecha" type="date" required
            style="padding:10px;width:220px;"><br><br>

        <button type="submit"
            style="padding:12px 25px;background:#25D366;color:white;border:none;border-radius:8px;">
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
        <div style='background:#222;padding:15px;margin:10px;border-radius:10px;color:white;'>
            <b>{r[0]}</b><br>
            📅 {r[1]}
        </div>
        """

    return f"""
    <html>
    <body style="background:#111;font-family:Arial;text-align:center;color:white;">

        <h1>📅 Reservas</h1>

        {lista if lista else "<p>No hay reservas aún</p>"}

        <br>
        <a href="/" style="color:#25D366;">⬅ Volver</a>

    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
