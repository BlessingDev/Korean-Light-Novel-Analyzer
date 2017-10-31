import book_data, crawler
from collections import defaultdict

#books = crawler.crawl_korean_novel_page()

#print(books.title_list[0])

def show_menu() :
    print("------라이트 노벨 분석기 v. 0.0.1------")
    print("1. 제목 크롤링")
    print("2. 제목 보기")
    print("3. 네이버 책 검색에서 정보 받아오기")
    print("4. 책 정보 보기")
    print("5. 프로그램 종료")
    print("--------------------------------------")


if __name__ == '__main__' :
    open_program = True
    storer = book_data.book_storer()

    while(open_program) :
        show_menu()
        choice = input("무엇을 선택하시겠습니까? ")

        if choice == '1' :
            storer = crawler.crawl_whole_korean_novel()
            print("크롤 완료")
        elif choice == '2' :
            print(storer.title_list)
        elif choice == '3' :
            book_list = list()
            for i in range(len(storer.title_list)) :
                data = book_data.book_data()
                book_list.append(data.from_title(storer.title_list[i]))

            storer.book_list = book_list

            book_dict = defaultdict(list)

            for key in storer.date_to_titles.keys() :
                title_list = storer.date_to_titles[key]
                for title in title_list :
                    for book in book_list :
                        if book.ori_title == title :
                            book_dict[key].append(book)

            storer.date_to_book = book_dict
        elif choice == '4':
            print(storer.book_list)
        elif choice == '5' :
            print("프로그램을 종료합니다")
            storer.export_data()
            open_program = False