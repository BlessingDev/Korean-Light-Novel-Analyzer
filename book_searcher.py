import datetime
import BookData

from external_tools import NaverBookSearcher

class BookSearcher :
    '''
    you should inherit this BookSearcher class to define your own searcher
    '''
    def __init__(self) :
        pass

    @classmethod
    def get_instance(cls) :
        # you should modify here to change searcher
        return NaverBookSearcher.NaverBookSearcher()

    def from_title(self, title):
        '''
        you should define from_title method because I call from_title method in BookStorer class
        :param title:
        :return:
        '''
        print("you have called ABC's from_title")
