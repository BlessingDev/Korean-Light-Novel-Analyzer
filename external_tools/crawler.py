import requests
from abc import *

def get_html(url):
    html = ""
    try:
        resp = requests.get(url)
    except:
        print("URL {}에 접속 불가".format(url))
        return None

    if resp.status_code == 200:
        html = resp.text

    return html

class Crawler :
    def __init__(self) :
        pass

    @abstractmethod
    def crawl_certain_month_novel(self, url, date) :
        '''
        abstract method
        :param url: 해당 발매 페이지의 url
        :param date: log를 위한 날짜 string
        :return: title list
        '''
        print("you have to override this function!")

    @abstractmethod
    def crawl_whole_korean_novel(self) :
        '''

        :return: BookStorer instance
        '''
        print("you have to override this function!")

    @abstractmethod
    def crawl_selected_month(self, ym_list, page_dic):
        '''
        abstract method
        :param ym_list:
        :param page_dic:
        :return:
        '''

        print("you have to override this function!")