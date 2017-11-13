import os
from unittest import TestCase, mock
from mongoengine import connect
import json
import datetime as dt

from sourcerer import app
from sourcerer.tasks import cse_search_task, \
    scrape_unscraped_urls_and_store_answers_task
from sourcerer.models import InitialSearch, QuestionAnswers, \
    InitialSearchToUrlToQuestionAnswers

GOOGLE_CSE_MOCK_RESPONSE_FILEPATH = os.path.abspath(
    './tests/support/google_cse_mock_response.json'
)


class TestTasks(TestCase):
    def tearDown(self):
        db = InitialSearch._get_db()
        all_collection_names = db.collection_names()
        [db.drop_collection(cn) for cn in all_collection_names]

    def test_cse_search_task(self):
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

        all_initial_searches = InitialSearch.objects.all()
        self.assertEqual(1, len(all_initial_searches))

    def test_unscraped_url_has_no_stackoverflow_domain(self):
        is_ = InitialSearch(
            source='google',
            result_urls=['http://something.com'],
            search_terms=['something', 'else']
        )
        is_.save()

        with mock.patch(
                'sourcerer.tasks.scrape_page'
        ) as scrape_page_mock:
            scrape_unscraped_urls_and_store_answers_task()

            assert scrape_page_mock.call_count == 0

    def test_unscraped_url_has_stackoverflow_domain(self):
        result_url_1 = 'https://stackoverflow.com/questions/123/the-question'
        result_url_2 = 'https://stackoverflow.com/questions/321/another-question'
        initial_search = InitialSearch(
            source='google',
            result_urls=[result_url_1, result_url_2],
            search_terms=['a', 'question', 'about', 'something']
        )
        initial_search.save()

        expected_answers_list_1 = [
            '<div class="post-text" itemprop="text"><h2>Tl;Dr - The Question:</h2><p>This is the question</p></div>',
            '<div class="post-text" itemprop="text"><p>Line of answer 1</p><p>Another line for answer 1</p></div>',
            '<div class="post-text" itemprop="text"><p>Line of answer 2</p><p>Another line for answer 2</p></div>'
        ]
        expected_answers_list_2 = [
            '<div class="post-text" itemprop="text"><h2>Tl;Dr - Another Question:</h2><p>This is another question</p></div>',
            '<div class="post-text" itemprop="text"><p>Line of answer 1</p><p>Another line for answer 1</p></div>',
            '<div class="post-text" itemprop="text"><p>Line of answer 2</p><p>Another line for answer 2</p></div>'
        ]

        expected_scrape_time = dt.datetime.now()

        with mock.patch(
                'sourcerer.tasks.scrape_page'
        ) as scrape_page_mock:
            with mock.patch(
                    'sourcerer.tasks.get_now'
            ) as get_now_mock:
                scrape_page_mock.side_effect = [
                    expected_answers_list_1,
                    expected_answers_list_2
                ]
                get_now_mock.return_value = expected_scrape_time
                scrape_unscraped_urls_and_store_answers_task()

        question_answers = QuestionAnswers.objects.all()
        self.assertEqual(2, len(question_answers))
        # Assertions related to result_url_1
        self.assertEqual(
            expected_answers_list_1[0],
            question_answers[0].question_markup
        )
        self.assertEqual(
            app.config['STACKOVERFLOW_STRING'],
            question_answers[0].source
        )
        self.assertEqual(
            len(expected_answers_list_1) - 1,
            len(question_answers[0].answers)
        )
        for a in question_answers[0].answers:
            self.assertTrue(
                a.answer_markup in expected_answers_list_1
            )
        search_to_url_to_question_answers = InitialSearchToUrlToQuestionAnswers.objects.all()
        self.assertEqual(2, len(search_to_url_to_question_answers))
        self.assertEqual(
            initial_search,
            search_to_url_to_question_answers[0].initial_search
        )
        self.assertEqual(
            question_answers[0],
            search_to_url_to_question_answers[0].question_answers
        )
        self.assertEqual(
            0,
            search_to_url_to_question_answers[0].url_list_index
        )
        self.assertEqual(
            result_url_1,
            search_to_url_to_question_answers[0].url_string
        )
        self.assertEqual(
            expected_scrape_time.strftime("%H:%M:%S"),
            search_to_url_to_question_answers[0].url_last_scraped_at.strftime("%H:%M:%S")
        )
        # Assertions related to result_url_2
        self.assertEqual(
            expected_answers_list_2[0],
            question_answers[1].question_markup
        )
        self.assertEqual(
            app.config['STACKOVERFLOW_STRING'],
            question_answers[1].source
        )
        self.assertEqual(
            len(expected_answers_list_2) - 1,
            len(question_answers[1].answers)
        )
        for a in question_answers[1].answers:
            self.assertTrue(
                a.answer_markup in expected_answers_list_2
            )
        search_to_url_to_question_answers = InitialSearchToUrlToQuestionAnswers.objects.all()
        self.assertEqual(
            initial_search,
            search_to_url_to_question_answers[1].initial_search
        )
        self.assertEqual(
            question_answers[1],
            search_to_url_to_question_answers[1].question_answers
        )
        self.assertEqual(
            1,
            search_to_url_to_question_answers[1].url_list_index
        )
        self.assertEqual(
            result_url_2,
            search_to_url_to_question_answers[1].url_string
        )
        self.assertEqual(
            expected_scrape_time.strftime("%H:%M:%S"),
            search_to_url_to_question_answers[1].url_last_scraped_at.strftime("%H:%M:%S")
        )
