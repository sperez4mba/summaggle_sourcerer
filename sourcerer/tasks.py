# -*- coding: utf-8 -*-
import sys
import requests
from urllib.parse import urlparse
import datetime as dt

from sourcerer import app, celery_app, logger
from sourcerer.services.google_custom_search_engine import \
    get_search_engine_results
from sourcerer.models import *
from sourcerer.scrapers.stackoverflow import scrape_page


@celery_app.task
def search_task(terms, source='google'):
    try:
        logger.info("task called {}".format(terms))
        if source == 'google':
            results = get_search_engine_results(terms)
            urls = []
            for i in results['items']:
                urls.append(
                    Url(
                        url=i['link']
                    ).save()
                )
            search_term_list = terms.split(" ")
            if is_worth_storing_search_results():
                is_ = InitialSearch(
                    source=source,
                    result_urls=urls,
                    search_terms=search_term_list
                )
                is_.save()
    except Exception as e:
        logger.error("search_task: Caught "
                     "error {}".format(e))


def is_worth_storing_search_results():
    return True


def check_if_search_is_similar_to_existing_one():
    pass


@celery_app.task
def scrape_unscraped_urls_and_store_answers_task():
    try:
        all_urls = Url.objects.all()
        logger.info("scrape_unscraped_urls_and_store_answers_task: {}".format(len(all_urls)))
        for url in all_urls:
            if url.url_last_scraped_at:
                logger.info("scrape_unscraped_urls_and_store_answers_task: "
                            "Url {} was scraped not long ago, "
                            "skip it".format(
                                url.to_json()
                            ))
                continue

            if has_stackoverflow_domain(url.url):
                answers = scrape_page(url.url)

                answer_objects = []
                # It's a Stackoverflow convention that the first element
                # of answers is the question so skip it
                for a in answers[1:]:
                    answer_objects.append(
                        Answer(
                            markup=a
                        )
                    )
                question_answers = QuestionAnswers(
                    question_markup=answers[0],
                    source=app.config['STACKOVERFLOW_STRING'],
                    answers=answer_objects
                )
                question_answers.save()

                url.url_last_scraped_at = get_now()
                url.save()
            else:
                logger.info("scrape_unscraped_urls_and_store_answers_task: "
                            "Url {} has none of the scrapable "
                            "domains".format(
                                url.to_json()
                            ))
    except Exception as e:
        logger.exception('traceback')
        logger.error("scrape_unscraped_urls_and_store_answers_task: "
                     "Caught error {}".format(e.to_dict()))


def get_now():
    return dt.datetime.now()


def has_stackoverflow_domain(url):
    parsed_uri = urlparse(url)
    domain = "{}://{}/".format(
        parsed_uri.scheme,
        parsed_uri.netloc
    )
    return domain.lower() == app.config['STACKOVERFLOW_DOMAIN_NAME']
