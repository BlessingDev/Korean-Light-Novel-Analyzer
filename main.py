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


if __name__ == "__main__" :
    open_program = True
    storer = book_data.book_storer()
    g = GenreClassifier.GenreClassifier()
    g.import_data()
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
            g.export_data()
            open_program = False
        elif choice == '6' :
            visualization.show_search_accuracy(storer, renew=False)
        elif choice == '7' :
            usable_set = [{"book" : t_set["book"], "genre" : t_set["genre"]} for t_set in storer.training_set
                     if len(t_set["genre"]) > 0]

            g.train(usable_set)
        elif choice == '8' :
            index = int(input("보고 싶은 책의 인덱스 : "))

            book = storer.get_ordinary_book()[index]
            print(book.__str__())
            #print([genre for genre, prob in g.classify(book) if prob > 0.3])
            print(g.classify(book))
