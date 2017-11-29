from collections import defaultdict
from urllib import parse, request
from bs4 import BeautifulSoup
import json, pathlib, datetime, random, json_file

import crawler, nlp_module


class book_storer:
    def __init__(self):
        self.book_list = list()
        self.date_to_book = defaultdict(list)
        self.training_set = None

    def import_data(self) :
        self.book_list = list()
        self.date_to_book = defaultdict(list)

        book_path = pathlib.Path('book_data.json')
        if book_path.exists() :
            temp = book_path.read_text(encoding='utf-16')
            book_list = json.loads(temp, strict=False)

            for book in book_list :
                #print(type(book))
                new_book = book_data()
                new_book.from_json_dict(book)
                self.book_list.append(new_book)

        book_path = pathlib.Path('date_to_book.json')
        if book_path.exists() :
            temp = book_path.read_text(encoding='utf-16')
            book_dict = json.loads(temp, strict=False)

            for key in book_dict.keys():
                new_list = list()
                book_list = book_dict[key]
                for book in book_list :
                    #print(type(book))
                    new_book = book_data()
                    new_book.from_json_dict(book)
                    new_list.append(new_book)

                self.date_to_book[key] = new_list

        tra_path = pathlib.Path("baseyan_set.json")
        if tra_path.exists() :
            temp = tra_path.read_text(encoding='utf-16')
            book_dict = json.loads(temp, strict=False)

            for dic in book_dict :
                new_book = book_data()
                new_book.from_json_dict(dic["book"])
                dic["book"] = new_book

            self.training_set = book_dict

    def add_by_tl_td(self, title_list, title_to_date):
        self.date_to_book = defaultdict(list)

        for title in title_list :
            book = book_data()
            book.from_title(title)
            self.book_list.append(book)
            self.date_to_book[title_to_date[book.ori_title]].append(book)

    def export_data(self) :
        book_p = pathlib.Path('book_data.json')
        book_p.write_text(json_file.list_to_json(self.book_list, json_file.data_to_json), encoding='utf-16')

        dic_p = pathlib.Path('date_to_book.json')
        dic_p.write_text(json_file.dict_to_json(self.date_to_book, json_file.data_to_json), encoding='utf-16')

        #ran_p = pathlib.Path('baseyan_set.json')
        #ran_p.write_text(json_file.list_to_json(self.random_set, json_file.data_to_json), encoding='utf-16')

    def get_title_list(self) :
        return [x.title for x in self.book_list]

    def get_error_codes(self) :
        return [x.error_code for x in self.book_list]

    def add_book(self, book) :
        self.book_list.append(book)
        self.date_to_book[book.get_pub_year_month()].append(book)

    def get_ordinary_book(self) :
        return [x for x in self.book_list if x.error_code == 0]

    def renew_accuracy(self) :
        for book in self.get_ordinary_book() :
            book.search_accuracy = nlp_module.search_accsuracy_examine(book)

    def make_random_set(self, num) :
        ordinary_set = [{'book':x, 'genre':[]} for x in self.get_ordinary_book() if x.search_accuracy >= 0.6]
        if num < len(ordinary_set) :
            self.random_set = random.sample(ordinary_set, num)

        return self.random_set

    def classify_book_genre(self, g) :
        for book in self.book_list :
            genres = []
            if book.error_code == 0 :
                genre_prob = g.classify(book)

                for genre, prob in genre_prob :
                    if prob >= 0.0005 :
                        genres.append(genre)

                book.genre = genres
                print(genres)



