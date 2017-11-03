import book_data, crawler, nlp_module, visualization

#books = crawler.crawl_korean_novel_page()

#print(books.title_list[0])

def show_menu() :
    print("------라이트 노벨 분석기 v. 0.1------")
    print("1. 데이터 전체 크롤")
    print("2. 제목 보기")
    print("3. 책 정보 보기")
    print("4. 검색 정확도 검사")
    print("5. 프로그램 종료")
    print("6. error_code 시각화")
    print("--------------------------------------")


if __name__ == '__main__' :
    open_program = True
    storer = book_data.book_storer()
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
            visualization.show_search_accuracy(storer)

        elif choice == '5' :
            print("프로그램을 종료합니다")
            storer.export_data()
            open_program = False
        elif choice == '6' :
            visualization.show_error_code(storer.get_error_codes())
