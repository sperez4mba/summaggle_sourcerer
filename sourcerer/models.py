# -*- coding: utf-8 -*-
from mongoengine import *


class Url(Document):
    url = StringField(max_length=500)
    url_last_scraped_at = DateTimeField(default=None)


class InitialSearch(Document):
    source = StringField(max_length=50, required=True)
    result_urls = ListField(ReferenceField(Url))
    search_terms = ListField(StringField(max_length=50))


class Answer(EmbeddedDocument):
    markup = StringField(max_length=10000, required=True)


class QuestionAnswers(Document):
    question_markup = StringField(max_length=10000, required=True)
    source = StringField(max_length=50, required=True)
    tags = ListField(StringField(max_length=50))
    answers = EmbeddedDocumentListField(Answer)
