import click

from sourcerer import app
from sourcerer.services.google_cse import get_cse_results
from sourcerer.scrapers.stackoverflow import scrape_page


@app.cli.command()
def get_cse_results_cmd():
    """Get CSE results"""
    get_cse_results()


@click.option('--url', default='', help='URL to be scraped')
@app.cli.command()
def scrape_page_cmd(url):
    """Scrape page given a URL"""
    scrape_page(url)
