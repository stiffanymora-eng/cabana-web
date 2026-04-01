from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1 style='text-align:center;'>Cabaña ME</h1>
    <div style='text-align:center;'>
        <a href='/reserva'>Reservar</a>
    </div>
    """

@app.route('/reserva', methods=['GET','POST'])
def reserva():
    if request.method == 'POST':
        return redirect('/confirmado')

    return """
    <style>
        body {
            background:#0f172a;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            color:white;
            font-family:sans-serif;
        }

        .card {
            background:#1e293b;
            padding:40px;
            border-radius:20px;
            text-align:center;
        }
    </style>

    <div class="card">
        <h1>Reservar</h1>

        <form method="POST">
            <input type="text" name="nombre" placeholder="Tu nombre"><br><br>
            <input type="date" name="fecha"><br><br>

            <button>Reservar</button>
        </form>
    </div>
    """

@app.route('/confirmado')
def confirmado():
    return "<h1 style='text-align:center;'>Reserva confirmada</h1>"

if __name__ == '__main__':
    app.run()
