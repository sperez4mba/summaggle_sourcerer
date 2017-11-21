from unittest import TestCase
import json

from sourcerer import app
from sourcerer.models import Answer


class TestAnswers(TestCase):
    def test_404_when_answer_object_doesnt_exist(self):
        with app.test_client() as c:
            resp = c.get('/api/v1/answers/fake_id')
            self.assertEqual(404, resp.status_code)

    def test_200_when_answer_object_exists(self):
        expected_answer = Answer(markup='<div>some markup</div>').save()
        expected_answer_object_id = str(expected_answer.id)

        with app.test_client() as c:
            uri = "/api/v1/answers/{}".format(expected_answer_object_id)
            resp = c.get(uri)
            self.assertEqual(200, resp.status_code)
            data = json.loads(resp.data.decode('utf-8'))
            self.assertEqual(
                expected_answer_object_id,
                data['_id']['$oid']
            )
