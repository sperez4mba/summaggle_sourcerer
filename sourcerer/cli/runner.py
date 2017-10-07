from flask_script import Manager

from sourcerer import app

manager = Manager(app)


def main():
    #manager.add_command('send_message', SendMessageCommand())
    manager.run()
