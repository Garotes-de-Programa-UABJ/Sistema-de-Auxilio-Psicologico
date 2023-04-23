from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'uabjpsychoatendsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:8aZp6T3VHFbdmzGQlPIu@containers-us-west-35.railway.app:6768/railway'

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

class perfil_usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100))
    nome_social = db.Column(db.String(100))
    data_nascimento = db.Column(db.String(100))
    naturalidade = db.Column(db.String(100))
    estado_civil = db.Column(db.String(100))
    cpf = db.Column(db.String(100), unique=True)
    telefone = db.Column(db.String(100))
    email_institucional = db.Column(db.String(100), unique=True)
    email_alternativo = db.Column(db.String(100), unique=True)
    endereco_residencial = db.Column(db.String(100))
    nome_mae = db.Column(db.String(100))
    curso = db.Column(db.String(100))
    periodo_graduacao = db.Column(db.String(100))
    bolsista = db.Column(db.String(100))
    tipo_bolsa = db.Column(db.String(100))
    pronomes = db.Column(db.String(100))
    genero = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    usuario = db.relationship('User', backref='perfil_usuario')


class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String(80), unique=False, nullable=False)
    hora = db.Column(db.String(80), unique=False, nullable=False)
    status= db.Column(db.String(80), unique=False, nullable=False)
    motivo_atendimento = db.Column(db.String(100), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    perfil_id= db.Column(db.Integer, db.ForeignKey('perfil_usuario.id'), nullable=False)

    user= db.relationship('User', backref='agendamentos')
    perfil= db.relationship('perfil_usuario', backref='agendamentos')

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'mostrarLogin'
login_manager.login_message = 'Você precisa estar logado para acessar essa página!'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # como o user_id é apenas a chave primária da tabela de usuários, use-o na consulta para encontrar o usuário
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/agendar', methods=['POST'])
@login_required
def agendar():
    user= current_user
    data = request.form['data']
    hora = request.form['hora']
    motivo_atendimento = request.form['motivo_atendimento']
    perfil= perfil_usuario.query.filter_by(usuario_id=user.id).first()

    def verificar_horario_disponivel(data, hora):
    # Consultar o banco de dados para verificar se já existe um agendamento com a mesma data e hora
        agendamento_existente = Agendamento.query.filter_by(data=data, hora=hora).filter(Agendamento.status.in_(['Marcado', 'Remarcado'])).first()

    # Se já existe um agendamento com a mesma data e hora, retornar False, indicando que o horário não está disponível
        if agendamento_existente:
            return False

    # Se não existe um agendamento com a mesma data e hora, retornar True, indicando que o horário está disponível
        return True

 # Chamar a função de verificação de horário disponível
    if verificar_horario_disponivel(data, hora):
        # Se o horário estiver disponível, verificar se o usuário tem um agendamento anterior com status diferente de 'começado'
        agendamento_anterior = Agendamento.query.filter_by(user=user).filter(Agendamento.status.in_(['Marcado', 'Remarcado'])).first()
        if agendamento_anterior:
            flash('Você já possui um agendamento marcado!', 'danger')
            return redirect(url_for('acompanhamento'))
        else:
            # Se o usuário não tem um agendamento anterior com status diferente de 'Marcado', criar um novo agendamento
            novo_agendamento = Agendamento(data=data, hora=hora, status='Marcado', user=user, perfil=perfil, motivo_atendimento=motivo_atendimento)
            db.session.add(novo_agendamento)
            db.session.commit()

            return redirect(url_for('acompanhamento'))
    else:
        flash('Horário indisponível. Por favor, escolha outro horário.', 'danger')
        return redirect(url_for('agendamento'))

@app.route ('/agendamento')
@login_required
def agendamento():
    return render_template('agendamento.html')

@app.route("/acompanhamento", methods=['POST', 'GET'])
@login_required
def acompanhamento():
    # Obter o usuário atualmente logado
    user = current_user

    # Obter todos os agendamentos do banco de dados
    agendamentos = Agendamento.query.filter_by(user=user).filter(Agendamento.status.in_(['Marcado', 'Remarcado'])).all()

    # Renderizar a página de acompanhamento, passando a lista de agendamentos e o usuário atualmente logado
    return render_template('acompanhamento.html', agendamentos=agendamentos, user=user)

@app.route('/cancelar/<int:agendamento_id>', methods=['POST', 'GET'])
@login_required
def cancelar(agendamento_id):
    agendamento = Agendamento.query.get(agendamento_id)
    if agendamento:
        agendamento.status = 'Cancelado'
        db.session.commit()
        flash('Consulta cancelada com sucesso.', 'success')
        return redirect(url_for('historico'))
    else:
        flash('ERRO', 'danger')
        return redirect(url_for('acompanhamento'))


@app.route ('/historico', methods=['POST', 'GET'])
@login_required
def historico():
    
    user = current_user

    consultas_cc = Agendamento.query.filter_by(status='Concluido', user=user).all()
    consultas_ca = Agendamento.query.filter_by(status='Cancelado', user=user).all()

    
    return render_template('historico.html', consultas_cc=consultas_cc, consultas_ca=consultas_ca, user=user)

@app.route('/perfil', methods=['POST','GET'])
@login_required
def perfil():
    user = current_user

    perfilU = perfil_usuario.query.filter_by(usuario_id=user.id).all()

    return render_template('perfil.html', perfilU=perfilU, user=user)
@app.route('/perfil-editar', methods=['POST','GET'])
@login_required
def perfil_editar():
    return render_template('perfileditar.html')

@app.route('/perfil-editar_bd', methods=['POST','GET'])
@login_required
def perfil_editar_bd():
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
    pronomes = request.form['pronomes']
    genero = request.form['genero']
    usuario= current_user

    cpf = perfil_usuario.query.filter_by(cpf=cpf).first()
    inst = perfil_usuario.query.filter_by(email_institucional=email_institucional).first()
    if cpf:
        flash('CPF já cadastrado!')
        return redirect(url_for('perfil_editar'))
    elif inst:
        flash('Email já cadastrado!')
        return redirect(url_for('perfil_editar'))
    
    new_perf= perfil_usuario(nome_completo=nome_completo, nome_social=nome_social, data_nascimento=data_nascimento, naturalidade=naturalidade, estado_civil=estado_civil, cpf=cpf, telefone=telefone, email_institucional=email_institucional, email_alternativo=email_alternativo, endereco_residencial=endereco_residencial, nome_mae=nome_mae, curso=curso, periodo_graduacao=periodo_graduacao, bolsista=bolsista, tipo_bolsa=tipo_bolsa, pronomes=pronomes, genero=genero, usuario=usuario)

    db.session.add(new_perf)
    db.session.commit()

    return redirect(url_for('perfil'))

@app.route ('/login')
def mostrarLogin():
    return render_template('login.html')

@app.route('/login-db', methods=['POST'])
def login_db():
    # Obter o email e senha do formulário de login
    email = request.form.get('email')
    password = request.form.get('password')

    # Procurar o usuário no banco de dados pelo email fornecido
    user = User.query.filter_by(email=email).first()

    # Verificar se o usuário existe e se a senha fornecida está correta
    if not user or not check_password_hash(user.password, password):
        # Se o usuário não existir ou a senha estiver incorreta, redirecionar para a página de login e exibir uma mensagem de erro
        flash('Por favor, verifique suas informações de login e tente novamente.')
        return redirect(url_for('mostrarLogin'))

    # Se todas as verificações passarem, o usuário tem as credenciais corretas
    login_user(user)
    return redirect(url_for('perfil'))

@app.route ('/register')
def mostrarCadastro():
    return render_template('cadastrar.html')

@app.route('/cadastro-db', methods=['POST'])
def register_db():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # se o email já existir, não deixa registrar

    if user: # se um usuário for encontrado, queremos redirecionar de volta para a página de inscrição para que o usuário possa tentar novamente
        flash('Email já cadastrado!')
        return redirect(url_for('mostrarCadastro'))

    # crie um novo usuário com os dados do formulário. Faça o hash da senha para que a versão em texto simples não seja salva.
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

    # Adicione o novo usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for('perfil_editar'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_server_error(error):
    return str(error), 500

if __name__ == '__main__':
    app.run(debug=True)
