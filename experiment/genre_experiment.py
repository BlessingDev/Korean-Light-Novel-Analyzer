from matplotlib import pyplot as plt
import matplotlib.font_manager as fm

import matplotlib

from external_tools import genre_classifier

font_location = "HANDotum.ttf"
font_name = fm.FontProperties(fname = font_location).get_name()
matplotlib.rc('font', family=font_name)

inited = False
word_list = []
book_word = []

def init(training_set) :
    global word_list, book_word, inited
    if not inited :
        inited = True
        num_counts = genre_classifier.count_word_num(training_set)
        num_counts = sorted(num_counts, key=lambda x: x[1], reverse=True)

        word_list = [nc for nc in num_counts if nc[1] > 1.0]

        book_word = [(t["book"], t["genre"], genre_classifier.tokenize_book(t["book"])) for t in training_set]



def word_to_word_genre_scatter(training_set, genre_index, start_num = 0, word_to_compare=5) :

    init(training_set)

    num_counts = word_list

    print(len(num_counts), num_counts)


    g = genre_classifier.index_to_genre[genre_index]


    ap_book = [e for e in book_word if g in e[1]]

    fig = plt.figure()

    fig.suptitle("{0} 장르의 단어({1}~{2}) 산포도".format(g, start_num, start_num + word_to_compare))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.07, top=0.9, hspace=0.5, wspace=0.2)

    for i in range(word_to_compare) :
        for j in range(word_to_compare) :
            ax = plt.subplot(word_to_compare, word_to_compare, i * word_to_compare + j + 1)
            w1 = num_counts[start_num + i][0]
            w2 = num_counts[start_num + j][0]

            ap_xy = []
            for b, gl, wl in ap_book:
                p1 = 0
                p2 = 0

                if w1 in wl:
                    p1 = 1 / len(gl)
                if w2 in wl:
                    p2 = 1 / len(gl)

                ap_xy.append((b.title, p1, p2))

            print(w1, w2, ap_xy)

            ax.set_xlabel(w1)
            ax.set_ylabel(w2)
            ax.set_xlim(xmin=0.0, xmax=1.0)
            ax.set_ylim(ymin=0.0, ymax=1.0)
            ax.scatter([x[1] for x in ap_xy], [x[2] for x in ap_xy])

    plt.show()