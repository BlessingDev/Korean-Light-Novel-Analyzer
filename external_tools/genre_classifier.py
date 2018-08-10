from collections import defaultdict
from abc import *
import math, pathlib, json

import nlp_module, json_file

genre_to_index = None
index_to_genre = None

genretoindex = pathlib.Path('genretoindex.json')
if genretoindex.exists() :
    genre_to_index = json.loads(genretoindex.read_text('utf-8'), strict=False)
    index_to_genre = [g for i in range(len(genre_to_index.keys())) for g, j in genre_to_index.items() if j == i]
else :
    print('genretoindex.json does not exist')

word_to_index = None
index_to_word = None

wordtoindex_file = pathlib.Path('wordtoindex.json')
if wordtoindex_file.exists() :
    word_to_index = json.loads(wordtoindex_file.read_text('utf-8'), strict=False)
    index_to_word = [w for i in range(len(word_to_index.keys())) for w, j in word_to_index.items() if j == i]
else:
    print('wordtoindex.json  does not exist')


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

def adjust_train_set(input_size, wordtoindex_dic, genre_num, genretoindex_dic, training_set):
    inputs = []
    targets = []
    print("학습 set 만들기 시작")

    for tr_dic in training_set :
        print(tr_dic["book"].title)
        input_vector = [0 for _ in range(input_size)]
        word_list = tokenize_book(tr_dic["book"])
        no_num = 0
        for word in word_list :
            if word in wordtoindex_dic.keys() :
                input_vector[wordtoindex_dic[word]] = 1
            else :
                no_num += 1
                print("{} 단어는 학습 대상이 아님".format(word))

        print("전체 단어 {}개 중에 학습 불가 단어 {}개".format(len(word_list), no_num))
        inputs.append(input_vector)

        target_vector = [0 for _ in range(genre_num)]
        for genre in tr_dic["genre"] :
            target_vector[genretoindex_dic[genre]] = 1

        targets.append(target_vector)

    return inputs, targets

def adjust_train_logistic(input_size, word_to_index, genre_num, genre_to_index, training_set) :
    inputs = []
    targets = []
    print("학습 set 만들기 시작")

    for tr_dic in training_set:
        print(tr_dic["book"].title)
        input_vector = [0 for _ in range(input_size)]
        word_list = tokenize_book(tr_dic["book"])
        no_num = 0
        for word in word_list:
            if word in word_to_index.keys():
                input_vector[word_to_index[word]] = 1
            else:
                no_num += 1
                print("{} 단어는 학습 대상이 아님".format(word))

        print("전체 단어 {}개 중에 학습 불가 단어 {}개".format(len(word_list), no_num))
        inputs.append(input_vector)

        target_vector = [0.0 for _ in range(genre_num)]
        for genre in tr_dic["genre"]:
            g_num = len(genre)
            target_vector[genre_to_index[genre]] = 1 / g_num

        targets.append(target_vector)

    return inputs, targets

def adjust_book_input(book, input_num) :
    print(book.title)
    input_vector = [0 for _ in range(input_num)]
    word_list = tokenize_book(book)
    for word in word_list:
        if word in word_to_index.keys():
            input_vector[word_to_index[word]] = 1
        else:
            print("{} 단어는 학습 대상이 아님".format(word))

    return input_vector

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

def set_to_vector(trainig_set, word_num) :
    global index_to_genre, index_to_word, word_to_index, genre_to_index

    genre_to_index = {}
    word_to_index = {}
    genre_list = [genre for item in trainig_set
                    for genre in item["genre"]]
    genre_list = set(genre_list)

    genre_num = len(genre_list)

    print(genre_list)
    num_counts = count_word_num(trainig_set)
    num_counts.sort(key=lambda x : x[1], reverse=True)

    num_counts = num_counts[:word_num]

    print("word_count done")

    for i in range(word_num) :
        word_to_index[num_counts[i][0]] = i

    index_to_word = [w for i in range(len(word_to_index.keys())) for w, j in word_to_index.items() if j == i]

    for i, genre in enumerate(list(genre_list)) :
        genre_to_index[genre] = i

    index_to_genre = [g for i in range(len(genre_to_index.keys())) for g, j in genre_to_index.items() if j == i]


    print("trainset adjustment finished")

    wordtoindex_dic_path = pathlib.Path('wordtoindex.json')
    wordtoindex_dic_path.write_text(json_file.dict_to_json(word_to_index, json_file.data_to_json),
                                    encoding='utf-8')

    genretoindex_dic_path = pathlib.Path('genretoindex.json')
    genretoindex_dic_path.write_text(json_file.dict_to_json(genre_to_index,
                                                            json_file.data_to_json),
                                     encoding='utf-8')

    print("2index set file saved")

    return adjust_train_logistic(word_num, word_to_index, genre_num, genre_to_index,
                                           trainig_set)

class genre_classifier :
    def __init__(self) :
        pass

    @abstractmethod
    def train(self, input_sets, target_sets, n=1000, error=0.1):
        '''
        classifier를 훈련시키기 위한 함수
        :param training_set: 입력 셋 [None, input_num]
        :param target_set: 목표 셋 [output_num]
        :param n: 훈련횟수
        :param error: 만족해야할 최소 에러
        :return: None
        '''
        print("you have to override this function")

    @abstractmethod
    def classify(self, book) :
        '''
        학습된 모델로 책의 장르를 분류하는 함수
        :param book: 분류할 책의 book_data 객체
        :return: [(genre name, float number)] 형태의 리스트로 반환
        '''
        print("you have to override this function")

    @abstractmethod
    def genre_hot(self, output):
        '''
        결과 벡터를 인자로 받아 genre의 리스트로 반환하는 함수
        :param output: 모델의 출력 벡터
        :return: [genre] 리스트
        '''
        print("you have to override this function")

    def genre_accuraccy(self, g1, g2):
        g_len = max(len(g1), len(g2))
        same_num = len([g_i for g_i in g1 if g_i in g2])
        return same_num / g_len

    def examine(self, test_set) :
        '''
        장르 정확도를 검사하는 함수
        :param test_set: [{"book" : book_data, "genre": []}]
        :return: float(0.0~1.0)
        '''
        t_num = len(test_set)
        a_sum = 0.0

        for t in test_set :
            g = self.genre_hot(self.classify(t["book"]))
            a_sum += self.genre_accuraccy(g, t["genre"])
            print(g, t["genre"])

        return a_sum / t_num