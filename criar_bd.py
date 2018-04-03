from server import bd
from models import *

bd.create_all()
bd.session.add(Usuario('bla','bla','bla',0))
bd.session.commit()
