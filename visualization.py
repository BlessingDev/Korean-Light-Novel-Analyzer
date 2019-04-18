from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib
from collections import Counter, defaultdict
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import datetime


import paretochart
from external_tools import genre_classifier

# 한글 폰트 추가
font_location = "HANDotum.ttf"
font_name = fm.FontProperties(fname = font_location).get_name()
matplotlib.rc('font', family=font_name)

def show_error_code(error_list) :
    """
    책을 검색할 때 난 에러의 검출수를 시각화하는 함수
    BookStorer.get_error_code와 BookData를 참고
    :param error_list: BookStorer.get_error_code로 반환되는 리스트
    :return: None
    """
    # Counter 객체를 통해 각 에로코드 기준으로 개수를 세 dictionary를 만든다
    error_count = Counter(error_list)

    print("keys: {}".format(error_count.keys()))
    print("items: {}".format(error_count.items()))

    # matplotlib에 전달할 x배열 생성
    xs = [i + 0.1 for i, _ in enumerate(error_count.keys())]

    # matplotlib에 그래프 입력
    plt.bar(xs, [x[1] for x in error_count.items()])
    plt.ylabel("# of error")
    plt.xlabel("kind of error")

    plt.xticks([i + 0.1 for i, _ in enumerate(error_count.keys())], ["error_code:{}".format(x) for x in error_count.keys()])
    plt.show()

def show_search_accuracy(storer, renew = False) :
    """
    BookStorer 객체를 인자로 받아 책의 검색 정확도를 막대 그래프로 시각화하는 함수
    :param storer:
    :param renew: 시각화하기에 앞서 정확도를 갱신할지 여부
    :return:
    """
    if renew :
        storer.renew_accuracy()

    result_list= list()
    for book in storer.get_ordinary_book() :
        result_list.append(book.search_accuracy)

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
    range1patch = mpatches.Patch(label = 'range1: 0.8~1.0')
    range2patch = mpatches.Patch(label = 'range2: 0.6~0.8')
    range3patch = mpatches.Patch(label = 'range3: 0.4~0.6')
    range4patch = mpatches.Patch(label = 'range4: 0.4~0.2')
    range5patch = mpatches.Patch(label = 'range5: 0.0~0.2')

    plt.legend(handles = [range1patch, range2patch, range3patch, range4patch, range5patch])
    plt.bar(xs, [x[1] for x in histogram.items()])
    plt.ylabel("정확도")
    plt.xlabel("accuracy range")

    plt.xticks([i + 0.1 for i, _ in enumerate(histogram.keys())],
               ["range:{}".format(x) for x in histogram.keys()])
    plt.show()



class WordFrequencyVisualizer :
    def __init__(self) :
        self.counts = None

    def initialize(self, training_set) :
        if self.counts is None :
            self.counts = genre_classifier.count_words(training_set)

    def show_genre_word_frequency(self, train_set, show_genre, n=20):
        self.initialize(train_set)
        num_dic = defaultdict(list)

        for word in self.counts.keys():
            for genre in self.counts[word].keys():
                num_dic[genre].append((word, self.counts[word][genre]))

        if show_genre in num_dic.keys() :
            num_dic[show_genre].sort(key=lambda x: x[1], reverse = True)
            print(num_dic[show_genre])

            xs = [i + 0.1 for i in range(n)]
            plt.figure(figsize = (12, 4), dpi = 100)

            plt.title("{} 장르의 단어별 개수 상위 {}개".format(show_genre, n))
            plt.bar(xs, [round(x[1], 2) for x in num_dic[show_genre][:20]])
            plt.ylabel("단어의 개수")
            plt.xlabel("단어")

            plt.xticks(xs, [x[0] for x in num_dic[show_genre][:20]])
            plt.show()
        else :
            print("{} 장르는 없음".format(show_genre))

def word_count_pareto(training_set, k = 0.9) :
    num_counts = genre_classifier.count_word_num(training_set)
    num_counts = sorted(num_counts, key=lambda x : x[1], reverse=True)

    print(num_counts)

    datas = [x[1] for x in num_counts]
    labels = [x[0] for x in num_counts]

    fig, axes = plt.subplots(1, 1)

    paretochart.pareto(datas, labels, axes = axes, limit = k, line_args=('g', ))
    plt.title("단어 개수로 본 파레토 그램 limit={}".format(k), fontsize = 10)

    fig.canvas.set_window_title('Word Count Pareto')
    plt.show()

def book_published_by_month(storer) :
    num_per_date = [(datetime.datetime.strptime(x, '%Y년 %m월'), len(storer.date_to_book[x])) for x in storer.date_to_book.keys()]

    num_per_date = sorted(num_per_date, key=lambda x : x[0])

    dates = ["{}년 {}월".format(x[0].year, x[0].month) for x in num_per_date]
    num_per_date = [x[1] for x in num_per_date]

    xs = [i + 0.1 for i, _ in enumerate(storer.date_to_book.keys())]

    ind = np.arange(len(num_per_date)) * 2
    width = 0.7

    fig, ax = plt.subplots(figsize = (16, 8), dpi = 100)
    rects1 = ax.bar(ind, num_per_date, width, color='b', align = 'edge')

    ax.set_title("라이트 노벨 월별 출간 권수 변화")
    ax.set_ylabel("권수")
    ax.set_xlabel("20OO년\nOO월")
    ax.set_xticks(ind + width / 2)

    date_list = [x.split()[0][2:] + "\n" + x.split()[1]
                 for x in dates]
    ax.set_xticklabels(date_list, size='small')

    plt.show()

def draw2d(data, labels, imagerate = 1000, jpeg = 'mds2d.jpg') :

    font = ImageFont.truetype('HANDotum.ttf', size=15)

    xlist = [data[i][0] for i in range(len(data))]
    ylist = [data[i][1] for i in range(len(data))]

    xlen = max(xlist) - min(xlist)
    ylen = max(ylist) - min(ylist)

    xadd = - min(xlist)
    yadd = - min(ylist)

    xrate = (int(xlen) * imagerate - imagerate / 100) / (max(xlist) + xadd)
    yrate = (int(ylen) * imagerate - imagerate / 100) / (max(ylist) + yadd)

    xadd += imagerate / 200 / xrate
    yadd += imagerate / 200 / yrate

    coordrate = min(xrate, yrate)

    img = Image.new('RGB', (int(xlen) * imagerate, int(ylen) * imagerate), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    for i in range(len(data)) :
        x = (data[i][0] + xadd) * coordrate
        y = (data[i][1] + yadd) * coordrate
        print("{} at ({}, {})".format(labels[i], x, y))
        draw.text((x, y), "\"" + labels[i] + "\"", (0, 0, 0), font = font)
    img.save(jpeg, 'JPEG')