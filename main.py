import random, sys, subprocess, os
from PyQt5 import QtCore, QtGui, QtWidgets

import book_data, book_storer, visualization, book_cluster, bookdata_searcher
from external_tools import cuda_genre_classifier
from experiment_tools_instantiater import external_tools_instantiater as exins
from experiment import genre_experiment

from forms import main_ui, search_ui, bookinfo_ui, result_ui, visualization_ui, crawl_ui


def show_menu() :
    print("------라이트 노벨 분석기 v. 0.1------")
    print("1. renew")
    print("2. ordinary_set")
    print("3. search")
    print("4. 정확도 특정 범위의 책 보기")
    print("5. 프로그램 종료")
    print("6. 검색 정확도 시각화")
    print("7. 장르 분류기 학습")
    print("8. 장르 자동 분류")
    print("--------------------------------------")

def split_data(li, rate) :

    border = int(round(len(li) * rate, 0))
    print(border)
    return li[:border], li[border:]

def classify_genre(g, storer) :
    if g is not None:
        ordinary_books = storer.get_ordinary_book()

        book_idx = input("장르를 분류하고 싶은 책의 인덱스 입력 ")
        book_idx = int(book_idx)
        book_idx = book_idx % len(ordinary_books)

        genre_prob = g.classify(ordinary_books[book_idx])
        print(genre_prob)
    else:
        print("g is None")

def networktest() :
    g = exins.get_instance().get_genre_classifier_cuda_instance("xor")


    input_vectors = [[0, 0], [1, 1], [1, 0], [0, 1]]
    target_vectors = [[0], [0], [1], [1]]

    while (True):
        choice = input("1. 결과보기 2. 학습 3. 종료")

        if choice == '1':
            results = [g._feed_forward_relu(input_vectors[i]) for i in range(4)]

            print("{}: {}".format(input_vectors[0], results[0][-1]))
            print("{}: {}".format(input_vectors[1], results[1][-1]))
            print("{}: {}".format(input_vectors[2], results[2][-1]))
            print("{}: {}".format(input_vectors[3], results[3][-1]))

            deviation = sum([(result[-1][0] - target_vectors[i][0]) ** 2 for i, result in enumerate(results)])
            print("deviation is {}".format(deviation))
            print()
        elif choice == '2':
            g.train_relu(input_vectors, target_vectors)
        elif choice == '3':
            break

def cluster_book(bc, storer) :
    bc.set_real_dist(storer.get_ordinary_book())
    print("dist 구하기 종료")
    bc.scaledown(rate=0.0002, trainn = 5000)
    print("2D 투영 종료")

    bc.visualize()
    print("이미지 출력 종료")

def book_search(bs, storer, n=10) :
    title = input("검색할 책의 제목을 적어주세요 ")

    searchedlist = bs.search_book_by_title(title, n=n)

    booklist = storer.get_ordinary_book()

    # GUI로 변경시에 이 부분을 함수로 만들어 리스트로 보여주게 할 것
    print(["{} : {}회 등장".format(booklist[i].title, n) for i, n in searchedlist])

    idx = input("선택할 책 인덱스(0~{}) ".format(n - 1))
    idx = int(idx)

    return (searchedlist[idx][0], booklist[searchedlist[idx][0]])

def get_close_book(bc, bs, storer) :
    idx, book = book_search(bs, storer)

    closelist = bc.get_close_books(idx)
    booklist = storer.get_ordinary_book()

    if closelist is not None :
        print([(booklist[i].title, dist) for i, dist in closelist])

def crawl_book(g, bc, bs) :
    cw = exins.get_instance().get_crawler_namu_instance()
    storer = cw.crawl_whole_korean_novel()
    renew_datas(storer, g, bc, bs)

    return storer

def renew_datas(storer, g, bc, bs) :
    storer.classify_book_genre(g)
    storer.download_images()
    bc.set_real_dist(storer.get_ordinary_book())
    bs.init_word_index(storer.get_ordinary_book())

def crawl_search_sample() :
    book = book_data.BookData()
    sr = exins.get_instance().get_searcher_naver_instance()
    sr.book = book
    sr.from_title('시원찮은 그녀를 위한 육성방법 GS 2권')

