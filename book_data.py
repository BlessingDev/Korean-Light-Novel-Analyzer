from collections import defaultdict
from urllib import parse, request
from bs4 import BeautifulSoup
import json
import pathlib

import crawler

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
    book_dict["description"] = book.description
    book_dict["isbn"] = book.isbn

    return dict_to_json(book_dict, lambda x : '"' + x.__str__() + '"')

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
    else :
        print("type은 {}".format(type(data)))
        return '""'


class book_storer:
    def __init__(self):
        self.date_to_titles = defaultdict(list)
        self.title_list = list()

        self.book_list = list()
        self.date_to_book = defaultdict(list)

        self.import_data()

    def import_data(self) :
        self.title_list = list()
        self.date_to_titles = defaultdict(list)

        title_p = pathlib.Path('book_title.json')
        if title_p.exists() :
            title_json = title_p.read_text('utf-16')
            self.title_list = json.loads(title_json)


        dic_p = pathlib.Path('date_to_titles.json')
        if dic_p.exists() :
            dic_json = dic_p.read_text('utf-16')
            self.date_to_titles = json.loads(dic_json)



    def add_by_date_title(self, date, title):
        self.date_to_titles[date].append(title)
        self.title_list.append(title)

        self.title_list = sorted(self.title_list)

    def export_data(self) :
        title_p = pathlib.Path('book_title.json')
        title_p.write_text(list_to_json(self.title_list, data_to_json), encoding='utf-16')

        dic_p = pathlib.Path('date_to_titles.json')
        dic_p.write_text(dict_to_json(self.date_to_titles, data_to_json), encoding='utf-16')

        book_p = pathlib.Path('book_data.json')
        book_p.write_text(list_to_json(self.book_list, data_to_json), encoding='utf-16')

        dic_p = pathlib.Path('date_to_book.json')
        dic_p.write_text(dict_to_json(self.date_to_book, data_to_json), encoding='utf-16')





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

    def from_title(self, title) :
        self.ori_title = title
        self.error_code = 0

        print("'{}'을 검색함".format(title))

        client_id = "EiPxhHox870abSfDvZBR"
        client_pw = "RqJncUd4p1"
        enc_text = parse.quote(title)

        url = "https://openapi.naver.com/v1/search/book.json?query=" + enc_text + "&display=10&start=1"
        req = request.Request(url)
        req.add_header("X-Naver-Client-Id", client_id)
        req.add_header("X-Naver-Client-Secret", client_pw)

        response = None
        try:
            response = request.urlopen(req)
        except:
            print("책 제목 {} 검색 불가".format(title))
            self.error_code = 1
            return self

        res_code = response.getcode()


        if (res_code == 200):
            response_body = response.read()

            book_dict = json.loads(response_body.decode('utf-8'))

            if (len(book_dict['items']) > 1) :
                item = book_dict['items'][0]

                self.title = item['title']
                self.image_url = item['image']
                self.author = item['author']
                self.publisher = item['publisher']
                self.isbn = item['isbn']
                self.description = ''
                self.translator = ''

                link = item['link']
                self.crawl_description(link)

                self.title = self.title.replace('<b>', '').replace('</b>', '')
                self.title.replace('\ufeff', '')
                self.image_url.replace('\ufeff', '')
                print("검색된 책 제목: {}".format(self.title))
            else :
                self.error_code = 2
                print("책 제목 {0}에 대한 검색 결과가 없음".format(title))


        else:
            print("error code: {0}".format(res_code))

        return self

    def from_json_dict(self, dict) :
        self.ori_title = dict["ori title"]
        self.title = dict["title"]
        self.author = dict["author"]
        self.translator = dict["translator"]
        self.image_url = dict["image_url"]
        self.isbn = dict["isbn"]
        self.publisher = dict["publisher"]
        self.description = dict["discription"]

        return self

    def __str__(self):
        rex = 'title: {}\n' \
              'author: {}\n' \
              'translator: {}\n' \
              'publisher: {}\n' \
              'description: {}' \
            .format(self.title, self.author, self.translator, self.publisher, self.description)

        return rex

    def crawl_description(self, link):
        c = crawler.get_html(link)

        if not (c is None) :
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
