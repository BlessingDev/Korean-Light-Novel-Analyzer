from abc import *
from book_data import BookData

class Searcher :
    '''
    this is an abstract base class for all searcher
    '''

    def __init__(self) :
        # you shoud assign self.book member variable to set BookData class
        self.book = BookData()

    @abstractmethod
    def from_titles(self, title_list):
        '''
        타이틀의 리스트를 인자로 받아 book_data 리스트를 반환하는 객체
        :param title_list: 
        :return: [book_data]
        '''

    @abstractmethod
    def from_title(self, title) :
        '''
        1. assign BookData.ori_title
        2. search books
        3. assign search accuracy
        4. finish searching
        :param title: a title to search from
        :return: self.book
        '''