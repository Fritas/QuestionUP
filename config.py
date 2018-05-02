class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'algo_secreto'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/questionup'
    WTF_CSRF_SECRET_KEY = 'algo_secreto'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
