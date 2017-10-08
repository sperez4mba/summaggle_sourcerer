from flask_script import Command

from sourcerer.services.google_cse import get_cse_results


class GetCSEResultsCommand(Command):
    def run(self):
        get_cse_results()
