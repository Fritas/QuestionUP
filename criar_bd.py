from sqlalchemy import create_engine
from models import *

try:
    sql = create_engine('mysql://root:alunoifc@localhost:3306')
    sql.execute('CREATE DATABASE IF NOT EXISTS questionup')
    sql.execute('USE questionup')

    bd.create_all()
    bd.session.add(Usuario('bla','bla','bla',9,0))
    bd.session.add(Usuario('ble','ble','ble',0,1))
    bd.session.commit()
    print('O banco de dados foi montado!')
except Exception as erro:
    print('Algo ocorreu e não foi possível montar o banco de dados! \nErro: ' + str(erro))