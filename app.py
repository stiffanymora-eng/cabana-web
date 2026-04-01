from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

# IMPORTANTE: limpia espacios invisibles
DATABASE_URL = os.getenv("DATABASE_URL").strip()

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def index():
    return "<h1>Bienvenido</h1><a href='/reserva'>Ir a reserva</a>"

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

            return "Reserva guardada correctamente"

        except Exception as e:
            return f"ERROR: {e}"

    return """
    <form method="POST">
        Nombre: <input name="nombre"><br>
        Fecha: <input name="fecha" type="date"><br>
        <button type="submit">Guardar</button>
    </form>
    """

if __name__ == '__main__':
    app.run(debug=True)
