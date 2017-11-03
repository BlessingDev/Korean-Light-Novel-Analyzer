from collections import defaultdict
from urllib import parse, request
from bs4 import BeautifulSoup
import json
import pathlib
import datetime

import crawler, nlp_module

def list_to_json(list, func):
    out_str = "["
    for val in list:
        out_str += func(val)
        out_str += ", "

    if len(out_str) > 2:
        out_str = out_str[:-2]

    out_str += "]"
    return out_str

def book_to_json(book) :
    book_dict = dict()
    book_dict["title"] = book.title
    book_dict["ori title"] = book.ori_title
    book_dict["author"] = book.author
    book_dict["translator"] = book.translator
    book_dict["image_url"] = book.image_url
    book_dict["publisher"] = book.publisher
    book_dict["description"] = book.description.replace('"', "'").replace('\n', '')
    book_dict["isbn"] = book.isbn
    book_dict["error_code"] = book.error_code
    book_dict["search_accuracy"] = book.search_accuracy

    return dict_to_json(book_dict, data_to_json)

def dict_to_json(dict, func) :
    out_str = "{"
    for key in dict.keys() :
        out_str += ('"' + key.__str__() + '"')
        out_str += ": "
        out_str += func(dict[key])
        out_str += ", "
    if len(out_str) > 2:
        out_str = out_str[:-2]

    out_str += "}"
    return out_str

def data_to_json(data) :
    if type(data) is str :
        return '"' + data + '"'
    elif type(data) is book_data :
        return book_to_json(data)
    elif type(data) is list :
        return list_to_json(data, data_to_json)
    elif type(data) is int or type(data) is float :
        return data.__str__()
    else :
        print("type은 {}".format(type(data)))
        return '""'


class book_storer:
    def __init__(self):
        self.book_list = list()
        self.date_to_book = defaultdict(list)

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

    def add_by_tl_td(self, title_list, title_to_date):
        self.date_to_book = defaultdict(list)

        for title in title_list :
            book = book_data()
            book.from_title(title)
            self.book_list.append(book)
            self.date_to_book[title_to_date[book.ori_title]].append(book)

    def export_data(self) :
        book_p = pathlib.Path('book_data.json')
        book_p.write_text(list_to_json(self.book_list, data_to_json), encoding='utf-16')

        dic_p = pathlib.Path('date_to_book.json')
        dic_p.write_text(dict_to_json(self.date_to_book, data_to_json), encoding='utf-16')

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



class book_data:
    def __init__(self) :
        self.ori_title = ""
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

    def search_for_book(self, title) :
        client_id = "EiPxhHox870abSfDvZBR"
        client_pw = "RqJncUd4p1"
        enc_text = parse.quote(title)

        url = "https://openapi.naver.com/v1/search/book.json?query=" + enc_text + "&display=10&start=1"
        req = request.Request(url)
        req.add_header("X-Naver-Client-Id", client_id)
        req.add_header("X-Naver-Client-Secret", client_pw)

        try:
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

            book_dict = json.loads(response_body.decode('utf-8'))

            if (len(book_dict['items']) > 1):
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

            if self.search_accuracy == 0 :
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
