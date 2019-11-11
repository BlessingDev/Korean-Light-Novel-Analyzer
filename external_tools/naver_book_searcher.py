from urllib import parse, request
from bs4 import BeautifulSoup
import json

import nlp_module, datetime
from external_tools import crawler, searcher
from book_data import BookData


class NaverBookSearcher(searcher.Searcher) :
    def __init__(self) :
        # 기본 BookData 객체로 생성
        # 사용하기 전에 반드시 book 멤버를 assign할 것
        searcher.Searcher.__init__(self)
        self.f = None

    def _search_for_book(self, title, category=True) :
        self.book.searched_title = title
        client_id = "EiPxhHox870abSfDvZBR"
        client_pw = "RqJncUd4p1"
        enc_text = parse.quote(title)

        url = "https://openapi.naver.com/v1/search/book_adv.json?d_titl=" + enc_text
        if category :
            url += "&d_catg=100040050"
        req = request.Request(url)
        req.add_header("X-Naver-Client-Id", client_id)
        req.add_header("X-Naver-Client-Secret", client_pw)

        try:
            print("{} requested".format(url))
            response = request.urlopen(req)
        except:
            print("책 제목 {} 검색 불가".format(title))
            self.book.error_code = 1
            return None

        res_code = response.getcode()

        print("{}을 검색함".format(title))
        self.f.write("{}을 검색함\n".format(title))
        self.book.ori_title = title

        if (res_code == 200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
            self.f.write(response_body.decode('utf-8'))
            book_dict = json.loads(response_body.decode('utf-8'))

            if (len(book_dict['items']) >= 1):
                highest_accuracy = 0.0
                highest_i = 0
                i = 0
                while self.book.search_accuracy <= 0.8 and\
                    i < len(book_dict['items']) :
                    item = book_dict['items'][i]

                    temp_title = item['title']
                    temp_title = temp_title.replace('<b>', '').replace('</b>', '')
                    print("{} 검색됨".format(self.book.title))
                    self.f.write("{} 검색됨\n".format(self.book.title))
                    self.book.search_accuracy = nlp_module.search_accsuracy_examine(self.book.ori_title, temp_title)
                    print('정확도: {}'.format(self.book.search_accuracy))
                    self.f.write('정확도: {}\n'.format(self.book.search_accuracy))
                    if self.book.search_accuracy > highest_accuracy :
                        highest_accuracy = self.book.search_accuracy
                        highest_i = i
                        print("{} {}".format(highest_accuracy, highest_i))
                        self.f.write("highest_acc: {} index: {}\n".format(highest_accuracy, highest_i))

                    i += 1

                if highest_accuracy >= 0.3 :
                    self.book.search_accuracy = highest_accuracy
                    return book_dict['items'][highest_i]
                else :
                    self.book.search_accuracy = 0.0
                    return None
            else :
                print("{}에 대한 검색 결과 없음".format(title))
                self.f.write("{}에 대한 검색 결과 없음\n".format(title))
                self.book.error_code = 2
                self.book.search_accuracy = 0.0

                return None

    def _get_data_from_searched_item(self, book_item) :
        self.book.title = book_item['title']
        self.book.image_url = book_item['image']
        self.book.author = book_item['author']
        self.book.publisher = book_item['publisher']
        self.book.isbn = book_item['isbn']
        self.book.pubdate = book_item['pubdate']
        self.book.description = ''
        self.book.translator = ''

        link = book_item['link']
        self._crawl_description(link)

        self.book.title = self.book.title.replace('<b>', '').replace('</b>', '')

        print("검색된 책 제목: {}".format(self.book.title))
        self.f.write("검색된 책 제목: {}".format(self.book.title))

    def from_titles(self, title_list) :
        books = []

        for i, title in enumerate(title_list) :
            self.book = BookData()
            print("{}/{}".format(i, len(title_list)))
            self.from_title(title)
            books.append(self.book)

        return books


    def from_title(self, title) :
        self.book.ori_title = title

        print("최초 검색어 '{}'".format(title))
        try :
            self.f.write("최초 검색어 '{}'\n".format(title))
        except:
            print("error occured in writing")
            #while u'\ufeff' in title :
            #    title.replace(u'\ufeff', '')
            return None


        item = self._search_for_book(title)

        if (item is not None) :
            self._get_data_from_searched_item(item)
        else :
            titles = nlp_module.make_alterative_search_set(title)
            print("alternative set made {}".format(titles))
            self.f.write("alternative set made {}\n".format(titles))
            for temp in titles :
                item = self._search_for_book(temp)

                if not (item is None):
                    self._get_data_from_searched_item(item)

                    if self.book.search_accuracy >= 0.6 :
                        break

            if self.book.search_accuracy == 0 :
                item = self._search_for_book(self.book.ori_title, category=False)

                if not (item is None):
                    self._get_data_from_searched_item(item)

                if self.book.search_accuracy == 0:
                    self.book.error_code = 2
                    print("책 제목 {0}에 대한 검색 결과가 전혀 없음".format(title))
                    self.f.write("책 제목 {0}에 대한 검색 결과가 전혀 없음\n".format(title))

        self.book.ori_title = title
        self.f.write('\n\n')
        return self.book

    def _crawl_description(self, link):
        c = crawler.get_html(link)

        i = 0
        while c is None :
            i += 1
            c = crawler.get_html(link)
            print("{}회 재시도".format(i))

        soup = BeautifulSoup(c)

        for div in soup('div'):
            if 'class' in div.attrs and \
                    'book_info_inner' in div['class'] :
                for em in div('em'):
                    if em.get_text() == '역자':
                        #print('역자 있음')
                        self.book.translator = em.next_sibling.next_sibling.get_text()

            elif 'id' in div.attrs and \
                    (div['id'] == 'bookIntroContent' or div['id'] == 'pubReviewContent') :
                #print('description 있음')
                self.book.description = div('p')[0].get_text()

                self.book.description = (self.book.description.replace('\n', '').replace('\r', ''))
                self.book.description.replace('\\', '')


    def search_finished(self) :
        self.f.close()