class book_data:
    def __init__(self) :
        self.ori_title = ""
        self.searched_title = ""
        self.title = ""
        self.author = ""
        self.translator = ""
        self.image_url = ""
        self.publisher = ""
        self.isbn = ""
        self.description = ""
        self.pubdate = ""
        self.error_code = 0
        self.search_accuracy = 0.0
        self.genre = []

    def search_for_book(self, title, category = True) :
        self.searched_title = title
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
            self.error_code = 1
            return None

        res_code = response.getcode()
        print("{}을 검색함".format(title))
        self.ori_title = title

        if (res_code == 200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
            book_dict = json.loads(response_body.decode('utf-8'))

            if (len(book_dict['items']) >= 1):
                highest_accuracy = 0.0
                highest_i = 0
                i = 0
                while self.search_accuracy <= 0.8 and\
                    i < len(book_dict['items']) :
                    item = book_dict['items'][i]

                    self.title = item['title']
                    self.title = self.title.replace('<b>', '').replace('</b>', '')
                    print("{} 검색됨".format(self.title))
                    self.search_accuracy = nlp_module.search_accsuracy_examine(self)
                    print('정확도: {}'.format(self.search_accuracy))
                    if self.search_accuracy > highest_accuracy :
                        highest_accuracy = self.search_accuracy
                        highest_i = i
                        print("{} {}".format(highest_accuracy, highest_i))

                    i += 1

                if highest_accuracy >= 0.6 :
                    self.search_accuracy = highest_accuracy
                    return book_dict['items'][highest_i]
                else :
                    self.search_accuracy = 0.0
                    return None
            else :
                print("{}에 대한 검색 결과 없음".format(title))
                self.error_code = 2
                self.search_accuracy = 0.0
                return None

    def from_title(self, title) :
        self.ori_title = title

        print("최초 검색어 '{}'".format(title))

        item = self.search_for_book(title)

        if (item is not None) :
            self.title = item['title']
            self.image_url = item['image']
            self.author = item['author']
            self.publisher = item['publisher']
            self.isbn = item['isbn']
            self.pubdate = item['pubdate']
            self.description = ''
            self.translator = ''

            link = item['link']
            self.crawl_description(link)

            self.title = self.title.replace('<b>', '').replace('</b>', '')
            self.title.replace('\ufeff', '')
            self.image_url.replace('\ufeff', '')
            print("검색된 책 제목: {}".format(self.title))
        else :
            titles = nlp_module.make_alterative_search_set(title)
            print("alternative set made {}".format(titles))
            for temp in titles :
                item = self.search_for_book(temp)

                if not (item is None):
                    self.image_url = item['image']
                    self.author = item['author']
                    self.publisher = item['publisher']
                    self.isbn = item['isbn']
                    self.pubdate = item['pubdate']
                    self.description = ''
                    self.translator = ''

                    link = item['link']
                    self.crawl_description(link)

                    self.title = self.title.replace('<b>', '').replace('</b>', '')
                    self.title.replace('\ufeff', '')
                    self.image_url.replace('\ufeff', '')
                    print("검색된 책 제목: {}".format(self.title))

                    if self.search_accuracy >= 0.8 :
                        break

            if self.search_accuracy == 0 :
                item = self.search_for_book(self.ori_title, category=False)

                if not (item is None):
                    self.image_url = item['image']
                    self.author = item['author']
                    self.publisher = item['publisher']
                    self.isbn = item['isbn']
                    self.pubdate = item['pubdate']
                    self.description = ''
                    self.translator = ''

                    link = item['link']
                    self.crawl_description(link)

                    self.title = self.title.replace('<b>', '').replace('</b>', '')
                    self.title.replace('\ufeff', '')
                    self.image_url.replace('\ufeff', '')
                    print("검색된 책 제목: {}".format(self.title))

                if self.search_accuracy == 0:
                    self.error_code = 2
                    print("책 제목 {0}에 대한 검색 결과가 전혀 없음".format(title))

        self.ori_title = title
        return self

    def from_json_dict(self, dict) :
        self.ori_title = dict["ori title"]
        self.title = dict["title"]
        self.author = dict["author"]
        self.translator = dict["translator"]
        self.image_url = dict["image_url"]
        self.isbn = dict["isbn"]
        self.publisher = dict["publisher"]
        self.description = dict["description"]
        self.error_code = int(dict["error_code"])
        self.search_accuracy = dict["search_accuracy"]
        #self.genre = dict["genre"]

        return self

    def __str__(self):
        rex = 'title: {}\n' \
              'ori title: {}\n' \
              'author: {}\n' \
              'translator: {}\n' \
              'publisher: {}\n' \
              'description: {}' \
            .format(self.title, self.ori_title, self.author, self.translator, self.publisher, self.description)

        return rex

    def crawl_description(self, link):
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
                        self.translator = em.next_sibling.next_sibling.get_text()

            elif 'id' in div.attrs and \
                    (div['id'] == 'bookIntroContent' or div['id'] == 'pubReviewContent') :
                #print('description 있음')
                self.description = div('p')[0].get_text()

                self.description = (self.description.replace('\n', '').replace('\r', ''))

    def get_pub_year_month(self) :
        temp_date = datetime.datetime.strptime(self.pubdate, '%Y%m%d')
        return (temp_date.year.__str__() + "년 " + temp_date.month.__str__() + "월")
