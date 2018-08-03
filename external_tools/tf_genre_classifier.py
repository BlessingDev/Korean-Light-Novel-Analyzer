from external_tools.tf_model import FC_Model
from external_tools import genre_classifier

import tensorflow as tf
import numpy as np

class tf_genre_classifier(genre_classifier.genre_classifier) :
    def __init__(self) :
        genre_classifier.genre_classifier.__init__(self)
        self.model = None

    def train(self, input_sets, target_sets, n=1000, error=0.1) :
        sess = tf.Session()
        self.model = FC_Model(sess, "genre_classifier", len(input_sets[0]), len(target_sets[0]), 5, [1000, 1000, 800, 800, 800])

        for i in range(n) :
            c, _ = self.model.train(np.asarray(input_sets), np.asarray(target_sets))

            if i % 10 == 0 :
                print(i, c)

            if c < error :
                print("error condition is satisfied")
                break

    def genre_hot(self, output) :
        cut_val = 0.3
        gl = []
        for g, p in output:
            if p >= cut_val:
                gl.append(g)

        return gl

    def classify(self, book) :
        input_vector = genre_classifier.adjust_book(book)

        output = self.model.predict(input_vector)
        output = tf.reshape(output, [len(genre_classifier.index_to_genre)])

        output = output.tolist()
        genre_prob = [(genre_classifier.index_to_genre[i], p) for i, p in enumerate(output)]