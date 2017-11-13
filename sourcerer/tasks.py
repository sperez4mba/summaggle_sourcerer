# -*- coding: utf-8 -*-
import sys
import requests
from urllib.parse import urlparse
import datetime as dt

from sourcerer import app, celery_app, logger
from sourcerer.services.google_cse import get_cse_results
from sourcerer.models import *
from sourcerer.scrapers.stackoverflow import scrape_page


@celery_app.task
def cse_search_task(search_terms):
    try:
        logger.info("task called {}".format(search_terms))
        results = get_cse_results(search_terms)
        urls = []
        for i in results['items']:
            urls.append(i['link'])
        search_term_list = search_terms.split(" ")
        if is_worth_storing_search_results():
            is_ = InitialSearch(
                source='google',
                result_urls=urls,
                search_terms=search_term_list
            )
            is_.save()
            logger.info(is_.to_json())
    except Exception as e:
        logger.error("cse_search_task: Caught "
                     "error {}".format(e))


def is_worth_storing_search_results():
    return True


def check_if_search_is_similar_to_existing_one():
    pass


@celery_app.task
def scrape_unscraped_urls_and_store_answers_task():
    try:
        all_initial_searches = InitialSearch.objects.all()
        for initial_search in all_initial_searches:
            urls = initial_search.result_urls
            for url_index, url in enumerate(urls):
                if has_url_been_scraped_lately(initial_search.id, url_index, url):
                    logger.info("scrape_unscraped_urls_and_store_answers_task: "
                                "Url {} was scraped not long ago, "
                                "skip it".format(
                                    url
                                ))
                    continue

                if has_stackoverflow_domain(url):
                    answers = scrape_page(url)

                    answer_objects = []
                    # It's a Stackoverflow convention that the first element
                    # of answers is the question so skip it
                    for a in answers[1:]:
                        answer_objects.append(
                            Answer(
                                answer_markup=a
                            )
                        )
                    question_answers = QuestionAnswers(
                        question_markup=answers[0],
                        source=app.config['STACKOVERFLOW_STRING'],
                        answers=answer_objects
                    )
                    question_answers.save()

                    scrape_time = get_now()
                    search_to_url_to_question_answer = InitialSearchToUrlToQuestionAnswers(
                        initial_search=initial_search,
                        url_list_index=url_index,
                        url_string=url,
                        question_answers=question_answers,
                        url_last_scraped_at=scrape_time
                    )
                    search_to_url_to_question_answer.save()
                else:
                    logger.info("scrape_unscraped_urls_and_store_answers_task: "
                                "Url {} has none of the scrapable "
                                "domains".format(
                                    url
                                ))
    except Exception as e:
        logger.error("scrape_unscraped_urls_and_store_answers_task: "
                     "Caught error {}".format(e))


def get_now():
    return dt.datetime.now()


def has_url_been_scraped_lately(initial_search_id, url_index, url):
    return False


def has_stackoverflow_domain(url):
    parsed_uri = urlparse(url)
    domain = "{}://{}/".format(
        parsed_uri.scheme,
        parsed_uri.netloc
    )
    return domain.lower() == app.config['STACKOVERFLOW_DOMAIN_NAME']
