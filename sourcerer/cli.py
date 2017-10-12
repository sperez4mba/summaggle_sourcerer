import click

from sourcerer import app
from sourcerer.services.google_cse import get_cse_results
from sourcerer.scrapers.stackoverflow import scrape_page
from sourcerer.models.mongo import QuestionAnswers


@app.cli.command()
def get_cse_results_cmd():
    """Get CSE results"""
    get_cse_results()


@click.option('--url', default='', help='URL to be scraped')
@app.cli.command()
def scrape_page_cmd(url):
    """Scrape page given a URL"""
    scrape_page(url)


@app.cli.command()
def prun():
    """Run flask server"""
    app.run(host='0.0.0.0')


@app.cli.command()
def create_test_answer_object_cmd():
    """Create a test QuestionAnswers object in mongo db"""
    qa = QuestionAnswers(
        question_markup='<div class="post-text" itemprop="text">\n </div>\n',
        source='test'
    )
    qa.save()