def cui_main(v, g, bc, bs, storer) :
    open_program = True

    while (open_program):
        show_menu()
        choice = input("무엇을 선택하시겠습니까? ")

        if choice == '1':
            cw = exins.get_instance().get_crawler_namu_instance()
            storer = cw.crawl_whole_korean_novel()
            renew_datas(storer, g, bc, bs)
            print("크롤 완료")
        elif choice == '2':
            print([book.title for book in storer.get_ordinary_book()])
            print("len: ", len(storer.get_ordinary_book()))

        elif choice == '3':
            print(book_search(bs, storer))

        elif choice == '4':
            start = float(input("시작범위(1.0-0.0) "))
            end = float(input("종료범위(1.0-0.0) "))

            i = 0
            for book in storer.book_list:
                i += 1
                if book.search_accuracy >= start and \
                                book.search_accuracy <= end:
                    print("index: {}".format(i))
                    print(book.__str__())
                    print(book.search_accuracy)
                    print()

        elif choice == '5':
            print("프로그램을 종료합니다")
            storer.export_data()
            if (g is not None):
                g.export_data()
            bc.export_data()
            bs.export_data()
            open_program = False
        elif choice == '6':
            visualization.show_error_code(storer.get_error_codes())
            visualization.show_search_accuracy(storer)
        elif choice == '7':
            usable_set = [{"book": t_set["book"], "genre": t_set["genre"]} for t_set in storer.training_set
                          if len(t_set["genre"]) > 0]

            # visualization.word_count_pareto(usable_set, k=0.8)
            genre_num, start_num = input("비교할 장르 번호, 단어 번호를 적어주세요: ").split(' ')
            genre_experiment.word_to_word_genre_scatter(usable_set, int(genre_num), start_num=int(start_num))
        elif choice == '8':
            g = cuda_genre_classifier.cuda_classifier(511, 300, 1)

            usable_set = [{"book": t_set["book"], "genre": t_set["genre"]} for t_set in storer.training_set
                          if len(t_set["genre"]) > 0]
            random.shuffle(usable_set)

            train_data, test_data = split_data(usable_set, 0.9)
            print(train_data)
            print(test_data)

            g.examine(test_data)
        elif choice == '9':
            i, book = book_search(bs, storer, n=20)
            print("idx = " + i.__str__())
            print(book.__str__())

        elif choice == '10':
            bc.set_real_dist(storer.get_ordinary_book())
            #bc.visualize()

        elif choice == '11':
            get_close_book(bc, bs, storer)
        elif choice == '12':
            storer.classify_book_genre(g)
        elif choice == '13' :
            crawl_search_sample()
        elif choice == '14':
            cw = exins.get_instance().get_crawler_namu_instance()
            books = cw.crawl_selected_month(['2017년 6월'])
            storer.add_books_by_title(books)



