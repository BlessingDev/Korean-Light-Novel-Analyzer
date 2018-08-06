from external_tools.tf_model import FC_Model
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

        self.model = FC_Model(self.sess, "genre_classifier", len(input_sets[0]), len(target_sets[0]),
                              20, [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 1800, 1800, 1800, 1800, 1800, 1800, 1600, 1600, 1300, 1000],
                              learning_rate=0.000001, activation=tf.sigmoid)
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
        cut_val = 0.3
        gl = []
        for g, p in output:
            if p >= cut_val:
                gl.append(g)

        return gl

    def classify(self, book) :
        input_vector = genre_classifier.adjust_book(book, self.input_num)

        output = self.model.predict(np.asarray([input_vector]))
        output = self.sess.run(tf.reshape(output, [len(genre_classifier.index_to_genre)]))

        output = output.tolist()
        print(output)
        genre_prob = [(genre_classifier.index_to_genre[i], p) for i, p in enumerate(output)]

        return genre_prob