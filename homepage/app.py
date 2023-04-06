# importando bibliotecas necessárias
from flask import Flask, render_template
import sqlite3


# inicia uma instância do app
app = Flask(__name__)


# definindo a página exiibida quando a url for 'http://127.0.0.1:5000/paghome'
@app.route("/paghome")
def home():
  return render_template('home.html')

app.run(debug=True)