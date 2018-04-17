from server import bd
from sqlalchemy import create_engine
from models import *

sql = create_engine('mysql://root:alunoifc@localhost:3306')
sql.execute('CREATE DATABASE IF NOT EXISTS questionup')
sql.execute('USE questionup')

bd.create_all()
bd.session.add(Usuario('bla','bla','bla',0))
bd.session.commit()
