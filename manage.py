from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

from server import app, bd

app.config.from_object('config.DevelopmentConfig')
migrate = Migrate(app, bd)
manager = Manager(app)

manager.add_command('bd', MigrateCommand)

if __name__ == '__main__':
    manager.run()
