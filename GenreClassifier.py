from collections import defaultdict
import math

import nlp_module

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
        if chunk[1] == 'NNG' or chunk[1] == 'VV' :
            word = chunk[0].lower()
            if not (word in ignore_word) :
                result.append(word)

    return set(result)

def tokenize_book(book) :
    word_list = []
    word_list.extend(tokenize(book.title))
    word_list.extend(tokenize(book.description))

    return word_list

def count_words(training_set) :
    counts = defaultdict(defaultdict(0))

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
    log_dict = defaultdict(0)

    for word, prob_dict in word_probs :
        if word in book_words :
            for genre in prob_dict.keys() :
                log_dict[genre] += math.log(prob_dict[genre])

        else :
            for genre in prob_dict.keys() :
                log_dict[genre] += math.log(1.0 - prob_dict[genre])

    exp_list = [(x, math.exp(log_dict[x])) for x in log_dict.keys()]
    prob_sum = sum([x for _, x in exp_list])
    return [{genre : (exp / prob_sum)} for genre, exp in exp_list]

class GenreClassifier :
    def __init__(self, k = 0.5) :
        self.k = k
        self.word_probs = {}
        self.genre_list = []

    def train(self, train_set) :
        num_genre = defaultdict(0)

        for t_set in train_set :
            for genre in t_set["genre"] :
                num_genre[genre] += 1 / len(t_set["genre"])

        self.genre_list = list(num_genre.keys())

        word_counts = count_words(train_set)
        self.word_probs = word_probabilities(word_counts, num_genre, self.k)

    def classify(self, book) :
        return genre_probability(self.word_probs, book)