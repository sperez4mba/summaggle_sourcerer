import os
from unittest import TestCase, mock
from mongoengine import connect
import json
import datetime as dt

from sourcerer import app
from sourcerer.tasks import search_task, \
    scrape_unscraped_urls_and_store_answers_task
from sourcerer.models import InitialSearch, Url, QuestionAnswers

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

        expected_urls = [
            'https://medium.com/@daspinola/video-stream-with-node-js-and-html5-320b3191a6b6',
            'https://stackoverflow.com/questions/24976123/streaming-a-video-file-to-an-html5-video-player-with-node-js-so-that-the-video-c',
            'https://stackoverflow.com/questions/42803724/live-video-stream-on-a-node-js-server',
            'https://www.quora.com/How-can-I-implement-a-video-streaming-server-using-Node-JS',
            'https://www.quora.com/How-do-you-build-a-video-streaming-service-on-Node-js-servers-like-at-Netflix',
            'https://www.quora.com/How-do-I-learn-to-stream-live-video-with-Node-js',
            'https://stackoverflow.com/questions/21921790/best-approach-to-real-time-http-streaming-to-html5-video-client',
            'https://stackoverflow.com/questions/4360060/video-streaming-with-html-5-via-node-js',
            'https://stackoverflow.com/questions/31792198/high-performance-video-file-server-in-nodejs',
            'https://stackoverflow.com/questions/45797818/how-to-create-node-server-that-receiving-video-stream-and-save-the-stream-as-vid'
        ]

        with mock.patch(
            'sourcerer.tasks.get_search_engine_results'
        ) as get_cse_results_mock:
            get_cse_results_mock.return_value = cse_mock_resp_dict

            search_task(search_terms)

        all_initial_searches = InitialSearch.objects.all()
        self.assertEqual(1, len(all_initial_searches))
        urls = all_initial_searches[0].result_urls
        self.assertEqual(len(expected_urls), len(urls))
        for url in urls:
            self.assertTrue(url.url in expected_urls)

    def test_unscraped_url_has_no_stackoverflow_domain(self):
        result_url_1 = 'http://something.com'
        url_1 = Url(url=result_url_1).save()
        initial_search = InitialSearch(
            source='google',
            result_urls=[url_1],
            search_terms=['something', 'else']
        )
        initial_search.save()

        with mock.patch(
                'sourcerer.tasks.scrape_page'
        ) as scrape_page_mock:
            scrape_unscraped_urls_and_store_answers_task()

            assert scrape_page_mock.call_count == 0

    def test_unscraped_url_has_stackoverflow_domain(self):
        result_url_1 = 'https://stackoverflow.com/questions/123/the-question'
        result_url_2 = 'https://stackoverflow.com/questions/321/another-question'
        url_1 = Url(url=result_url_1).save()
        url_2 = Url(url=result_url_2).save()
        initial_search = InitialSearch(
            source='google',
            result_urls=[url_1, url_2],
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
            question_answers[0].source_url.source
        )
        self.assertEqual(
            result_url_1,
            question_answers[0].source_url.url
        )
        self.assertEqual(
            len(expected_answers_list_1) - 1,
            len(question_answers[0].answers)
        )
        for a in question_answers[0].answers:
            self.assertTrue(
                a.markup in expected_answers_list_1
            )
        # Assertions related to result_url_2
        self.assertEqual(
            expected_answers_list_2[0],
            question_answers[1].question_markup
        )
        self.assertEqual(
            app.config['STACKOVERFLOW_STRING'],
            question_answers[1].source_url.source
        )
        self.assertEqual(
            result_url_2,
            question_answers[1].source_url.url
        )
        self.assertEqual(
            len(expected_answers_list_2) - 1,
            len(question_answers[1].answers)
        )
        for a in question_answers[1].answers:
            self.assertTrue(
                a.markup in expected_answers_list_2
            )
