from flask_wtf import FlaskForm as BaseForm
from wtforms import TextField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrarForm(BaseForm):
	nome = StringField(
		'nome',
		validators=[DataRequired()]
	)
	usuario = StringField(
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
	usuario = StringField('usuario', validators=[DataRequired()])
	senha = PasswordField('senha', validators=[DataRequired()])

class EnviarForm(BaseForm):
	questao = StringField('questao', validators=[DataRequired()])
	opcao1 = StringField('opcao1', validators=[DataRequired()])
	opcao2 = StringField('opcao2', validators=[DataRequired()])
	opcao3 = StringField('opcao3', validators=[DataRequired()])
	opcao4 = StringField('opcao4', validators=[DataRequired()])
	resposta = SelectField(
		'resposta',
		choices=[('opcao1', 'A'), ('opcao2', 'B'), ('opcao3', 'C'), ('opcao4', 'D')],
		validators=[DataRequired()]
	)
	categoria = SelectField(
		'categoria',
		choices=[('enem', 'ENEM'), ('cfoav','CFOAV'), ('detran','DETRAN')],
		validators=[DataRequired()]
	)

class QuizForm(BaseForm):
	resposta_escolhida = SelectField(
		'resposta_escolhida',
		choices=[('opcao1', 'A'), ('opcao2', 'B'), ('opcao3', 'C'), ('opcao4', 'D')],
		validators=[DataRequired()]
	)
