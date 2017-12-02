from collections import defaultdict, Counter

import nlp_module

class BookSearcher :
    def __init__(self) :
        self.wordtobookindex = None

    def init_word_index(self, book_set) :
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