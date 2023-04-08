from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/perfil', methods=['POST'])
def perfil():
    nome_completo = request.form['nome_completo']
    nome_social = request.form['nome_social']
    data_nascimento = request.form['data_nascimento']
    naturalidade = request.form['naturalidade']
    estado_civil = request.form['estado_civil']
    cpf = request.form['cpf']
    telefone = request.form['telefone']
    email_institucional = request.form['email_institucional']
    email_alternativo = request.form['email_alternativo']
    endereco_residencial = request.form['endereco_residencial']
    nome_mae = request.form['nome_mae']
    curso = request.form['curso']
    periodo_graduacao = request.form['periodo_graduacao']
    bolsista = request.form['bolsista']
    tipo_bolsa = request.form['tipo_bolsa']
    motivo_atendimento = request.form['motivo_atendimento']
    pronomes = request.form['pronomes']

    # banco de dados aqui

    return render_template('perfil.html', nome_completo=nome_completo, nome_social=nome_social, data_nascimento=data_nascimento, naturalidade=naturalidade, estado_civil=estado_civil, cpf=cpf, telefone=telefone, email_institucional=email_institucional, email_alternativo=email_alternativo, endereco_residencial=endereco_residencial, nome_mae=nome_mae, curso=curso, periodo_graduacao=periodo_graduacao, bolsista=bolsista, tipo_bolsa=tipo_bolsa, motivo_atendimento=motivo_atendimento, pronomes=pronomes)

if __name__ == '__main__':
    app.run(debug=True)
