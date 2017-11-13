# -*- coding: utf-8 -*-
from mongoengine import *


class InitialSearch(Document):
    source = StringField(max_length=50, required=True)
    result_urls = ListField(StringField(max_length=500))
    search_terms = ListField(StringField(max_length=50))


class Answer(EmbeddedDocument):
    answer_markup = StringField(max_length=10000, required=True)


class QuestionAnswers(Document):
    question_markup = StringField(max_length=10000, required=True)
    source = StringField(max_length=50, required=True)
    tags = ListField(StringField(max_length=50))
    answers = EmbeddedDocumentListField(Answer)


class InitialSearchToUrlToQuestionAnswers(Document):
    initial_search = ReferenceField(InitialSearch)
    url_list_index = IntField()
    url_string = StringField(max_length=500)
    question_answers = ReferenceField(QuestionAnswers)
    url_last_scraped_at = DateTimeField()
