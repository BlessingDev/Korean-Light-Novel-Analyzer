from collections import defaultdict

class book_data :

    def __init__(self):
        self.date_to_titles = defaultdict(list)
        self.title_list = list()

    def add_by_date_title(self, date, title) :
        self.date_to_titles[date].append(title)
        self.title_list.append(title)

        self.title_list = sorted(self.title_list)