import tensorflow as tf
from abc import *

class NNModel :
    def __init__(self, sess, name, input_num, output_num, learning_rate=0.01, activation=tf.nn.relu) :
        self.sess = sess
        self.name = name
        self.input_num = input_num
        self.output_num = output_num
        self.learning_rate = learning_rate
        self.activation = activation

    @abstractmethod
    def _build_net(self) :
        '''
        This function build net for Neural Network
        신경망을 구축하는 함수
        :return: None
        '''

    @abstractmethod
    def predict(self, x_datas, keep_prob=1.0) :
        '''
        This function proccess NN with x_data
        x_datas로 모델을 실행시켜 입력값에 대한 예측값을 얻습니다
        :param x_datas: ndarray [N, input_num]
        :param keep_prob: dropout_prob
        :return: ndarray [N, output_num]
        '''

    @abstractmethod
    def get_accuracy(self, x_test, y_test, keep_prob=1.0) :
        '''
        This function gives accuracy of the model
        모델의 정확도(0~1)를 측정하는 함수
        :param x_test: ndarray [N, input_num]
        :param y_test: ndarray [N, output_num]
        :param keep_prob: dropout prob (0.0~1.0)
        :return: 0.0~1.0
        '''

    @abstractmethod
    def train(self, x_data, y_data, keep_prob=0.7) :
        '''
        This function trains the model
        모델을 훈련시키는 함수
        :param x_data: ndarray [N, input_num]
        :param y_data: ndarray [N, output_num]
        :param keep_prob: dropout prob (0.0~1.0)
        :return: cost, state
        '''


class FC_Model(NNModel) :
    def __init__(self, sess, name, input_num, output_num, hidden_num, hidden_node_nums, learning_rate=0.01, activation=tf.nn.relu) :
        '''
        Fully Connected 신경망 모델 초기화 함수
        :param sess: tensorflow 세션
        :param name: 신경망의 이름
        :param input_num: 입력 노드의 개수
        :param output_num: 출력 노드의 개수
        :param hidden_num: 숨겨진 레이어의 개수
        :param hidden_node_num: [숨겨진 레이어의 노드 개수]
        '''
        super().__init__(sess, name, input_num, output_num, learning_rate, activation)

        self.hidden_num = hidden_num
        self.hidden_node_nums = hidden_node_nums

        self._build_net()


    def _build_net(self) :
        with tf.variable_scope(self.name) :
            self.keep_prob = tf.placeholder(tf.float32)

            self.X = tf.placeholder(tf.float32, [None, self.input_num])
            self.Y = tf.placeholder(tf.float32, [None, self.output_num])

            bef_input_num = self.input_num
            bef_output = self.X
            for i in range(self.hidden_num) :
                with tf.variable_scope("Layer{0}".format(i + 1)) :
                    W = tf.Variable(tf.random_normal([bef_input_num, self.hidden_node_nums[i]]), name='weight{0}'.format(i + 1))
                    b = tf.Variable(tf.random_normal([self.hidden_node_nums[i]]), name='bias{0}'.format(i + 1))
                    L = self.activation(tf.matmul(bef_output, W) + b)
                    L = tf.nn.dropout(L, keep_prob=self.keep_prob)
                    bef_output = L
                    bef_input_num = self.hidden_node_nums[i]

            Wl = tf.Variable(tf.random_normal([self.hidden_node_nums[-1], self.output_num]), name='last_weight')
            bl = tf.Variable(tf.random_normal([self.output_num]), name='last_bias')
            self.hypothesis = tf.sigmoid(tf.matmul(bef_output, Wl) + bl, name='hypothesis')

        self.cost = tf.reduce_mean(tf.square(self.hypothesis - self.Y), name='cost')
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)

        correct_prediction = tf.equal(tf.cast(self.hypothesis > 0.5, dtype=tf.float32), self.Y)
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

        self.hy_hist = tf.summary.histogram("hypothesis", self.hypothesis)
        self.cost_summ = tf.summary.scalar("cost", self.cost)

        self.summary = tf.summary.merge_all()

    def predict(self, x_test, keep_prob=1.0) :
        return self.sess.run(self.hypothesis,
                             feed_dict={self.X: x_test, self.keep_prob: keep_prob})

    def get_accuracy(self, x_test, y_test, keep_prob=1.0) :
        return self.sess.run(self.accuracy,
                             feed_dict={self.X: x_test, self.Y: y_test, self.keep_prob: keep_prob})

    def train(self, x_data, y_data, keep_prob=0.7) :
        return self.sess.run([self.cost, self.summary, self.optimizer],
                             feed_dict={self.X: x_data, self.Y: y_data, self.keep_prob: keep_prob})

