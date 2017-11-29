from collections import defaultdict
import numpy
import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
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
        self.hidden_size = num_hidden
        self.genre_num = output_size

        hidden_layer = [neuron([random.random() * 2 - 1 for _ in range(input_size + 1)])
                        for _ in range(num_hidden)]

        output_layer = [neuron([random.random() * 2 - 1 for _ in range(num_hidden + 1)])
                        for _ in range(output_size)]

        self.neuron_layers = [
            hidden_layer,
            output_layer
        ]

        template = """
        #include <math.h>
        
        __global__ void sigmoid(float* c, const float* i)
        {
            int idx = threadIdx.x;
    
            float val = i[idx];
            c[idx] = 1 / (1 + exp(-val));
        }
        
        __global__ void Relu(float* c, const float* i)
        {
            int idx = threadIdx.x;
        
            float val = i[idx];
            c[idx] = (val > 0) ? val : 0;
        }
        
        __global__ void CutOffVal(float* vector, float* factor)
        {
            int idx = threadIdx.x;
            if (factor[idx] <= 0)
                vector[idx] = 0;
        }
        
        __global__ void MultiplyNeuron(const float* inputVector, const float* weights, float* out)
        {
            int neuronIdx = blockIdx.x * (blockDim.x);
            const float* curWeights = (weights + neuronIdx);
            float* curOut = (out + neuronIdx);
            
            curOut[threadIdx.x] = inputVector[threadIdx.x] * curWeights[threadIdx.x];
        }
        
        __global__ void DotNeuron(const float* multied, float* out, const int inputSize)
        {
            const float* curMul = (multied + (threadIdx.x * inputSize));
        
            out[threadIdx.x] = 0;
            for (int i = 0; i < inputSize; i += 1)
            {
                out[threadIdx.x] += curMul[i];
            }
        }
        
        __global__ void DotRelu(const float* outputDelta, const float* hiddenOutput, float* out)
        {
            float* curOut = (out + (blockDim.x * blockIdx.x));
        
            curOut[threadIdx.x] = outputDelta[blockIdx.x] * hiddenOutput[threadIdx.x];
        }
        
        __global__ void OutputDeltas(const float* outputs, const float* targets, float* out)
        {
            int idx = threadIdx.x;
        
            out[idx] = outputs[idx] * (1 - outputs[idx]) * (outputs[idx] - targets[idx]);
        }
        
        __global__ void OutputDeltasRelu(const float* outputs, const float* targets, float* out)
        {
            int idx = threadIdx.x;
        
            out[idx] = 2.0 * (outputs[idx] - targets[idx]);
        }
        
        __global__ void AdjustNeuron(float* weights, const float* deltas, const float* befInput)
        {
            int i = blockIdx.x;
            int j = threadIdx.x;
            float* curWeghts = (weights + (blockDim.x * blockIdx.x));
        
            curWeghts[j] -= deltas[i] * befInput[j];
        
        }
        
        __global__ void AdjustNeuronRelu(float* weights, const float* deltas, const float trainingRate)
        {
            int i = blockIdx.x;
            int j = threadIdx.x;
            float* curWeghts = (weights + (blockDim.x * blockIdx.x));
            const float* curDelta = (deltas + (blockDim.x * blockIdx.x));
        
            curWeghts[j] -= curDelta[j] * trainingRate;
        }
        
        __global__ void	Transpose(const float* weights, float* out)
        {
            int weightIdx = (blockDim.x  * threadIdx.x);
            const float* curWeight = (weights + weightIdx);
        
            int outIdx = (blockDim.x * blockIdx.x);
            float* curOut = (out + outIdx);
        
            curOut[threadIdx.x] = curWeight[blockIdx.x];
        }
        
        __global__ void HiddenDeltas(const float* outputs, const float* deltas, float* out)
        {
            int idx = threadIdx.x;
        
            out[idx] = outputs[idx] * (1 - outputs[idx]) * deltas[idx];
        }
        """

        self.cuda_func = SourceModule(template)

        print("neuron_classifier __init__")

    def export_data(self) :
        weights = [[], []]
        for neuron in self.neuron_layers[0] :
            weights[0].extend(neuron.weights)
        for neuron in self.neuron_layers[1] :
            weights[1].extend(neuron.weights)

        weights_path = pathlib.Path('weights.json')
        weights_path.write_text(json_file.list_to_json(weights, json_file.data_to_json),
                                'utf-8')

        network_info = pathlib.Path('network_info.json')
        network_info.write_text(json_file.list_to_json(
            [self.input_size, self.hidden_size, self.genre_num], json_file.data_to_json),
            encoding='utf-8')

        wordtoindex_dic_path = pathlib.Path('wordtoindex.json')
        wordtoindex_dic_path.write_text(json_file.dict_to_json(self.wordtoindex_dic, json_file.data_to_json),
                                        encoding='utf-8')

        genretoindex_dic_path = pathlib.Path('genretoindex.json')
        genretoindex_dic_path.write_text(json_file.dict_to_json(self.genretoindex_dic,
                                                                json_file.data_to_json),
                                         encoding='utf-8')

    def import_data(self) :
        info = pathlib.Path('network_info.json')
        if info.exists() :
            info_list = json.loads(info.read_text('utf-8'), strict=False)
            self.input_size = info_list[0]
            self.hidden_size = info_list[1]
            self.genre_num = info_list[2]
        else :
            print('network_info.json does not exist')

        weights = pathlib.Path('weights.json')
        if weights.exists() :
            weight_list = json.loads(weights.read_text('utf-8'), strict=False)
            weight_length = [self.input_size + 1, self.hidden_size + 1]
            node_size = [self.hidden_size, self.genre_num]
            layers = [list() for _ in range(2)]
            for i in range(2) :
                for j in range(node_size[i]) :
                    layers[i].append(neuron(weight_list[i][j * weight_length[i]:(j + 1) * weight_length[i]]))

            self.neuron_layers = layers
        else :
            print('weights.json does not exist')

        wordtoindex = pathlib.Path('wordtoindex.json')
        if wordtoindex.exists() :
            self.wordtoindex_dic = json.loads(wordtoindex.read_text('utf-8'), strict=False)
        else :
            print('wordtoindex.json does not exist')

        genretoindex = pathlib.Path('genretoindex.json')
        if genretoindex.exists() :
            self.genretoindex_dic = json.loads(genretoindex.read_text('utf-8'), strict=False)
        else :
            print('genretoindex.json does not exist')



    def feed_forward(self, input_vector) :
        outputs = []

        multiply_neuron = self.cuda_func.get_function("MultiplyNeuron")
        dot_neuron = self.cuda_func.get_function("DotNeuron")
        d_sigmoid = self.cuda_func.get_function("sigmoid")

        input_size = [self.input_size, self.hidden_size]
        output_size = [self.hidden_size, self.genre_num]

        i = 0
        # 이 for문은 최적화 가능
        for layer in self.neuron_layers :
            cur_input_size = input_size[i]
            cur_output_size = output_size[i]

            input_with_bias = input_vector + [1]

            weights = [nr.weights[i]
                      for nr in layer
                      for i in range(len(nr.weights))]
            d_weights = numpy.asarray(weights, numpy.float32)
            d_input_with_bias = numpy.asarray(input_with_bias, numpy.float32)

            d_out = numpy.asarray([0 for _ in range(len(weights))], numpy.float32)

            multiply_neuron(cuda.In(d_input_with_bias), cuda.In(d_weights), cuda.Out(d_out),
                            grid = (cur_output_size, 1, 1), block = (cur_input_size + 1, 1, 1))

            d_multi = d_out
            d_out = numpy.asarray([0 for _ in range(cur_output_size)], numpy.float32)
            d_input_size = numpy.int32(cur_input_size + 1)

            dot_neuron(cuda.In(d_multi), cuda.Out(d_out), d_input_size, block = (cur_output_size, 1, 1))

            d_dot = d_out
            d_out = numpy.asarray([0 for _ in range(cur_output_size)], numpy.float32)

            d_sigmoid(cuda.Out(d_out), cuda.In(d_dot), block = (cur_output_size, 1, 1))

            out = d_out.tolist()

            outputs.append(out)
            input_vector = out
            #print(out)
            i += 1

        return outputs

    def backpropagate(self, input_vector, targets, bef_result) :

        output_deltas = self.cuda_func.get_function("OutputDeltas")
        adjust_neuron = self.cuda_func.get_function("AdjustNeuron")
        weight_set = self.cuda_func.get_function("Transpose")
        multiply_neuron = self.cuda_func.get_function("MultiplyNeuron")
        dot_neuron = self.cuda_func.get_function("DotNeuron")
        hidden_deltas = self.cuda_func.get_function("HiddenDeltas")

        hidden_outputs, outputs = self.feed_forward(input_vector)
        deviations = sum([abs(bef - output) for bef, output in zip(bef_result, outputs)])

        d_out = numpy.asarray([0 for _ in range(self.genre_num)], numpy.float32)
        d_input = numpy.asarray(outputs, numpy.float32)
        d_weight = numpy.asarray(targets, numpy.float32)

        output_deltas(cuda.In(d_input), cuda.In(d_weight), cuda.Out(d_out),
                        block = (self.genre_num, 1, 1))

        weights = []
        for i in range(self.genre_num) :
            weights.extend(self.neuron_layers[1][i].weights)

        input_with_bias = hidden_outputs + [1]

        d_output_deltas = d_out
        d_weight = numpy.asarray(weights, numpy.float32)
        d_bef_input = numpy.asarray(input_with_bias, numpy.float32)

        adjust_neuron(cuda.InOut(d_weight), cuda.In(d_output_deltas), cuda.In(d_bef_input),
                      grid = (self.genre_num, 1, 1), block = (self.hidden_size + 1, 1, 1))

        weights = d_weight.tolist()

        # 수정된 weight를 원래 weight에 대입
        for i in range(self.genre_num) :
            #print(weights[i * (self.hidden_size + 1) : (i + 1) * (self.hidden_size + 1)])
            self.neuron_layers[1][i].weights = weights[i * (self.hidden_size + 1) : (i + 1) * (self.hidden_size + 1)]

        weights = []
        for i in range(self.genre_num) :
            cur_weight = self.neuron_layers[1][i].weights
            weights.extend(cur_weight[:-1])

        d_weight = numpy.asarray(weights, numpy.float32)
        d_out = numpy.asarray([0 for _ in range(self.genre_num * self.hidden_size)], numpy.float32)

        weight_set(cuda.In(d_weight), cuda.Out(d_out),
                   grid = (self.hidden_size, 1, 1), block = (self.genre_num, 1, 1))


        d_weight = d_out
        d_input = d_output_deltas
        d_out = numpy.asarray([0 for _ in range(self.genre_num * self.hidden_size)], numpy.float32)

        multiply_neuron(cuda.In(d_input), cuda.In(d_weight), cuda.Out(d_out),
                        grid = (self.hidden_size, 1, 1), block = (self.genre_num, 1, 1))

        d_weight = d_out
        d_out = numpy.asarray([0 for _ in range(self.hidden_size)])
        d_size = numpy.int32(self.genre_num)

        dot_neuron(cuda.In(d_weight), cuda.Out(d_out), d_size,
                   block = (self.hidden_size, 1, 1))

        d_weight = numpy.asarray(hidden_outputs, numpy.float32)
        d_input = d_out
        d_out = numpy.asarray([0 for _ in range(self.hidden_size)], numpy.float32)

        hidden_deltas(cuda.In(d_weight), cuda.In(d_input), cuda.Out(d_out),
                      block = (self.hidden_size, 1, 1))

        # hidden node에 대한 수정된 weight 구하기
        weights = []
        for i in range(self.hidden_size) :
            weights.extend(self.neuron_layers[0][i].weights)

        input_with_bias = input_vector + [1]

        d_weight = numpy.asarray(weights, numpy.float32)
        d_input = d_out # hidden delta를 대입
        d_bef_input = numpy.asarray(input_with_bias, numpy.float32)

        adjust_neuron(cuda.InOut(d_weight), cuda.In(d_input), cuda.In(d_bef_input),
                      grid = (self.hidden_size, 1, 1), block = (self.input_size + 1, 1, 1))

        weights = d_weight.tolist()

        for i in range(self.hidden_size) :
            self.neuron_layers[0][i].weights = weights[i * (self.input_size + 1) : (i + 1) * (self.input_size + 1)]

        return deviations, outputs

    def feed_forward_relu(self, input_vector) :
        outputs = []

        multiply_neuron = self.cuda_func.get_function("MultiplyNeuron")
        dot_neuron = self.cuda_func.get_function("DotNeuron")
        d_relu = self.cuda_func.get_function("Relu")

        input_size = [self.input_size, self.hidden_size]
        output_size = [self.hidden_size, self.genre_num]

        i = 0
        for layer in self.neuron_layers :
            cur_input_size = input_size[i]
            cur_output_size = output_size[i]

            input_with_bias = input_vector

            weights = [nr.weights[i]
                      for nr in layer
                      for i in range(len(nr.weights))]
            d_weights = numpy.asarray(weights, numpy.float32)
            d_input_with_bias = numpy.asarray(input_with_bias, numpy.float32)

            d_out = numpy.asarray([0 for _ in range(len(weights))], numpy.float32)

            multiply_neuron(cuda.In(d_input_with_bias), cuda.In(d_weights), cuda.Out(d_out),
                            grid = (cur_output_size, 1, 1), block = (cur_input_size, 1, 1))

            d_multi = d_out
            d_out = numpy.asarray([0 for _ in range(cur_output_size)], numpy.float32)
            d_input_size = numpy.int32(cur_input_size)

            dot_neuron(cuda.In(d_multi), cuda.Out(d_out), d_input_size, block = (cur_output_size, 1, 1))

            d_dot = d_out
            d_out = numpy.asarray([0 for _ in range(cur_output_size)], numpy.float32)

            d_relu(cuda.Out(d_out), cuda.In(d_dot), block = (cur_output_size, 1, 1))

            out = d_out.tolist()

            outputs.append(out)
            input_vector = out
            #print(out)
            i += 1

        return outputs

    def backpropagate_relu(self, input_vector, targets, bef_result) :
        training_rate = 0.002

        output_deltas = self.cuda_func.get_function("OutputDeltasRelu")
        adjust_neuron = self.cuda_func.get_function("AdjustNeuronRelu")
        transpose = self.cuda_func.get_function("Transpose")
        multiply_neuron = self.cuda_func.get_function("MultiplyNeuron")
        dot_neuron = self.cuda_func.get_function("DotNeuron")
        cut_off = self.cuda_func.get_function("CutOffVal")
        dot_relu = self.cuda_func.get_function("DotRelu")


        hidden_outputs, outputs = self.feed_forward_relu(input_vector)
        deviations = sum([abs(bef - output) for bef, output in zip(bef_result, outputs)])

        d_out = numpy.asarray([0 for _ in range(self.genre_num)], numpy.float32)
        d_input = numpy.asarray(outputs, numpy.float32)
        d_weights = numpy.asarray(targets, numpy.float32)

        output_deltas(cuda.In(d_input), cuda.In(d_weights), cuda.Out(d_out),
                      block=(self.genre_num, 1, 1))

        d_weights = numpy.asarray(hidden_outputs, numpy.float32)
        d_input_with_bias = d_out

        d_out = numpy.asarray([0 for _ in range(self.hidden_size * self.genre_num)], numpy.float32)

        dot_relu(cuda.In(d_input_with_bias), cuda.In(d_weights), cuda.Out(d_out),
                 grid = (self.genre_num, 1, 1), block = (self.hidden_size, 1, 1))

        weights = []
        for i in range(self.genre_num):
            weights.extend(self.neuron_layers[1][i].weights[:self.hidden_size])

        d_output_deltas = d_out
        d_weight = numpy.asarray(weights, numpy.float32)
        d_training_rate = numpy.float32(training_rate)

        adjust_neuron(cuda.InOut(d_weight), cuda.In(d_output_deltas), d_training_rate,
                      grid=(self.genre_num, 1, 1), block=(self.hidden_size + 1, 1, 1))

        weights = d_weight.tolist()

        # 수정된 weight를 원래 weight에 대입
        for i in range(self.genre_num):
            # print(weights[i * (self.hidden_size + 1) : (i + 1) * (self.hidden_size + 1)])
            self.neuron_layers[1][i].weights = weights[i * (self.hidden_size): (i + 1) * (self.hidden_size)]

        weights = []
        for i in range(self.genre_num):
            cur_weight = self.neuron_layers[1][i].weights
            weights.extend(cur_weight[:self.hidden_size])

        d_weight = numpy.asarray(weights, numpy.float32)
        d_out = numpy.asarray([0 for _ in range(self.genre_num * self.hidden_size)], numpy.float32)

        transpose(cuda.In(d_weight), cuda.Out(d_out),
                   grid=(self.hidden_size, 1, 1), block=(self.genre_num, 1, 1))

        d_weight = d_out
        d_input = d_output_deltas
        d_out = numpy.asarray([0 for _ in range(self.genre_num * self.hidden_size)], numpy.float32)

        multiply_neuron(cuda.In(d_input), cuda.In(d_weight), cuda.Out(d_out),
                        grid=(self.hidden_size, 1, 1), block=(self.genre_num, 1, 1))

        d_weight = d_out
        d_out = numpy.asarray([0 for _ in range(self.hidden_size)])
        d_size = numpy.int32(self.genre_num)

        dot_neuron(cuda.In(d_weight), cuda.Out(d_out), d_size,
                   block=(self.hidden_size, 1, 1))

        d_weight = numpy.asarray(hidden_outputs, numpy.float32)
        d_out = numpy.asarray([0 for _ in range(self.hidden_size)], numpy.float32)

        cut_off(cuda.InOut(d_out), cuda.In(d_weight),
                      block=(self.hidden_size, 1, 1))

        d_weights = numpy.asarray(input_vector, numpy.float32)
        d_input_with_bias = d_out

        d_out = numpy.asarray([0 for _ in range(self.hidden_size * self.genre_num)], numpy.float32)

        dot_relu(cuda.In(d_input_with_bias), cuda.In(d_weights), cuda.Out(d_out),
                 grid=(self.hidden_size, 1, 1), block=(self.input_size, 1, 1))

        # hidden node에 대한 수정된 weight 구하기
        weights = []
        for i in range(self.hidden_size):
            weights.extend(self.neuron_layers[0][i].weights)

        d_output_deltas = d_out
        d_weight = numpy.asarray(weights, numpy.float32)
        d_training_rate = numpy.float32(training_rate)

        adjust_neuron(cuda.InOut(d_weight), cuda.In(d_output_deltas), d_training_rate,
                      grid=(self.genre_num, 1, 1), block=(self.hidden_size + 1, 1, 1))

        weights = d_weight.tolist()

        for i in range(self.hidden_size):
            self.neuron_layers[0][i].weights = weights[i * (self.input_size + 1): (i + 1) * (self.input_size + 1)]

        return deviations, outputs

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

    def train_with_book(self, trainig_set, n = 10000, error = 0.0001) :
        genre_list = [genre for item in trainig_set
                       for genre in item["genre"]]
        genre_list = set(genre_list)

        self.genre_num = len(genre_list)
        output_layer = [neuron([random.random() * 2 - 1 for _ in range(self.hidden_size + 1)])
                        for _ in range(self.genre_num)]
        self.neuron_layers[1] = output_layer

        print(genre_list)
        num_counts = count_word_num(trainig_set)
        num_counts.sort(key=lambda x : x[1], reverse=True)

        num_counts = num_counts[:self.input_size]

        print("word_count done")

        for i in range(self.input_size) :
            self.wordtoindex_dic[num_counts[i][0]] = i

        for i, genre in enumerate(list(genre_list)) :
            self.genretoindex_dic[genre] = i

        inputs, targets = self.adjust_train_set(trainig_set)

        print("trainset adjustment finished")

        self.train(inputs, targets, n, error)

        print("train succeed")
        print(self.neuron_layers)

    def train(self, training_set, target_set, n = 10000, error = 0.0001) :
        bef_outputs = [[0 for _ in range(len(target_set[0]))]
                      for _ in range(len(training_set))]
        for i in range(n) :
            deviations = []
            j = 0
            for input_vector, target_vector in zip(training_set, target_set) :
                deviation, output = self.backpropagate(input_vector, target_vector, bef_outputs[j])
                deviations.append(deviation)
                bef_outputs[j] = output
                j += 1

            print("train cycle {} finished".format(i))
            print("cur ouput is {}".format(bef_outputs))
            print("cur deviation is {}".format(sum(deviations)))

            if sum(deviations) <= error :
                print("this network is trained enough")
                break

    def train_relu(self, training_set, target_set, n = 10000, error = 0.0001) :
        bef_outputs = [[0 for _ in range(len(target_set[0]))]
                       for _ in range(len(training_set))]
        for i in range(n):
            deviations = []
            j = 0
            for input_vector, target_vector in zip(training_set, target_set):
                deviation, output = self.backpropagate_relu(input_vector, target_vector, bef_outputs[j])
                deviations.append(deviation)
                bef_outputs[j] = output
                j += 1

            print("train cycle {} finished".format(i))
            print("cur ouput is {}".format(bef_outputs))
            print("cur deviation is {}".format(sum(deviations)))

            if sum(deviations) <= error:
                print("this network is trained enough")
                break


    def classify(self, book) :
        '''
        학습된 신경망으로 책의 장르를 자동으로 분류하는 함수
        :param book: 분류할 책의 book_data 객체
        :return: [(genre name(str), probability(float))] 형태의 리스트로 반환
        '''
        print(book.title)
        input_vector = [0 for _ in range(self.input_size)]
        word_list = tokenize_book(book)
        for word in word_list:
            if word in self.wordtoindex_dic.keys():
                input_vector[self.wordtoindex_dic[word]] = 1
            else:
                print("{} 단어는 학습 대상이 아님".format(word))

        outputs = self.feed_forward(input_vector)
        indextogenre_dic = {idx : genre for genre, idx in self.genretoindex_dic.items()}
        return [(indextogenre_dic[i], outputs[-1][i]) for i in range(len(outputs[-1]))]