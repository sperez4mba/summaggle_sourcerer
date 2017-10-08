from bs4 import BeautifulSoup


with open('/Users/sergioperezaranda/Mycodestore/knowledge_summarization_tool/scraped_stackoverflow_question_24976123.txt','r') as fd:
    answers_page = fd.read()

tree = BeautifulSoup(answers_page, 'lxml')
#tree.find_all('td',{'class':'answercell'})[1]

answers_html = tree.find_all('div', {'class': 'post-text'})
import bpdb;bpdb.set_trace()
