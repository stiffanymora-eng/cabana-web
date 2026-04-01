from flask import Flask, request
import psycopg2

app = Flask(__name__)

DATABASE_URL = "postgresql://cabana_db_bslw_user:OWImMBfuedmMJjci4jqkdEwLEEAECAP2@dpg-d76a6nmslomc738ep61g-a.oregon-postgres.render.com/cabana_db_bslw"

def get_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


# 🏠 HOME
@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Cabaña ME</title>
        <style>
            body {
                margin:0;
                font-family: Arial;
                background:#0f172a;
                color:white;
            }

            .hero {
                height:90vh;
                background:url('https://images.unsplash.com/photo-1505691938895-1758d7feb511') center/cover;
                display:flex;
                align-items:center;
                justify-content:center;
                flex-direction:column;
                text-align:center;
            }

            .hero h1 {
                font-size:60px;
                margin:0;
            }

            .btn {
                background:#25D366;
                padding:15px 30px;
                border-radius:10px;
                color:white;
                text-decoration:none;
                margin-top:20px;
                font-size:18px;
            }

            .section {
                padding:40px;
                text-align:center;
            }

            .card {
                background:#1e293b;
                padding:20px;
                margin:10px;
                border-radius:15px;
                display:inline-block;
                width:250px;
            }

            .whatsapp {
                position:fixed;
                bottom:20px;
                right:20px;
                background:#25D366;
                padding:15px;
                border-radius:50%;
                font-size:25px;
                text-decoration:none;
                color:white;
            }
        </style>
    </head>

    <body>

        <div class="hero">
            <h1>🏡 Cabaña ME</h1>
            <p>Escápate a la naturaleza</p>

            <a href="/reserva" class="btn">Reservar ahora</a>
        </div>

        <div class="section">
            <h2>🌲 Experiencia</h2>

            <div class="card">🔥 Fogata</div>
            <div class="card">🌄 Vista increíble</div>
            <div class="card">🛏️ Comodidad total</div>
        </div>

        <a class="whatsapp" href="https://wa.me/50689872394">📲</a>

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
            conn = get_db()
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS reservas (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT,
                    fecha TEXT
                )
            """)

            cur.execute("INSERT INTO reservas (nombre, fecha) VALUES (%s, %s)", (nombre, fecha))

            conn.commit()
            cur.close()
            conn.close()

            return """
            <html>
            <head>
                <title>Confirmado</title>
                <style>
                    body {
                        font-family: Arial;
                        background:#0f172a;
                        color:white;
                        text-align:center;
                        padding-top:100px;
                    }

                    .card {
                        background:#1e293b;
                        padding:40px;
                        border-radius:20px;
                        display:inline-block;
                    }

                    h1 {
                        color:#22c55e;
                    }

                    .btn {
                        display:block;
                        margin:15px;
                        padding:15px;
                        border-radius:10px;
                        text-decoration:none;
                        color:white;
                    }

                    .whatsapp {
                        background:#25D366;
                    }

                    .volver {
                        background:#3b82f6;
                    }
                </style>
            </head>

            <body>

                <div class="card">
                    <h1>✅ Reserva confirmada</h1>

                    <a class="btn volver" href="/">⬅ Volver</a>

                    <a class="btn whatsapp" href="https://wa.me/50689872394">
                        📲 Confirmar por WhatsApp
                    </a>
                </div>

            </body>
            </html>
            """

        except Exception as e:
            return f"Error: {e}"

    return """
    <html>
    <head>
        <style>
            body {
                font-family: Arial;
                background:#0f172a;
                color:white;
                text-align:center;
                padding-top:100px;
            }

            input, button {
                padding:10px;
                margin:10px;
                border-radius:8px;
                border:none;
            }

            button {
                background:#22c55e;
                color:white;
            }
        </style>
    </head>

    <body>

        <h1>Reservar</h1>

        <form method="POST">
            <input name="nombre" placeholder="Tu nombre"><br>
            <input type="date" name="fecha"><br>
            <button>Reservar</button>
        </form>

    </body>
    </html>
    """


# 📊 ADMIN
@app.route('/admin')
def admin():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM reservas")
    data = cur.fetchall()

    cur.close()
    conn.close()

    html = "<h1>Reservas</h1>"

    for r in data:
        html += f"<p>{r[1]} - {r[2]}</p>"

    return html


if __name__ == "__main__":
    app.run()
