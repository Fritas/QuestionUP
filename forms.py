from flask_wtf import Form as BaseForm
from flask_wtf import FlaskForm as BaseForm
from wtforms import TextField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrarForm(BaseForm):
	nome = TextField(
		'nome',
		validators=[DataRequired()]
	)
	usuario = TextField(
		'usario',
		validators=[DataRequired(), Length(min=3, max=25)]
	)
	senha = PasswordField(
		'senha',
		validators=[DataRequired(), Length(min=3, max=25)]
	)
	confirmacao = PasswordField(
		'confirmacao',
		validators=[DataRequired(), EqualTo('senha', message='Senhas precisam ser iguais.')]
	)

class EntrarForm(BaseForm):
	usuario = TextField('usuario', validators=[DataRequired()])
	senha = PasswordField('senha', validators=[DataRequired()])

class EnviarForm(BaseForm):
	questao = TextField('questao', validators=[DataRequired()])
	opcao1 = TextField('opcao1', validators=[DataRequired()])
	opcao2 = TextField('opcao2', validators=[DataRequired()])
	opcao3 = TextField('opcao3', validators=[DataRequired()])
	opcao4 = TextField('opcao4', validators=[DataRequired()])
	resposta = SelectField(
		'resposta',
		choices=[('opcao1', 'A'), ('opcao2', 'B'), ('opcao3', 'C'), ('opcao4', 'D')],
		validators=[DataRequired()]
	)
	categoria = SelectField(
		'categoria',
		choices=[('enem', 'Enem')],
		validators=[DataRequired()]
	)

class QuizForm(BaseForm):
	resposta_escolhida = SelectField(
		'resposta_escolhida',
		choices=[('opcao1', 'A'), ('opcao2', 'B'), ('opcao3', 'C'), ('opcao4', 'D')],
		validators=[DataRequired()]
	)
