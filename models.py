from server import bd

class Usuario(bd.Model):
	__tablename__= 'usuario'

	id = bd.Column(bd.Integer, primary_key=True)
	nome = bd.Column(bd.String(20), nullable=False)
	usuario = bd.Column(bd.String(20), nullable=False)
	senha = bd.Column(bd.String(20), nullable=False)
	recorde = bd.Column(bd.Integer, nullable=False)
	perm_acesso = bd.Column(bd.Integer, nullable=False)
	respondidas = bd.Column(bd.PickleType)

	def __init__(self, nome, usuario, senha, recorde, perm_acesso):
		self.nome = nome
		self.usuario = usuario
		self.senha = senha
		self.recorde = recorde
		self.perm_acesso = perm_acesso

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __repr__(self):
		return "<O usuário é '%s'" %(self.usuario)

class Questoes(bd.Model):
	__tablename__ = 'questao'

	questao = bd.Column(bd.String(500), nullable=False)
	opcao1 = bd.Column(bd.String(250), nullable=False)
	opcao2 = bd.Column(bd.String(250), nullable=False)
	opcao3 = bd.Column(bd.String(250), nullable=False)
	opcao4 = bd.Column(bd.String(250), nullable=False)
	resposta = bd.Column(bd.String(250), nullable=False)
	id_criador = bd.Column(bd.String(20), nullable=False)
	id_questao = bd.Column(bd.Integer, primary_key=True)
	categoria = bd.Column(bd.String(20), nullable=False)

	def __init__(self, questao, opcao1, opcao2, opcao3, opcao4, resposta, id_criador, categoria):
		self.questao = questao
		self.opcao1 = opcao1
		self.opcao2 = opcao2
		self.opcao3 = opcao3
		self.opcao4 = opcao4
		self.resposta = resposta
		self.id_criador = id_criador
		self.categoria = categoria

	def __repr__(self):
		return "<ID da questão é %s e o id do criador é %s" %(self.id_questao, self.id_criador)
