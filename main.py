import book_data, crawler

#books = crawler.crawl_korean_novel_page()

#print(books.title_list[0])

def show_menu() :
    print("------라이트 노벨 분석기 v. 0.0.1------")
    print("1. 제목 크롤링")
    print("2. 제목 보기")
    print("3. 프로그램 종료")
    print("--------------------------------------")


if __name__ == '__main__' :
    open_program = True
    storer = book_data.book_storer()

    while(open_program) :
        show_menu()
        choice = input("무엇을 선택하시겠습니까? ")

        if choice == '1' :
            storer = crawler.crawl_korean_novel_page()
            print("크롤 완료")
        elif choice == '2' :
            print(storer.title_list)
        elif choice == '3' :
            print("프로그램을 종료합니다")
            storer.export_data()
            open_program = False