import random

import book_data, crawler, visualization, GenreClassifier

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


if __name__ == "__main__" :
    open_program = True
    storer = book_data.book_storer()
    v = visualization.WordFrequencyVisualizer()
    bg = GenreClassifier.bayes_GenreClassifier()
    bg.import_data()
    storer.import_data()

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
            open_program = False
        elif choice == '6' :
            visualization.book_published_by_month(storer)
        elif choice == '7' :
            usable_set = [{"book" : t_set["book"], "genre" : t_set["genre"]} for t_set in storer.training_set
                     if len(t_set["genre"]) > 0]

            visualization.word_count_pareto(usable_set, k=0.7)
        elif choice == '8' :
            g = GenreClassifier.neuron_classifier(input_size=511, num_hidden=300, output_size=len(bg.genre_list.keys()))

            g.feed_forward([])

            usable_set = [{"book": t_set["book"], "genre": t_set["genre"]} for t_set in storer.training_set
                          if len(t_set["genre"]) > 0]
            random.shuffle(usable_set)

            train_data, test_data = split_data(usable_set, 0.9)
            print(train_data)
            print(test_data)

            g.train_with_book(train_data, bg.genre_list, n=1000)

            for test in test_data :
                genre_prob = g.classify(test["book"])

                print(genre_prob)
                print(test["genre"])
        elif choice == '9':
            crawler.crawl_certain_time('2012년 7월', '2012년 7월', storer)

        elif choice == '10' :
            g = GenreClassifier.neuron_classifier(input_size = 2, num_hidden = 2, output_size=1)

            input_vectors = [[0, 0], [1, 1], [1, 0], [0, 1]]
            target_vectors = [[0], [0], [1], [1]]

            while(True):
                choice = input("1. 결과보기 2. 학습 3. 종료")

                if choice == '1' :
                    choice = input("index ")
                    choice = int(choice) % 4

                    print("{}: {}".format(input_vectors[choice], g.feed_forward(input_vectors[choice])))
                elif choice == '2' :
                    g.train(input_vectors, target_vectors)
                elif choice == '3' :
                    break