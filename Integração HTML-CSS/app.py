from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('agendar.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
);
""")
conn.commit()

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    data = request.form['data']
    hora = request.form['hora']
    nome = request.form['nome']
    email = request.form['email']
    conn = sqlite3.connect('agendar.db')
    c = conn.cursor()

    # Verifica se já existe um agendamento para a data e hora selecionadas
    c.execute("""
    SELECT COUNT(*) FROM agendamentos
    WHERE data = ? AND hora = ?
    """, (data, hora))
    count = c.fetchone()[0]
    if count > 0:
        # Caso já exista um agendamento, exibe uma mensagem de erro personalizada
        return render_template('erro.html', mensagem='Já existe um agendamento para a data e hora selecionadas.')
    else:
        # Caso não exista, insere o novo agendamento no banco de dados
        c.execute("""
        INSERT INTO agendamentos (data, hora, nome, email)
        VALUES (?, ?, ?, ?)
        """, (data, hora, nome, email))
        conn.commit()
        conn.close()
        return redirect('/sucesso.html')

@app.route ('/agendamento')
def cadastradosucesso():
    return render_template('formulario.html')

@app.route ('/historico')
def historico():
    return render_template('historico.html')

@app.route ('/perfil')
def mostrarPerfil():
    return render_template('perfil.html')

@app.route ('/login')
def mostrarLogin():
    return render_template('login.html')

@app.route ('/cadastro')
def mostrarCadastro():
    return render_template('cadastro.html')

# definindo a página exibida quando a url for 'http://127.0.0.1:5000/acompanhamento'
@app.route("/acompanhamento")
def acompanhamento():

    # se conectando com o banco de dados para fazer as devidas manipulações
    conn = sqlite3.connect('agenda.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM agendaTable')
    dados = cursor.fetchall()

    conn.close()

    return render_template('acompanhamento.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)
