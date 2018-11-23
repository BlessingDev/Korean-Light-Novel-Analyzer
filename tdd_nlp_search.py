import unittest
from book_data import BookData
from external_tools import naver_book_searcher as nb
import nlp_module

class NaverSearchTest(unittest.TestCase) :

    def test_normal_set1(self) :
        book = BookData()
        sc = nb.NaverBookSearcher()
        sc.book = book
        sc.from_title('바보와 시험과 소환수 10')
        self.assertEqual("바보와 시험과 소환수 10", book.title)

    def test_extraordinary_set1(self) :
        book = BookData()
        sc = nb.NaverBookSearcher()
        sc.book = book
        sc.from_title('시큐브 11')
        self.assertEqual("C3 시큐브 11 (Extreme Novel)", book.title)

    def test_extraordinary_set2(self) :
        book = BookData()
        sc = nb.NaverBookSearcher()
        sc.book = book
        sc.from_title('너 또한, 위장연인(오타쿠)이라 할지라도 1 上')
        self.assertEqual("C3 시큐브 11 (Extreme Novel)", book.title)

class NLPTest(unittest.TestCase) :

    def test_title_preprocessing1(self) :
        titles = nlp_module.preprocess_title('빙결경계의 에덴 1, 2')
        self.assertEqual(titles.__str__(), "['빙결경계의 에덴 1', '빙결경계의 에덴 2']")


if __name__ == "__main__" :
    unittest.main()