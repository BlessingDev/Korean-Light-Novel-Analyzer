import tensorflow as tf

class FC_Model :
    def __init__(self, sess, name, input_num, output_num, hidden_num, hidden_node_nums, learning_rate=0.01) :
        '''
        Fully Connected 신경망 모델 초기화 함수
        :param sess: tensorflow 세션
        :param name: 신경망의 이름
        :param input_num: 입력 노드의 개수
        :param output_num: 출력 노드의 개수
        :param hidden_num: 숨겨진 레이어의 개수
        :param hidden_node_num: [숨겨진 레이어의 노드 개수]
        '''
        self.sess = sess
        self.name = name
        self.input_num = input_num
        self.output_num = output_num
        self.hidden_num = hidden_num
        self.hidden_node_nums = hidden_node_nums

        self.learning_rate = learning_rate

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
                    L = tf.nn.relu(tf.matmul(bef_output, W) + b)
                    L = tf.nn.dropout(L, keep_prob=self.keep_prob)
                    bef_output = L

            Wl = tf.Variable(tf.random_normal([self.hidden_node_nums[-1], self.output_num]), name='last_weight')
            bl = tf.Variable(tf.random_normal([self.output_num]), name='last_bias')
            self.hypothesis = tf.sigmoid(tf.matmul(bef_output, Wl) + bl)

        self.cost = tf.reduce_mean(tf.square(self.hypothesis - self.Y))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)

        correct_prediction = tf.equal(tf.cast(self.hypothesis > 0.5, dtype=tf.float32), self.Y)
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    def predict(self, x_test, keep_prob=1.0) :
        return self.sess.run(self.hypothesis,
                             feed_dict={self.X: x_test, self.keep_prob: keep_prob})

    def get_accuracy(self, x_test, y_test, keep_prob=1.0) :
        return self.sess.run(self.accuracy,
                             feed_dict={self.X: x_test, self.Y: y_test, self.keep_prob: keep_prob})

    def train(self, x_data, y_data, keep_prob=0.7) :
        return self.sess.run([self.cost, self.optimizer],
                             feed_dict={self.X: x_data, self.Y: y_data, self.keep_prob: keep_prob})