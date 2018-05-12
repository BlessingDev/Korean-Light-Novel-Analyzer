from collections import defaultdict, Counter
import json, pathlib

import nlp_module, json_file

class BookDataSearcher :
    def __init__(self) :
        self.wordtobookindex = None

    def init_word_index(self, book_set) :
        # 검색 인덱스랑 나중에 책 인덱스랑 안 맞음
        self.wordtobookindex = defaultdict(list)

        for i in range(len(book_set)) :
            book = book_set[i]
            words = nlp_module.pos_Kkma(book.title)

            words = set(words)
            for word in words :
                if word[1][0] == 'N' or word[1] == 'OL':
                    #print(word)
                    self.wordtobookindex[word[0]].append(i)

        dictlist = ["'{}' : {}".format(key, [(idx, book_set[idx].title) for idx in self.wordtobookindex[key]])
              for key in self.wordtobookindex.keys()]
        for i in range(len(dictlist)) :
            print(dictlist[i])
        print("index init finished")

    def search_book_by_title(self, title, n = 10) :
        words = nlp_module.pos_Kkma(title)

        words = set(words)
        appearance_list = []
        for word in words :
            if (word[1][0] == 'N' or word[1] == 'OL') and\
                    word[0] in self.wordtobookindex.keys():
                print(word)
                #print(self.wordtobookindex[word[0]])
                appearance_list.extend(self.wordtobookindex[word[0]])

        #print(appearance_list)
        counted_list = Counter(appearance_list)

        sortedlist = sorted(counted_list.items(), key=lambda x : x[1], reverse=True)

        return sortedlist[:n]

    def export_data(self) :
        wtipath = pathlib.Path('wordtoindex_searcher.json')
        wtipath.write_text(json_file.dict_to_json(self.wordtobookindex, json_file.data_to_json), encoding='utf-8')

    def import_data(self) :
        wtipath = pathlib.Path('wordtoindex_searcher.json')
        if wtipath.exists() :
            self.wordtobookindex = json.loads(wtipath.read_text('utf-8'), encoding='utf-8', strict=False)