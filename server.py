from flask import Flask, render_template, flash, redirect, request, url_for, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from flask_sqlalchemy import *
from pickle import *
from forms import EntrarForm, RegistrarForm, EnviarForm, QuizForm

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
bd = SQLAlchemy(app)

from models import *

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'entrar'
login_manager.login_message = 'Por favor entre em sua conta para visualizar esta página'

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.filter(Usuario.id == int(id_usuario)).first()

def getStandings():
    usuarios = Usuario.query.order_by(Usuario.recorde.desc())
    return usuarios

@app.route('/')
def index():
    return render_template('index.html.j2', usuarios=getStandings())

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    logout_user()
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
            return render_template('login.html.j2', form=form, erro=erro)
    return render_template('login.html.j2', form=form)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrarForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            usuario = Usuario(
                nome=form.nome.data,
                usuario=form.usuario.data,
                senha=form.senha.data,
                recorde=0, perm_acesso=0
            )
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
        bd.session.commit()
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
        print(questoes_disponiveis)
        return render_template('trivia.html.j2', questoes_disponiveis=questoes_disponiveis, form=form, usuarios=getStandings())
    else:
        ja_respondido = loads(current_user.respondidas)
        questoes_disponiveis = Questoes.query.filter(Questoes.id_criador != str(current_user.id)).filter(Questoes.id_questao.in_(ja_respondido)).all()
        print(questoes_disponiveis)
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
        current_user.recorde = recorde_atual
        correto = 1
    else:
        recorde_atual = recorde_atual - 1
        current_user.recorde = recorde_atual
        correto = 0

    beforePickle = current_user.respondidas
    afterPickle = loads(beforePickle)

    afterPickle.append(id)
    current_user.respondidas = dumps(afterPickle)
    bd.session.commit()

    return jsonify(recorde=recorde_atual, correto=correto)

@app.route('/jogo/<string:categoria>')
@login_required
def categoria_escolhida(categoria):
    categorias = ['enem',
                  'cfoav',
                  'detran',]
    if categoria in categorias:
        form = QuizForm()
        if current_user.respondidas is None:
            current_user.respondidas = dumps([])
            bd.session.commit()

        ja_respondido = loads(current_user.respondidas)
        questoes_disponiveis = Questoes.query.filter(Questoes.id_criador != str(current_user.id)).filter(Questoes.id_questao.in_(ja_respondido)).filter(Questoes.categoria == categoria).all()

        if len(questoes_disponiveis) is 0:
            flash('Não foi possível encontrar questões para tal escolha')
            return render_template('trivia.html.j2', questoes_disponiveis = questoes_disponiveis, form =  form, users = getStandings())
    else:
        form = QuizForm()
        if current_user.respondidas is None:
            current_user.respondidas = dumps([])
            bd.session.commit()

        ja_respondido = loads(current_user.respondidas)
        questoes_disponiveis = Questoes.query.filter(Questoes.id_criador != str(current_user.id)).filter(Questoes.id_questao.in_(ja_respondido)).all()
        flash('Por favor entre em url onde a categoria é uma das' + str(categorias))
        return redirect(url_for('trivia.html.j2', questoes_disponiveis = questoes_disponiveis, form = form, users = getStandings()))

@app.route('/ranking')
@login_required
def ranking():
    usuarios = Usuario.query.order_by(Usuario.recorde.desc())
    return render_template('ranking.html.j2', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
