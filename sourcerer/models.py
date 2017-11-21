# -*- coding: utf-8 -*-
#from mongoengine import *
from sourcerer import db


class Url(db.Document):
    url = db.StringField(max_length=500, required=True)
    url_last_scraped_at = db.DateTimeField(default=None)
    source = db.StringField(max_length=50)


class InitialSearch(db.Document):
    result_urls = db.ListField(db.ReferenceField(Url))
    search_terms = db.ListField(db.StringField(max_length=50))
    source = db.StringField(max_length=50)


class Answer(db.Document):
    markup = db.StringField(max_length=10000, required=True)


class QuestionAnswers(db.Document):
    question_markup = db.StringField(max_length=10000, required=True)
    source_url = db.ReferenceField(Url)
    tags = db.ListField(db.StringField(max_length=50))
    answers = db.ListField(db.ReferenceField(Answer))
