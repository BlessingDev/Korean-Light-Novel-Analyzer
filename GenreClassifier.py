from collections import defaultdict
import math, pathlib, json

import nlp_module, json_file

def tokenize(sentences) :
    sen_nlp = nlp_module.pos_Kkma(sentences)
    result = []

    ignore_word = [
        'extreme',
        'novel',
        'j',
        'l',
        'nt'
    ]

    for chunk in sen_nlp :
        if chunk[1] == 'NNG' :
            word = chunk[0].lower()
            if not (word in ignore_word) :
                result.append(word)

    return set(result)

def tokenize_book(book) :
    word_list = []
    word_list.extend(tokenize(book.title))
    word_list.extend(tokenize(book.description))

    return set(word_list)

def count_words(training_set) :
    counts = defaultdict(lambda : defaultdict(lambda : 0))

    for t_set in training_set :
        for word in tokenize_book(t_set["book"]) :
            for genre in t_set["genre"] :
                counts[word][genre] += 1 / len(t_set["genre"])

    return counts

def word_probabilities(counts, total_genres, k = 0.5) :
    prob_list = []

    for word in counts.keys() :
        prob_dict = {}
        for genre in total_genres.keys() :
            genre_word_num = counts[word].get(genre, 0)
            prob_dict[genre] = (genre_word_num + k) / (total_genres[genre] + k * 2)

        prob_list.append((word, prob_dict))

    return prob_list

def genre_probability(word_probs, book) :
    '''
    모든 장르에 대한 bayesian 확률을 계산하는 함수
    :param word_probs: [(word, prob_list:각 장르에 대한 확률 리스트)]
    :param book: book_data 객체
    :return: {genre: prob} 각 장르에 대한 확률
    '''
    book_words = tokenize_book(book)
    log_dict = defaultdict(lambda : 0)

    for word, prob_dict in word_probs :
        #print(prob_dict)
        if word in book_words :
            for genre in prob_dict.keys() :
                log_dict[genre] += math.log(prob_dict[genre])

        else :
            for genre in prob_dict.keys() :
                #print(1.0 - prob_dict[genre])
                log_dict[genre] += math.log(1.0 - prob_dict[genre])

    exp_list = [(x, math.exp(log_dict[x])) for x in log_dict.keys()]
    prob_sum = sum([x for _, x in exp_list])
    return [(genre, (exp / prob_sum)) for genre, exp in exp_list]

class GenreClassifier :
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

        print(prob_list)
        return smoothed_list

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