def gui_main(v, g, bc, bs, storer) :
    mainui = None
    searchui = None
    searchList = None

    def mainList(ui):
        uis = [
            "특정기간 책 크롤",
            "책 검색",
            "시각화"
        ]

        model = QtGui.QStandardItemModel(ui.listView)

        for uiitem in uis:
            item = QtGui.QStandardItem(uiitem)

            model.appendRow(item)

        ui.listView.setModel(model)

    def mainText(modelIndex):
        explains = [
            ["특정기간 책 크롤",
             "특정 기간의 책을 크롤해서 자동으로 데이터를 추가한다."],
            ["책 검색",
             "책 제목을 검색하여 여러가지 작업을 수행한다."],
            ["시각화",
             "여러가지 시각화 결과를 본다."]
        ]

        # print(modelIndex.row())
        mainui.textBrowser.clear()
        curexplain = explains[modelIndex.row()]
        for line in curexplain:
            mainui.textBrowser.append(line)

    def onClick(bool=False) :

        def onSearchClick(bool=False):
            global searchList

            curNum = searchui.comboBox.currentIndex()
            curNum += 1
            searchWord = searchui.lineEdit.text()

            searchList = bs.search_book_by_title(searchWord, n=curNum)

            books = storer.get_ordinary_book()

            model = QtGui.QStandardItemModel(searchui.listView)

            for index, _ in searchList:
                item = QtGui.QStandardItem(books[index].title)

                model.appendRow(item)

            searchui.listView.setModel(model)
            scene = QtWidgets.QGraphicsScene()
            searchui.graphicsView.setScene(scene)
            searchui.graphicsView.show()

        def on_list_clicked(modelIndex) :
            global searchList
            curindex = modelIndex.row()
            curbook = storer.get_ordinary_book()[searchList[curindex][0]]
            image = QtGui.QPixmap(curbook.get_image_dir())

            scene = QtWidgets.QGraphicsScene()
            scene.addItem(QtWidgets.QGraphicsPixmapItem(image))
            view = searchui.graphicsView
            view.setScene(scene)
            view.show()

        def on_book_selected(bool=False) :
            global searchList
            global g
            global bc
            def on_action_clicked(bool=False) :
                curindex = bookui.listView.currentIndex().row()

                if curindex == 0 :
                    print('자동장르분류')
                    problist = [x for x in g.classify(selected_book) if x[1] >= 0.0001]
                    problist = sorted(problist, key=lambda x : x[1], reverse=True)

                    widget = QtWidgets.QDialog()
                    resui = result_ui.Ui_Form()
                    resui.setupUi(widget)

                    model = QtGui.QStandardItemModel(resui.listView)
                    for genre, prob in problist :
                        item = QtGui.QStandardItem("장르: {}, 확률: {:.4f}%".format(genre, prob * 100))
                        model.appendRow(item)

                    if len(problist) == 0 :
                        item = QtGui.QStandardItem("0.01%보다 높은 확률을 가지는 장르가 없음")
                        model.appendRow(item)

                    resui.listView.setModel(model)

                    resui.label.setText('장르 자동 분류 결과')

                    widget.show()
                    widget.exec_()
                elif curindex == 1:
                    print('컨텐츠 기반 추천')
                    close_book = bc.get_close_books(searched_index)

                    widget = QtWidgets.QDialog()
                    resui = result_ui.Ui_Form()
                    resui.setupUi(widget)

                    model = QtGui.QStandardItemModel(resui.listView)

                    if close_book is None :
                        item = QtGui.QStandardItem("0.01%보다 높은 확률을 가지는 장르가 없음")
                        model.appendRow(item)
                    else :
                        for bindex, dist in close_book:
                            item = QtGui.QStandardItem("책제목: {}".format(storer.get_ordinary_book()[bindex].title))
                            model.appendRow(item)

                    resui.listView.setModel(model)

                    resui.label.setText('컨텐츠 기반 비슷한 책 상위 10개')

                    widget.show()
                    widget.exec_()

            ###
            curindex = searchui.listView.currentIndex().row()

            selected_book = storer.get_ordinary_book()[searchList[curindex][0]]
            searched_index = searchList[curindex][0]

            widget = QtWidgets.QDialog()
            bookui = bookinfo_ui.Ui_Form()
            bookui.setupUi(widget)
            image = QtGui.QPixmap(selected_book.get_image_dir())

            scene = QtWidgets.QGraphicsScene()
            scene.addItem(QtWidgets.QGraphicsPixmapItem(image))
            view = bookui.graphicsView
            view.setScene(scene)
            view.show()

            infolist = [
                "제목: {}".format(selected_book.title),
                "작가: {}".format(selected_book.author),
                "출판일자: {}".format(selected_book.pubdate),
                "번역가: {}".format(selected_book.translator),
                "출판사: {}".format(selected_book.publisher)
            ]

            for info in infolist :
                bookui.textBrowser.append(info)

            menulist = [
                '자동장르분류',
                '컨텐츠 기반 책 추천'
            ]

            model = QtGui.QStandardItemModel(bookui.listView)
            for menu in menulist :
                item = QtGui.QStandardItem(menu)
                model.appendRow(item)

            bookui.listView.setModel(model)

            bookui.pushButton.clicked.connect(on_action_clicked)

            widget.show()
            widget.exec_()

        def on_vis_clicked(bool=False) :
            curindex = visui.listView.currentIndex().row()

            if curindex == 0 :
                visualization.book_published_by_month(storer)
            elif curindex == 1 :
                visualization.show_search_accuracy(storer)
            elif curindex == 2:
                visualization.show_error_code(storer.get_error_codes())
            elif curindex == 3 :
                genre = visui.lineEdit.text()

                if genre == '' or genre == '장르를 입력해주세요':
                    visui.lineEdit.setText('장르를 입력해주세요')
                else :
                    v.show_genre_word_frequency(storer.training_set, genre)
            elif curindex == 4:
                imgpath = os.path.dirname(os.path.realpath(__file__)) + '\\book_relavant.jpg'

                subprocess.run(['explorer', imgpath])

        def cr_item_changed(item) :
            if item.checkState() == QtCore.Qt.Checked :
                selected_ym.append(item)
            elif item.checkState() == QtCore.Qt.Unchecked :
                selected_ym.remove(item)

        def on_cr_clicked(bool=False) :
            global storer
            ymlist = []
            crui.textBrowser.clear()

            for item in selected_ym :
                ymlist.append(item.text())

            crui.textBrowser.append('크롤 시작')
            cw = exins.get_instance().get_crawler_namu_instance()

            crui.textBrowser.append('크롤된 제목으로 네이버 검색')
            if len(ymlist) == 0 :
                storer = cw.crawl_whole_korean_novel()
            else :
                books = cw.crawl_selected_month(ymlist, pages)
                storer.add_books_by_title(books)

            crui.textBrowser.append('검색 완료')
            crui.textBrowser.append('정보 갱신 시작(책간 거리, 책검색 등)')
            renew_datas(storer, g, bc, bs)
            crui.textBrowser.append('전과정 종료')

        def on_cr_save_clicked(bool=False) :
            print('save clicked')
            storer.export_data()
            if (g is not None):
                g.export_data()
            bc.export_data()
            bs.export_data()

        ###

        curIndex = mainui.listView.currentIndex().row()
        print(curIndex)
        selected_ym = []
        global searchui
        global MainWindow
        if curIndex == 0 :
            cw = exins.get_instance().get_crawler_namu_instance()
            pages = cw.crawl_entire_novel_page()
            selected_ym = []
            widget = QtWidgets.QDialog()
            crui = crawl_ui.Ui_widget()
            crui.setupUi(widget)


            model = QtGui.QStandardItemModel(crui.listView)
            model.itemChanged.connect(cr_item_changed)

            for vis in pages.keys():
                item = QtGui.QStandardItem(vis)
                item.setCheckable(True)

                model.appendRow(item)

            crui.listView.setModel(model)

            crui.pushButton.clicked.connect(on_cr_clicked)
            crui.pushButton_2.clicked.connect(on_cr_save_clicked)

            widget.show()
            widget.exec_()
        elif curIndex == 1 :
            widget = QtWidgets.QDialog()
            searchui = search_ui.Ui_Form()
            searchui.setupUi(widget)
            searchui.pushButton.clicked.connect(onSearchClick)
            searchui.listView.clicked.connect(on_list_clicked)
            searchui.pushButton_2.clicked.connect(on_book_selected)

            widget.show()
            widget.exec_()

        elif curIndex == 2 :
            widget = QtWidgets.QDialog()
            visui = visualization_ui.Ui_Form()
            visui.setupUi(widget)

            vislist = [
                '월별 출판권수 변화 추이',
                '검색된 책의 정확도 그래프',
                '네이버 API 검색에서 일어난 오류 빈도',
                '학습 데이터의 장르별 등장 단어 상위 20개(장르 입력 필요)',
                '책간 컨텐츠 기반 거리 2차원 축소 이미지'
            ]

            model = QtGui.QStandardItemModel(visui.listView)

            for vis in vislist:
                item = QtGui.QStandardItem(vis)

                model.appendRow(item)

            visui.listView.setModel(model)

            visui.pushButton.clicked.connect(on_vis_clicked)


            widget.show()
            widget.exec_()

    ###
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    mainui = main_ui.Ui_MainWindow()
    mainui.setupUi(MainWindow)
    mainList(mainui)
    mainui.listView.clicked.connect(mainText)
    mainui.pushButton.clicked.connect(onClick)

    MainWindow.show()
    app.setQuitOnLastWindowClosed(True)
    app.exec_()




if __name__ == "__main__" :
    storer = book_storer.BookStorer()
    storer.import_data()
    v = visualization.WordFrequencyVisualizer()
    #v.initialize(storer.training_set)
    g = None
    # g.import_data()
    bc = book_cluster.BookCluster()
    bc.import_data()
    bs = bookdata_searcher.BookDataSearcher()
    bs.import_data()

    cui_main(v, g, bc, bs, storer)
    # gui_main(v, g, bc, bs, storer)