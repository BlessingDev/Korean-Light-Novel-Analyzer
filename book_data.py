import datetime


class BookData:
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

        if 'genre' in dict.keys() :
            self.genre = dict['genre']
        if 'pubdate' in dict.keys() :
            self.pubdate = dict['pubdate']

        return self

    def __str__(self):
        rex = 'title: {}\n' \
              'ori title: {}\n' \
              'author: {}\n' \
              'translator: {}\n' \
              'publisher: {}\n' \
              'description: {}\n' \
              'genre: {}' \
            .format(self.title, self.ori_title, self.author, self.translator, self.publisher, self.description, self.genre)

        return rex

    def get_pub_year_month(self) :
        temp_date = datetime.datetime.strptime(self.pubdate, '%Y%m%d')
        return (temp_date.year.__str__() + "년 " + temp_date.month.__str__() + "월")

    def get_image_dir(self) :
        path = 'images\\' + self.title + '_image.' +\
                                self.image_url.split('.')[-1].split('?')[0]

        ignore_word = [
            '?',
            '/',
            ':'
        ]
        for word in ignore_word:
            path = path.replace(word, '')

        return path

    def get_icon_dir(self) :
        path = 'images\\' + self.title + '_icon.' + \
               self.image_url.split('.')[-1].split('?')[0]

        ignore_word = [
            '?',
            '/',
            ':'
        ]
        for word in ignore_word:
            path = path.replace(word, '')

        return path