from flask_script import Manager

from sourcerer import app
from sourcerer.cli.cli import GetCSEResultsCommand

manager = Manager(app)


def main():
    manager.add_command('get_cse_results', GetCSEResultsCommand())
    manager.run()
