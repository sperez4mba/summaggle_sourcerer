# -*- coding: utf-8 -*-
import pprint
from googleapiclient.discovery import build

from sourcerer import app


def get_search_engine_results(search_terms):
    service = build('customsearch', 'v1', developerKey=app.config['CSE_API_KEY'])

    # Search terms like i.e.
    # nodejs video streaming server
    res = service.cse().list(
        cx=app.config['CSE_CONTEXT'],
        q=search_terms
    ).execute()
    return res
