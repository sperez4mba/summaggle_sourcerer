import os
from unittest import TestCase, mock
from mongoengine import connect
import json

from sourcerer import app
from sourcerer.tasks import cse_search_task

GOOGLE_CSE_MOCK_RESPONSE_FILEPATH = os.path.abspath(
    './tests/support/google_cse_mock_response.json'
)


class TestTasks(TestCase):
    def test_(self):
        cse_mock_json = None
        with open(GOOGLE_CSE_MOCK_RESPONSE_FILEPATH, 'r') as fd:
            cse_mock_json = fd.read()
        cse_mock_resp_dict = json.loads(cse_mock_json)

        search_terms = 'nodejs video streaming server'

        with mock.patch(
            'sourcerer.tasks.get_cse_results'
        ) as get_cse_results_mock:
            get_cse_results_mock.return_value = cse_mock_resp_dict

            cse_search_task(search_terms)