class SoftmaxModel(NNModel) :
    def __init__(self, sess, name, input_num, output_num, hidden_num, hidden_node_nums, learning_rate=0.01, activation=tf.nn.relu) :
        '''
                Fully Connected 신경망 모델 초기화 함수
                :param sess: tensorflow 세션
                :param name: 신경망의 이름
                :param input_num: 입력 노드의 개수
                :param output_num: 출력 노드의 개수
                :param hidden_num: 숨겨진 레이어의 개수
                :param hidden_node_num: [숨겨진 레이어의 노드 개수]
                '''
        super().__init__(sess, name, input_num, output_num, learning_rate, activation)

        self.hidden_num = hidden_num
        self.hidden_node_nums = hidden_node_nums

        self._build_net()

    def _build_net(self) :
        with tf.variable_scope(self.name) :
            self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

            self.X = tf.placeholder(tf.float32, [None, self.input_num], name='x')
            self.Y = tf.placeholder(tf.float32, [None, self.output_num], name='y')

            bef_input_num = self.input_num
            bef_output = self.X
            for i in range(self.hidden_num) :
                with tf.variable_scope("Layer{0}".format(i + 1)) :
                    W = tf.get_variable('W{0}'.format(i + 1), shape=[bef_input_num, self.hidden_node_nums[i]],
                                        initializer=tf.contrib.layers.xavier_initializer())
                    b = tf.Variable(tf.random_normal([self.hidden_node_nums[i]]), name='b{0}'.format(i + 1))
                    L = self.activation(tf.matmul(bef_output, W) + b)

                    tf.summary.histogram("weights", W)
                    tf.summary.histogram("bias", b)
                    tf.summary.histogram("activations", L)

                    L = tf.nn.dropout(L, keep_prob=self.keep_prob)

                    bef_output = L
                    bef_input_num = self.hidden_node_nums[i]

            with tf.variable_scope("OutputLayer"):
                Wl = tf.get_variable('lW', shape=[bef_input_num, self.output_num],
                                        initializer=tf.contrib.layers.xavier_initializer())
                bl = tf.Variable(tf.random_normal([self.output_num]), name='last_bias')
                self.logits = tf.matmul(bef_output, Wl) + bl
                self.hypothesis = tf.nn.softmax(self.logits, name='hypothesis')

                tf.summary.histogram("weights", Wl)
                tf.summary.histogram("bias", bl)
                tf.summary.histogram("pred", self.hypothesis)

        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.Y))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)

        correct_prediction = tf.equal(tf.cast(self.hypothesis > 0.5, dtype=tf.float32), self.Y)
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

        tf.summary.histogram("hypothesis", self.hypothesis)
        tf.summary.scalar("cost", self.cost)
        tf.summary.scalar("accuracy", self.accuracy)

        self.summary = tf.summary.merge_all()

    def predict(self, x_test, keep_prob=1.0) :
        return self.sess.run(self.hypothesis,
                             feed_dict={self.X: x_test, self.keep_prob: keep_prob})

    def get_accuracy(self, x_test, y_test, keep_prob=1.0) :
        return self.sess.run(self.accuracy,
                             feed_dict={self.X: x_test, self.Y: y_test, self.keep_prob: keep_prob})

    def train(self, x_data, y_data, keep_prob=0.7) :
        return self.sess.run([self.cost, self.summary, self.optimizer],
                             feed_dict={self.X: x_data, self.Y: y_data, self.keep_prob: keep_prob})

class RestoredModel(NNModel) :
    def __init__(self, sess, file_name, input_num, output_num) :
        super().__init__(sess, file_name, input_num, output_num)

        saver = tf.train.import_meta_graph(file_name)
        saver.restore(sess, tf.train.latest_checkpoint('./'))

        graph = tf.get_default_graph()
        self.X = graph.get_tensor_by_name('genre_classifier/x:0')
        self.Y = graph.get_tensor_by_name('genre_classifier/y:0')
        self.keep_prob = graph.get_tensor_by_name('genre_classifier/keep_prob:0')
        self.hypothesis = graph.get_tensor_by_name("genre_classifier/OutputLayer/hypothesis:0")
        self.accuracy = graph.get_tensor_by_name("accuracy:0")

    def predict(self, x_test, keep_prob=1.0):
        return self.sess.run(self.hypothesis,
                             feed_dict={self.X: x_test, self.keep_prob: keep_prob})

    def get_accuracy(self, x_test, y_test, keep_prob=1.0):
        return self.sess.run(self.accuracy,
                             feed_dict={self.X: x_test, self.Y: y_test, self.keep_prob: keep_prob})

    def train(self, x_data, y_data, keep_prob=0.7) :
        print('This is restored graph!')
        return None