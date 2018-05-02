from sqlalchemy import create_engine
from models import *

try:
    sql = create_engine('mysql://root:@localhost:3306')
    sql.execute('CREATE DATABASE IF NOT EXISTS questionup')
    sql.execute('USE questionup')

    bd.create_all()
    bd.session.add(Usuario('bla','bla','bla',0))
    bd.session.commit()
    print('O banco de dados foi montado!')
except:
    print('Algo ocorreu e não foi possível montar o banco de dados!')