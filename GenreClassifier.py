from collections import defaultdict
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
import math, pathlib, json, random

import nlp_module, json_file

def tokenize(sentences) :
    sen_nlp = nlp_module.pos_Kkma(sentences)
    result = []

    ignore_word = [
        'extreme',
        'novel',
        'j',
        'l',
        'nt',
        '노',
        '라이트',
        '시리즈',
        '제',
        '노',
        '일본',
        '의',
        '벨',
        '회',
        '노와',
        '리',
        '장',
        '마',
        '라',
        '히',
        '을',
        '토',
        '팬',
        '전',
        '탄',
        '오',
        '말',
        '메',
        '레',
        '로',
        '타',
        '바',
        '가',
        '서',
        '루',
        '디',
        '데',
        '요',
        '하',
        '들',
        '카',
        '키',
        '미',
        '코',
        '유',
        '속',
        '우',
        '사',
        '르',
        '출간',
        '사이트',
        '독자',
        '세',
        '작품',
        '회',
        '편',
        '완결',
        '신작',
        '호평',
        '누',
        '연재',
        '저자',
        '원작',
        '주',
        '단편',
        '단편집',
        '국내',
        '장려상',
        '발행',
        '최신작',
        '모',
        '사토',
        '와의',
        '중',
        '책갈피',
        '초판',
        '한국',
        '투',
        '황',
        '모토',
        '니스',
        '마코토',
        '나미',
        '통합',
        '루가',
        '이지만',
        '마사',
        '맥',
        '토모',
        '이슈',
        '전개'
    ]

    for chunk in sen_nlp :
        if chunk[1] == 'NNG' or chunk[1] == 'NNP':
                #or chunk[1] == 'VV' or chunk[1] == 'VA':
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
        words = tokenize_book(t_set["book"])
        for word in words :
            for genre in t_set["genre"] :
                counts[word][genre] += 1 / len(t_set["genre"])

    return counts

def count_word_num(training_set) :
    counts = count_words(training_set)

    num_counts = [(word, sum([counts[word][genre] for genre in counts[word].keys()]))
                  for word in counts.keys()]

    return num_counts

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

def sigmoid(t) :
    return 1 / (1 + math.exp(-t))

def dot(x, y) :
    return sum([x_i * y_i for x_i, y_i in zip(x, y)])

class neuron :
    def __init__(self, weights) :
        self.weights = []
        for data in weights :
            self.weights.append(numpy.float64(data))

    def output(self, input) :
        return sigmoid(dot(self.weights, input))

    def __str__(self) :
        return self.weights.__str__()

class neuron_classifier :
    def __init__(self, input_size, num_hidden, output_size) :
        self.wordtoindex_dic = {}
        self.genretoindex_dic = {}
        random.seed()

        self.input_size = input_size
        self.genre_num = output_size

        hidden_layer = [neuron([random.random() for _ in range(input_size + 1)])
                        for _ in range(num_hidden)]

        output_layer = [neuron([random.random() for _ in range(num_hidden + 1)])
                        for _ in range(output_size)]

        self.neuron_layers = [
            hidden_layer,
            output_layer
        ]

        print("neuron_classifier __init__")

    def feed_forward(self, input_vector) :
        outputs = []

        template = """
        #include <cmath>
        
        #define VECTOR_LEN $Vecotr_Len
        
        __device__ void dot(float* A, float* B, float* o)
        {
            *(o) += A[threadId.x] * B[threadId.x];
        }
        
        __device__ float sigmoid(float* A, float* B, int* len)
        {
            
        }
        
        """


        # 이 for문은 최적화 가능
        for layer in self.neuron_layers :
            input_with_bias = input_vector + [1]
            output = [nr.output(input_with_bias) for nr in layer]
            outputs.append(output)

            input_vector = output

        return outputs

    def backpropagate(self, input_vector, targets) :

        hidden_outputs, outputs = self.feed_forward(input_vector)

        output_deltas = [output * (output - 1) * (output - target)
                         for output, target in zip(outputs, targets)]

        # 이 for문은 최적화 가능
        for i, output_neuron in enumerate(self.neuron_layers[-1]) :
            # i번째 출력층에 대해
            for j, hidden_output in enumerate(hidden_outputs) :
                output_neuron.weights[j] -= output_deltas[i] * hidden_output

        hidden_deltas = [hidden_output * (1 - hidden_output) *
                         dot(output_deltas, [n.weights[i] for n in self.neuron_layers[-1]])
                         for i, hidden_output in enumerate(hidden_outputs)]

        for i, hidden_neuron in enumerate(self.neuron_layers[0]) :
            for j, input in enumerate(input_vector + [1]) :
                hidden_neuron.weights[j] -= hidden_deltas[i] * input

    def adjust_train_set(self, training_set) :
        inputs = []
        targets = []
        print("학습 set 만들기 시작")

        for tr_dic in training_set :
            print(tr_dic["book"].title)
            input_vector = [0 for _ in range(self.input_size)]
            word_list = tokenize_book(tr_dic["book"])
            no_num = 0
            for word in word_list :
                if word in self.wordtoindex_dic.keys() :
                    input_vector[self.wordtoindex_dic[word]] = 1
                else :
                    no_num += 1
                    print("{} 단어는 학습 대상이 아님".format(word))

            print("전체 단어 {}개 중에 학습 불가 단어 {}개".format(len(word_list), no_num))
            inputs.append(input_vector)

            target_vector = [0 for _ in range(self.genre_num)]
            for genre in tr_dic["genre"] :
                target_vector[self.genretoindex_dic[genre]] = 1

            targets.append(target_vector)

        return inputs, targets

    def train_with_book(self, trainig_set, genre_list, n = 10000) :
        print(genre_list)
        num_counts = count_word_num(trainig_set)
        num_counts.sort(key=lambda x : x[1], reverse=True)

        num_counts = num_counts[:self.input_size]

        print("word_count done")

        for i in range(self.input_size) :
            self.wordtoindex_dic[num_counts[i][0]] = i

        for i, genre in enumerate(list(genre_list.keys())) :
            self.genretoindex_dic[genre] = i

        inputs, targets = self.adjust_train_set(trainig_set)

        print("trainset adjustment finished")

        for i in range(n) :
            for input_vector, target_vector in zip(inputs, targets) :
                self.backpropagate(input_vector, target_vector)
            print("train cycle {} finished".format(i))

        print("train succeed")
        print(self.neuron_layers)

    def classify(self, book) :
        '''
        학습된 신경망으로 책의 장르를 자동으로 분류하는 함수
        :param book: 분류할 책의 book_data 객체
        :return: [(genre name(str), probability(float))] 형태의 리스트로 반환
        '''
        print(book.title)
        input_vector = [0 for _ in range(len(self.input_size))]
        word_list = tokenize_book(book)
        for word in word_list:
            if word in self.wordtoindex_dic.keys():
                input_vector[self.wordtoindex_dic[word]] = 1
            else:
                print("{} 단어는 학습 대상이 아님".format(word))

        outputs = self.feed_forward(input_vector)
        indextogenre_dic = {idx : genre for genre, idx in self.genretoindex_dic.items()}
        return [(indextogenre_dic[i], outputs[i]) for i in range(len(outputs))]