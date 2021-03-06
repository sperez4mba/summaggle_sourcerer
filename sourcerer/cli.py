# -*- coding: utf-8 -*-
import click
from subprocess import call
import sys

from sourcerer import app
from sourcerer.services.google_custom_search_engine import get_search_engine_results
from sourcerer.scrapers.stackoverflow import scrape_page
from sourcerer.models import QuestionAnswers


@click.option('--search', default='', help='Search terms to be looked up through Google CSE')
@app.cli.command()
def get_search_engine_results_cmd(search):
    """Get Google Custom Search Engine results"""
    #SUMMAGGLE_SETTINGS=/Users/sergioperezaranda/Mycodestore/knowledge_summarization_tool/summaggle/summaggle_sourcerer/config/config-local.py ./manage get_cse_results_cmd --search "nodejs video streaming server"
    import pprint;pprint.pprint(get_search_engine_results(search))


@click.option('--url', default='', help='URL of SO to be scraped')
@app.cli.command()
def scrape_so_page_cmd(url):
    """Scrape question/answers SO page given a URL"""
    scrape_page(url)


@app.cli.command()
def prun():
    """Run flask server"""
    app.run(host='0.0.0.0', threaded=True)


@app.cli.command()
def create_test_answer_object_cmd():
    """Create a test QuestionAnswers object in mongo db"""
    qa = QuestionAnswers(
        question_markup='<div class="post-text" itemprop="text">\n </div>\n',
        source='test'
    )
    qa.save()


@app.cli.command()
def celery_worker_up():
    """Run celery worker"""
    call(["celery", "worker", "-A", "sourcerer.celery_app", "--loglevel=debug"])


@app.cli.command()
def celery_beat_up():
    """Run celery beat"""
    INTERVAL_STRING = "--max-interval={}".format(
        str(
            app.config['CELERY_BEAT_MAX_INTERVAL_IN_SECS']
        )
    )
    call(["celery", "beat", "-A", "sourcerer.celery_app", "--loglevel=debug", INTERVAL_STRING])
