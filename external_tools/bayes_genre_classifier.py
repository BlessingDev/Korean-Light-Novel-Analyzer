import json
import pathlib
from collections.__init__ import defaultdict

import json_file
from external_tools.genre_classifier import count_words, word_probabilities, genre_probability


class bayes_GenreClassifier :
    def __init__(self, k = 0.5) :
        self.k = k
        self.word_probs = []
        self.genre_list = []

    def train(self, train_set) :
        num_genre = defaultdict(lambda : 0)

        for t_set in train_set :
            for genre in t_set["genre"] :
                num_genre[genre] += 1 / len(t_set["genre"])

        self.genre_list = num_genre
        print(num_genre)

        word_counts = count_words(train_set)
        self.word_probs = word_probabilities(word_counts, num_genre, self.k)

    def classify(self, book) :
        prob_list = genre_probability(self.word_probs, book)
        smoothed_list = list()

        for genre, prob in prob_list :
            prob =  prob * 1.0e56
            smoothed_list.append((genre, prob / self.genre_list[genre] ** 32))

        #print(prob_list)
        return prob_list

    def export_data(self) :
        dic_p = pathlib.Path('word_prob.json')
        dic_p.write_text(json_file.list_to_json([[x, y] for x, y in self.word_probs], json_file.data_to_json), encoding='utf-16')

        dic_p = pathlib.Path('genre_num.json')
        dic_p.write_text(json_file.dict_to_json(self.genre_list, json_file.data_to_json), encoding='utf-16')

    def import_data(self) :
        book_path = pathlib.Path('word_prob.json')
        if book_path.exists():
            temp = book_path.read_text(encoding='utf-16')
            prob_list = json.loads(temp, strict=False)

            for genre, prob in prob_list:
                # print(type(book))
                self.word_probs.append((genre, prob))

        book_path = pathlib.Path('genre_num.json')
        if book_path.exists():
            temp = book_path.read_text(encoding='utf-16')
            self.genre_list = json.loads(temp, strict=False)