import random

import book_data, crawler, visualization, GenreClassifier, book_cluster, book_searcher

#books = crawler.crawl_korean_novel_page()

#print(books.title_list[0])

def show_menu() :
    print("------라이트 노벨 분석기 v. 0.1------")
    print("1. 데이터 전체 크롤")
    print("2. 제목 보기")
    print("3. 책 정보 보기")
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
    g = GenreClassifier.neuron_classifier(input_size=2, num_hidden=30, output_size=1)

    input_vectors = [[0, 0], [1, 1], [1, 0], [0, 1]]
    target_vectors = [[0], [0], [1], [1]]

    while (True):
        choice = input("1. 결과보기 2. 학습 3. 종료")

        if choice == '1':
            results = [g.feed_forward_relu(input_vectors[i]) for i in range(4)]

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
    bc.scaledown(rate=0.0001, trainn = 5000)
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

if __name__ == "__main__" :
    open_program = True
    storer = book_data.book_storer()
    v = visualization.WordFrequencyVisualizer()
    storer.import_data()
    g = GenreClassifier.neuron_classifier(1, 1, 1)
    g.import_data()
    bc = book_cluster.BookCluster()
    bs = book_searcher.BookSearcher()
    bs.init_word_index(storer.get_ordinary_book())

    while(open_program) :
        show_menu()
        choice = input("무엇을 선택하시겠습니까? ")

        if choice == '1' :
            storer = crawler.crawl_whole_korean_novel()
            print("크롤 완료")
        elif choice == '2' :
            print(storer.get_title_list())

        elif choice == '3':
            index = int(input("몇 번째 인덱스의 책을 볼까요? "))
            print(storer.book_list[index].__str__())
        elif choice == '4':
            start = float(input("시작범위(1.0-0.0) "))
            end = float(input("종료범위(1.0-0.0) "))

            i = 0
            for book in storer.book_list :
                i += 1
                if book.search_accuracy >= start and \
                    book.search_accuracy <= end :
                    print("index: {}".format(i))
                    print(book.__str__())
                    print(book.search_accuracy)
                    print()

        elif choice == '5' :
            print("프로그램을 종료합니다")
            storer.export_data()
            if(g is not None) :
                g.export_data()
            open_program = False
        elif choice == '6' :
            visualization.book_published_by_month(storer)
        elif choice == '7' :
            usable_set = [{"book" : t_set["book"], "genre" : t_set["genre"]} for t_set in storer.training_set
                     if len(t_set["genre"]) > 0]

            visualization.word_count_pareto(usable_set, k=0.5)
        elif choice == '8' :
            g = GenreClassifier.neuron_classifier(511, 300, 1)

            usable_set = [{"book": t_set["book"], "genre": t_set["genre"]} for t_set in storer.training_set
                          if len(t_set["genre"]) > 0]
            random.shuffle(usable_set)

            train_data, test_data = split_data(usable_set, 0.9)
            print(train_data)
            print(test_data)

            g.train_with_book(train_data, n=5000, error = 5)

            for test in test_data :
                genre_prob = g.classify(test["book"])

                print(genre_prob)
                print(test["genre"])
        elif choice == '9':
            i, book = book_search(bs, storer, n=20)
            print("idx = " + i.__str__())
            print(book.__str__())

        elif choice == '10' :
            cluster_book(bc, storer)

        elif choice == '11' :
            get_close_book(bc, bs, storer)
        elif choice == '12' :
            storer.classify_book_genre(g)