# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


def scrape_page(url):
    answers_page = requests.get(url)

    tree = BeautifulSoup(answers_page.content, 'html.parser')
    #tree.find_all('td',{'class':'answercell'})[1]

    answers_html = tree.find_all('div', {'class': 'post-text'})
