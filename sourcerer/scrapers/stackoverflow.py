# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


def scrape_page(url):
    answers_page = requests.get(url)
    tree = BeautifulSoup(answers_page.content, 'html.parser')
    answers_html = tree.find_all('div', {'class': 'post-text'})
    return [str(ah) for ah in answers_html]
