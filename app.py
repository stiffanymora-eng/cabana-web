from flask import Flask, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "secreto123"  # 🔐 clave para login

DATABASE_URL = os.getenv("DATABASE_URL").strip()

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# 🏠 HOME
@app.route('/')
def index():
    return """
    <html>
    <body style="margin:0;font-family:Arial;background:#111;color:white;text-align:center;">
        <h1 style="padding-top:50px;">🏡 Cabaña ME</h1>
        <p>Escápate a la naturaleza</p>

        <a href="/reserva" style="background:#25D366;padding:15px 30px;border-radius:10px;color:white;text-decoration:none;">
            Reservar ahora
        </a>

        <br><br>

        <a href="/login" style="color:#25D366;">🔐 Admin</a>
    </body>
    </html>
    """

# 📅 RESERVA
@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']

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
            return "<h2 style='color:red;text-align:center;'>❌ Fecha ocupada</h2><a href='/reserva'>Volver</a>"

        cur.execute(
            "INSERT INTO reservas (nombre, fecha) VALUES (%s, %s)",
            (nombre, fecha)
        )

        conn.commit()
        cur.close()
        conn.close()

        return f"""
        <h2 style='text-align:center;color:green;'>✅ Reserva confirmada</h2>
        <div style='text-align:center;'>
            <a href='https://wa.me/50689872394?text=Reserva%20{nombre}%20{fecha}'
               style='background:#25D366;color:white;padding:15px;border-radius:10px;text-decoration:none;'>
               📲 WhatsApp
            </a>
        </div>
        """

    return """
    <html>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;">
        <h1>Reservar</h1>

        <form method="POST">
            <input name="nombre" placeholder="Nombre" required><br><br>
            <input name="fecha" type="date" required><br><br>
            <button>Reservar</button>
        </form>
    </body>
    </html>
    """

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']

        if user == "admin" and password == "1234":
            session['admin'] = True
            return redirect('/admin')

        return "<h3 style='color:red;'>Credenciales incorrectas</h3>"

    return """
    <html>
    <body style="text-align:center;font-family:Arial;">
        <h1>🔐 Login Admin</h1>

        <form method="POST">
            <input name="user" placeholder="Usuario"><br><br>
            <input name="password" type="password" placeholder="Contraseña"><br><br>
            <button>Entrar</button>
        </form>
    </body>
    </html>
    """

# 📊 PANEL ADMIN
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, nombre, fecha FROM reservas ORDER BY fecha")
    reservas = cur.fetchall()

    cur.close()
    conn.close()

    lista = ""
    for r in reservas:
        lista += f"""
        <div style='background:#222;padding:15px;margin:10px;border-radius:10px;color:white;'>
            <b>{r[1]}</b> - {r[2]}<br><br>

            <a href='/eliminar/{r[0]}' style='color:red;'>❌ Eliminar</a>
        </div>
        """

    return f"""
    <html>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;">
        <h1>📊 Panel Admin</h1>

        {lista if lista else "<p>No hay reservas</p>"}

        <br>
        <a href="/logout" style="color:#25D366;">Cerrar sesión</a>
    </body>
    </html>
    """

# 🗑️ ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    if not session.get('admin'):
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM reservas WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect('/admin')

# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
