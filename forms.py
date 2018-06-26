from flask_wtf import FlaskForm as BaseForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Lenght

class FormLogin(BaseForm):
    usuario = StringField('usuario', validators=[DataRequired()])

class FormEnvio(BaseForm):
    questao = StringField('questao', validators=[DataRequired()])
    opcao1 = StringField('opcao1', validators=[DataRequired()])
    opcao2 = StringField('opcao2', validators=[DataRequired()])
    opcao3 = StringField('opcao3', validators=[DataRequired()])
    opcao4 = StringField('opcao4', validators=[DataRequired()])
    opcao5 = StringField('opcao5', validators=[DataRequired()])
    resposta = SelectField(
        'resposta',
        choices=[('enem','ENEM')],
        validators=[DataRequired()]
    )

class FormJogo(BaseForm):
    tentativa_resposta = SelectField(
        'tentativa_resposta',
        choices=[('opcao1','A'),('opcao2','B'),('opcao3','C'),('opcao4','D'),('opcao5','E')],
        validators=[DataRequired()]
    )