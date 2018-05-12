import requests
from external_tools import namu_wiki_crawler

def get_html(url):
    html = ""
    resp = ""
    try:
        resp = requests.get(url)
    except:
        print("URL {}에 접속 불가".format(url))
        return None

    if resp.status_code == 200:
        html = resp.text

    return html

class crawler :
    def __init__(self) :
        pass

    @classmethod
    def get_instance(cls) :
        return namu_wiki_crawler.NamuNovelCrawler() # you should modify here to change crawler

    def crawl_certain_month_novel(self, url, date) :
        '''
        abstract method
        :param url: 해당 발매 페이지의 url
        :param date: log를 위한 날짜 string
        :return: title list
        '''
        print("you have to override this function!")

    def crawl_whole_korean_novel(self) :
        '''

        :return: BookStorer instance
        '''
        print("you have to override this function!")

    def crawl_certain_period(self, start_time, end_time):
        '''

        :param start_time:
        :param end_time:
        :return: title list
        '''
        print("you have to override this function!")