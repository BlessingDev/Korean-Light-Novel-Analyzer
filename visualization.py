from matplotlib import pyplot as plt
from collections import Counter

import nlp_module

def show_error_code(error_list) :
    error_count = Counter(error_list)

    print("keys: {}".format(error_count.keys()))
    print("items: {}".format(error_count.items()))

    xs = [i + 0.1 for i, _ in enumerate(error_count.keys())]

    plt.bar(xs, [x[1] for x in error_count.items()])
    plt.ylabel("# of error")
    plt.xlabel("kind of error")

    plt.xticks([i + 0.1 for i, _ in enumerate(error_count.keys())], ["error_code:{}".format(x) for x in error_count.keys()])
    plt.show()

def show_search_accuracy(storer) :
    result_list= list()
    for book in storer.get_ordinary_book() :
        result_list.append(nlp_module.search_accsuracy_examine(book))

    def devide_range(pro) :
        if pro >= 0.8 :
            return 1
        elif pro >= 0.6 :
            return 2
        elif pro >= 0.4 :
            return 3
        elif pro >= 0.2 :
            return 4
        else :
            return 5

    histogram = Counter([devide_range(x) for x in result_list])

    print("items: {}".format(histogram.items()))

    xs = [i + 0.1 for i, _ in enumerate(histogram.keys())]

    plt.bar(xs, [x[1] for x in histogram.items()])
    plt.ylabel("# of accuracy")
    plt.xlabel("accuracy range")

    plt.xticks([i + 0.1 for i, _ in enumerate(histogram.keys())],
               ["range:{}".format(x) for x in histogram.keys()])
    plt.show()
