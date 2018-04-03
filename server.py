from flask import Flask, render_template, flash, redirect, request, url_for, session, jsonify

# Importar ferramentas de gerenciamento de login com o flask
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
# Importar conector flask-mysql
#from flask_mysql import MySQL

# Não sei explicar ainda
from flask_sqlalchemy import *
#from flask_bcrypt import Bcrypt
#from werkzeug import generate_password_hash, check_password_hash
from pickle import *

# Importar formularios
from forms import EntrarForm, RegistrarForm, EnviarForm, QuizForm

# Para criar a aplicação
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
#app.secret_key = 'algo_secreto'

# Para criar o objeto do banco de dados
bd = SQLAlchemy(app)
#mysql = MySQL()
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = ''
#app.config['MYSQL_DATABASE_DB'] = ''
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#mysql.init_app(app)


# Para criar o objeto bcrypt
#bcrypt = Bcrypt(app)

# Para importar os modelos após a criação da aplicação
from models import *

# Para criar o objeto do LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Para configurar o objeto LoginManager
login_manager.login_view = 'entrar'
login_manager.login_message = 'Por favor entre em sua conta para visualizar esta página'

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.filter(Usuario.id == int(id_usuario)).first()

def getStandings():
    usuarios = Usuario.query.order_by(Usuario.recorde.desc())
    return usuarios

# Traça a rota web à página inicial
@app.route('/')
def index():
    return render_template('index.html.j2', usuarios=getStandings())

# Traça uma rota web à página de login
@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    erro = None
    form = EntrarForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(usuario=request.form['usuario']).first()
            if usuario is not None and (usuario.senha, request.form['senha']):
                login_user(usuario)
                flash('Você se conectou ao servidor!')
                return redirect(url_for('index'))
            else:
                erro = 'Credenciais inválidas, tente novamente!'
        else:
            erro = 'Credenciais inválidas, tente novamente!'
            render_template('login.html.j2', form=form, erro=erro)
    return render_template('login.html.j2', form=form)

# Traça uma rota web à página de registro
@app.route('/registrar')
def registrar():
    form = RegistrarForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            usuario = Usuario(nome=form.nome.data, usuario=form.usuario.data, senha=form.senha.data, recorde=0)
            bd.session.add(usuario)
            bd.session.commit()
            login_user(usuario)
            flash('Você foi cadastrado e conectado ao servidor')
            return redirect(url_for('index'))
        logout_user()
        flash('Você foi desconectado do servidor')
    return render_template('register.html.j2', form=form)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Você se desconectou do servidor')
    return redirect(url_for('entrar'))

@app.route('/enviar', methods=['GET', 'POST'])
@login_required
def enviar():
    form = EnviarForm()
    if form.validate_on_submit():
        questao_data = Questoes(
            questao=form.questao.data,
            opcao1=form.opcao1.data,
            opcao2=form.opcao2.data,
            opcao3=form.opcao3.data,
            opcao4=form.opcao4.data,
            resposta=form.resposta.data,
            id_criador=current_user.id,
            categoria=form.categoria.data
        )
        bd.session.add(questao_data)
        bd.session.commit
        flash('Sua questao foi enviada para o servidor')
        return render_template('enviar.html.j2', form=form, usuarios=getStandings())
    return render_template('enviar.html.j2', form=form, usuarios=getStandings())

@app.route('/jogo', methods=['GET', 'POST'])
@login_required
def quiz():
    form = QuizForm()
    if current_user.respondidas is None:
        current_user.respondidas = dumps([])
        bd.session.commit()
        questoes_disponiveis = Questoes.query.filter(Questoes.id_criador != str(current_user.id)).all()
        return render_template('trivia.html.j2', questoes_disponiveis=questoes_disponiveis, form=form, usuarios=getStandings())
    else:
        ja_respondido = loads(current_user.respondidas)
        questoes_disponiveis = Questoes.query.filter(Questoes.id_criador != str(current_user.id)).filter(Questoes.id_questao.in_(ja_respondido)).all()
        return render_template('trivia.html.j2', questoes_disponiveis=questoes_disponiveis, form=form, usuarios=getStandings())

@app.route('/resposta')
def pegar_resposta():
    id = request.args.get('id', 0, type=int)
    valor = request.args.get('valor', 0, type=str)
    id_usuario = request.args.get('id_usuario', 0, type=int)

    tentativa_questao = Questoes.query.filter(Questoes.id_questao == id).all()
    usuario_atual = Usuario.query.get(id_usuario)
    recorde_atual = usuario_atual.recorde

    if tentativa_questao[0].resposta == valor:
        recorde_atual = recorde_atual + 1
        usuario_atual.recorde = recorde_atual
        correto = 1
    else:
        recorde_atual = recorde_atual - 1
        usuario_atual.recorde = recorde_atual
        correto = 0

    pickle_antes = usuario_atual.respondidas
    pickle_depois = loads(pickle_antes)

    pickle_depois.append(16)
    current_user.respondidas = dumps(pickle_depois)
    bd.session.commit()

    return jsonify(recorde=recorde_atual, correto=correto)

@app.route('/ranking')
@login_required
def ranking():
    usuarios = Usuario.query.order_by(Usuario.recorde.desc())
    return render_template('ranking.html.j2', usuarios=usuarios)

# Para inicializar o arquivo
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
