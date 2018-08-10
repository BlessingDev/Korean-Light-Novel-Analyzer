from external_tools.tf_model import Softmax_Model, FC_Model
from external_tools import genre_classifier

import tensorflow as tf
import numpy as np

class tf_genre_classifier(genre_classifier.genre_classifier) :
    def __init__(self) :
        genre_classifier.genre_classifier.__init__(self)
        self.input_num = 0
        self.genre_num = 0

        self.model = None
        self.sess = None

    def train(self, input_sets, target_sets, n=1000, error=0.1) :

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=config)

        self.model = Softmax_Model(self.sess, "genre_classifier", len(input_sets[0]), len(target_sets[0]),
                              5, [1200, 800, 500, 500, 500],
                              learning_rate=0.00001, activation=tf.nn.tanh)

        self.input_num = len(input_sets[0])
        self.genre_num =  len(target_sets[0])

        self.sess.run(tf.global_variables_initializer())

        writer = tf.summary.FileWriter('./logs')
        writer.add_graph(self.sess.graph)

        if n != 0 :
            for i in range(n) :
                c, s, _ = self.model.train(np.asarray(input_sets), np.asarray(target_sets))

                writer.add_summary(s, global_step=i)

                if i % 10 == 0 :
                    print(i, c)

                if c < error :
                    print("error condition is satisfied")
                    break
        else :
            c = 10000
            i = 0
            while c > error :
                c, s, _ = self.model.train(np.asarray(input_sets), np.asarray(target_sets))

                writer.add_summary(s, global_step=i)

                if i % 10 == 0:
                    print(i, c)

                i += 1

            print(c, "error condition is satisfied")

    def genre_hot(self, output) :
        cut_val = 0.1
        acc_max = 0.8
        gl = []
        acc_p = 0.0
        output = sorted(output, key=lambda x : x[1], reverse=True)
        print(output)
        for g, p in output:
            if p >= cut_val :
                gl.append(g)
            acc_p += p

            if acc_p >= acc_max :
                break


        return gl

    def classify(self, book) :
        input_vector = genre_classifier.adjust_book_input(book, self.input_num)

        output = self.model.predict(np.asarray([input_vector]))
        output = self.sess.run(tf.reshape(output, [len(genre_classifier.index_to_genre)]))

        output = output.tolist()
        genre_prob = [(genre_classifier.index_to_genre[i], p) for i, p in enumerate(output)]

        return genre_prob