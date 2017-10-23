# -*- coding: utf-8 -*-
import sys

from sourcerer import celery_app, logger
from sourcerer.services.google_cse import get_cse_results
from sourcerer.models.mongo import InitialSearch


@celery_app.task
def cse_search_task(search_terms):
    try:
        logger.info("task called {}".format(search_terms))
        results = get_cse_results(search_terms)
        links = []
        for i in results['items']:
            links.append(i['link'])
        search_term_list = search_terms.split(" ")
        if is_worth_storing_search_results():
            is_ = InitialSearch(
                source='google',
                result_links=links,
                search_terms=search_term_list
            )
            is_.save()
            logger.info(is_.to_json())
    except Exception as e:
        logger.error("cse_search_task: Caught "
                     "error {}".format(e))
        logger.exception('traceback')


def is_worth_storing_search_results():
    return True


def check_if_search_is_similar_to_existing_one():
    pass