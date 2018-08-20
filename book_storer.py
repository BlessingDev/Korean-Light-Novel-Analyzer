from collections import defaultdict
from urllib import request
import pathlib, random, json, datetime

import json_file, book_data, nlp_module
from external_tools_instantiater import external_tools_instantiater as exins

class BookStorer :
    def __init__(self):
        self.book_list = list()
        self.date_to_book = defaultdict(list)
        self.training_set = None
        self.searcher = exins.get_instance().get_searcher_naver_instance() #
        self.curt = datetime.datetime.now()


    def import_data(self) :
        self.book_list = list()
        self.date_to_book = defaultdict(list)

        book_path = pathlib.Path('book_data.json')
        if book_path.exists() :
            temp = book_path.read_text(encoding='utf-16')
            book_list = json.loads(temp, encoding='utf-16', strict=False)

            for book in book_list :
                new_book = book_data.BookData()
                new_book.from_json_dict(book)
                self.book_list.append(new_book)

        book_path = pathlib.Path('date_to_book.json')
        if book_path.exists() :
            temp = book_path.read_text(encoding='utf-16')
            book_dict = json.loads(temp, encoding='utf-16', strict=False)

            for key in book_dict.keys():
                new_list = list()
                book_list = book_dict[key]
                for book in book_list :
                    new_book = book_data.BookData()
                    new_book.from_json_dict(book)
                    new_list.append(new_book)

                self.date_to_book[key] = new_list

        tra_path = pathlib.Path("training_set.json")
        if tra_path.exists() :
            temp = tra_path.read_text(encoding='utf-16')
            book_dict = json.loads(temp, strict=False)

            for dic in book_dict :
                new_book = book_data.BookData()
                new_book.from_json_dict(dic["book"])
                dic["book"] = new_book

            self.training_set = book_dict

    def add_by_tl_td(self, title_list, title_to_date) :
        self.date_to_book = defaultdict(list)
        f = open("Naver Book Search Log_{} {}h{}m{}s.txt".
                 format(self.curt.date(), self.curt.hour, self.curt.minute, self.curt.second), "w")
        self.searcher.f = f

        for idx in range(len(title_list)) :
            title = title_list[idx]
            print("{}/{}".format(idx, len(title_list)))
            book = book_data.BookData()
            self.searcher.book = book
            self.searcher.from_title(title)
            self.book_list.append(book)
            self.date_to_book[title_to_date[book.ori_title]].append(book)

        self.searcher.search_finished()

    def export_data(self) :
        book_p = pathlib.Path('book_data.json')
        try:
            book_p.write_text(json_file.list_to_json(self.book_list, json_file.data_to_json), encoding='utf-16')
        except:
            print("exception occured")

        dic_p = pathlib.Path('date_to_book.json')
        dic_p.write_text(json_file.dict_to_json(self.date_to_book, json_file.data_to_json), encoding='utf-16')

        #ran_p = pathlib.Path('training_set.json')
        #ran_p.write_text(json_file.list_to_json(self.random_set, json_file.data_to_json), encoding='utf-16')

    def get_title_list(self) :
        return [x.title for x in self.book_list]

    def get_orititle_list(self) :
        return [x.ori_title for x in self.book_list]

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
            if book.error_code == 0 and book.genre == []:
                genres = g.genre_hot(g.classify(book))

                print(genres)
                book.genre = genres

    def download_images(self) :
        for book in self.get_ordinary_book() :
            iconpath = 'images\\' + book.title + '_icon.' +\
                                book.image_url.split('.')[-1].split('?')[0]


            ignore_word = [
                '?',
                '/',
                ':'
            ]
            for word in ignore_word :
                iconpath = iconpath.replace(word, '')

            if pathlib.Path(iconpath).exists() :
                print(book.title + " 이미 받아짐")
                continue

            try:
                request.urlretrieve(book.image_url, iconpath)
                print(book.title + ' icon 다운로드됨')
            except:
                print(book.title + " icon 다운로드에 Error")

            imagepath = 'images\\' + book.title + '_image.' +\
                                book.image_url.split('.')[-1].split('?')[0]
            for word in ignore_word :
                imagepath = imagepath.replace(word, '')

            try:
                request.urlretrieve(book.image_url.split('?')[0], imagepath)
                print(book.title + ' image 다운로드됨')
            except:
                print(book.title + " image 다운로드에 Error")

    def add_books_by_title(self, bookdate) :
        titlelist = self.get_orititle_list()
        f = open("Naver Book Search Log_{} {}h{}m{}s.txt".
                 format(self.curt.date(), self.curt.hour, self.curt.minute, self.curt.second), "w")
        self.searcher.f = f

        for idx in range(len(bookdate)) :
            btlist = bookdate[idx][1]
            dt = bookdate[idx][0]
            for bt in btlist :
                if bt in titlelist :
                    print('{}가 갱신됨'.format(bt))
                    bidx = titlelist.index(bt)
                    b = book_data.BookData()
                    self.searcher.book = b
                    self.searcher.from_title(bt)
                    self.book_list[bidx] = b

                    dtitle = [x.ori_title for x in self.date_to_book[dt]]
                    if bt in dtitle :
                        bdidx = dtitle.index(bt)
                        self.date_to_book[dt][bdidx] = self.book_list[bidx]
                    else :
                        print('왜 {}는 책 리스트에는 있는데 {} 출판 책 리스트에는 없는거지?'.format(bt, dt))
                        self.date_to_book[dt].append(self.book_list[bidx])
                else :
                    b = book_data.BookData()
                    self.searcher.book = b
                    self.searcher.from_title(bt)
                    self.date_to_book[dt].append(b)

        self.searcher.search_finished()

    def get_usable_training_set(self) :
        return [{"book": t_set["book"], "genre": t_set["genre"]} for t_set in self.training_set
                          if len(t_set["genre"]) > 0]