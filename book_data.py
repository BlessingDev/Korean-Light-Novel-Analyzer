from collections import defaultdict
from urllib import parse, request
from bs4 import BeautifulSoup
import json
import pathlib

import crawler

def list_to_json(list):
    out_str = "["
    for val in list:
        out_str += ('"' + val.__str__() + '"')
        out_str += ", "

    out_str = out_str[:-2]
    out_str += "]"
    return out_str

def listdict_to_json(dict) :
    out_str = "{"
    for key in dict.keys() :
        out_str += ('"' + key.__str__() + '"')
        out_str += ": "
        out_str += list_to_json(dict[key])
        out_str += ", "

    out_str = out_str[:-2]
    out_str += "}"
    return out_str


class book_storer:
    def __init__(self):
        self.date_to_titles = defaultdict(list)
        self.title_list = list()

        self.import_data()

    def import_data(self) :
        title_p = pathlib.Path('book_title.json')
        if title_p.exists() :
            title_json = title_p.read_text('utf-8')
            self.title_list = json.loads(title_json)

        dic_p = pathlib.Path('date_to_titles.json')
        if dic_p.exists() :
            dic_json = dic_p.read_text('utf-8')
            self.date_to_titles = json.loads(dic_json)


    def add_by_date_title(self, date, title):
        self.date_to_titles[date].append(title)
        self.title_list.append(title)

        self.title_list = sorted(self.title_list)

    def export_data(self) :
        title_p = pathlib.Path('book_title.json')
        str_data = self.title_list.__str__()
        str_data = str_data[:88] + str_data[88:].replace("'", '"')\
            .replace('μ"', "μ'").replace('"서민 샘플"', "'서민 샘플'")\
            .replace('"유가오"', "'유가오'").replace('"나"', "'나'")
        title_p.write_text(list_to_json(self.title_list), encoding='utf-8')

        dic_p = pathlib.Path('date_to_titles.json')
        str_data = self.date_to_titles.__str__()
        str_data = str_data[27:].replace("'", '"').replace('μ"', "μ'")\
            .replace('"유가오"', "'유가오'").replace('"아오이"', "'아오이'")\
            .replace('"오보로즈키요"', "'오보로즈키요'").replace('"스에츠무하나"', "'스에츠무하나'")\
            .replace('"나"', "'나'")
        dic_p.write_text(listdict_to_json(self.date_to_titles), encoding='utf-8')



class book_data:
    def __init__(self, title):
        self.ori_title = title

        client_id = "EiPxhHox870abSfDvZBR"
        client_pw = "RqJncUd4p1"
        enc_text = parse.quote(title)

        url = "https://openapi.naver.com/v1/search/book.json?query=" + enc_text + "&display=10&start=1"
        req = request.Request(url)
        req.add_header("X-Naver-Client-Id", client_id)
        req.add_header("X-Naver-Client-Secret", client_pw)

        response = request.urlopen(req)
        res_code = response.getcode()

        if (res_code == 200):
            response_body = response.read()

            book_dict = json.loads(response_body.decode('utf-8'))

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


        else:
            print("error code: {0}".format(res_code))

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

        soup = BeautifulSoup(c)

        for div in soup('div'):
            if 'class' in div.attrs and \
                    'book_info_inner' in div['class'] :
                for em in div('em'):
                    if em.get_text() == '역자':
                        print('역자 있음')
                        self.translator = em.next_sibling.next_sibling.get_text()

            elif 'id' in div.attrs and \
                    (div['id'] == 'bookIntroContent' or div['id'] == 'pubReviewContent') :
                print('description 있음')
                self.description = div('p')[0].get_text()
