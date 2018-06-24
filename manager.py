#encoding:utf-8
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db
from app import app

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('db', MigrateCommand)
manager.add_command('runServer', Server(host='localhost', port=5000))
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()