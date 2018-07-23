
from bs4 import BeautifulSoup

import BookStorer, nlp_module, crawler


class NamuNovelCrawler() :
    def __init__(self):
        pass

    def crawl_entire_novel_page(self) :
        '''
        내부 호출용 함수로, 나무위키의 월별 발매 라이트노벨 페이지를 크롤하여
        각 월의 라이트노벨 url list를 반환
        :return: 각 월 라이트노벨 리스트 페이지의 url list
        '''
        pages = {}

        c = crawler.get_html(
            'https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%ED%8A%B8%20%EB%85%B8%EB%B2%A8/%EC%8B%A0%EA%B0%84%20%EB%AA%A9%EB%A1%9D')

        soup = BeautifulSoup(c)

        for td in soup('td'):
            for a in td('a'):
                if ('class' in a.attrs
                    and 'wiki-link-internal' in a['class']
                    and a.get_text()[-1] == '월'):

                    date = ""
                    for parent in a.parents :
                        if parent.name == 'div' and\
                            'class' in parent.attrs and\
                            'wiki-heading-content' in parent['class'] :

                            for sibling in parent.previous_siblings :
                                if sibling.name == 'h2' :
                                    for sa in sibling('a') :
                                        if 'title' in sa.attrs :
                                            date = sa.get_text()
                                            date += " "
                                            break

                                if date != "" :
                                    break

                        if date != "" :
                            break

                    date += a.get_text()

                    pages[date] = ('https://namu.wiki' + a['href'])

        return pages

    def crawl_certain_month_novel(self, url, date) :
        '''
        내부에서 호출하여 나무위키 각월 라이트노벨 발매 페이지를 크롤하는 함수
        :param url: 해당 발매 페이지의 url
        :param date: log를 위한 날짜 string
        :return: 책 제목이 들은 list
        '''
        title_list = list()

        ignore_word = [
            '최근 변경',
            '최근 토론',
            '특수 기능',
            '게시판',
            '작성이 필요한 문서',
            '고립된 문서',
            '분류가 되지 않은 문서',
            '편집된 지 오래된 문서',
            '내용이 짧은 문서',
            '내용이 긴 문서',
            '차단 내역',
            'RandomPage',
            '파일 올리기',
            '라이선스',
            '라이브',
            '설정',
            '어두운 화면으로',
            '내 문서 기여 목록',
            '내 토론 기여 목록',
            '로그인',
            '관련 문서: 라이트 노벨/목록',
            '라이트 노벨/신간 목록'
        ]

        c = crawler.get_html(url)

        i = 0
        while c is None:
            i += 1
            c = crawler.get_html(url)
            print("{}회 재시도".format(i))

        soup = BeautifulSoup(c)

        need_japan_check = False
        for h2 in soup.find_all("h2"):
            if h2.get_text() == "1. 대한민국[편집]":
                need_japan_check = True
                break

        for div in soup('div'):

            if ('class' in div.attrs and
                        'wiki-inner-content' in div['class']):

                for li in div('li'):

                    if need_japan_check:
                        japan_check = False

                        for parent in li.parents:
                            if (parent.name == "div" and 'class' in parent.attrs and
                                    'wiki-heading-content' in parent['class']) or \
                                    parent.name == 'ul':
                                for sibling in parent.previous_siblings:
                                    if sibling.name == 'h2':
                                        if sibling.get_text() != '1. 대한민국[편집]':
                                            print('일본 체크 {0}'.format(sibling.get_text()))
                                            japan_check = True
                                            break

                        if japan_check:
                            break

                    print(li.get_text())
                    book_title = li.get_text().strip()

                    if book_title != "" and (not (book_title in ignore_word)):
                        if '[' in book_title:
                            list_a = book_title.split('[')

                            book_title = list_a[0]

                        if book_title[-1] == ')':
                            list_a = book_title.split('(')

                            book_title = list_a[0]

                        if book_title[-1] == '권':
                            book_title = book_title.split('권')[0]
                        book_title.encode('utf-8 sig')

                        book_title = nlp_module.preprocess_title(book_title)
                        title_list.extend(book_title)

        print("{0} 크롤링 종료".format(date))

        return title_list

    def crawl_whole_korean_novel(self) :
        '''
        외부에서 호출하여 크롤의 결과로 BookStorer 객체를 반환하는 함수
        :return: BookStorer 객체
        '''
        books = BookStorer.BookStorer()
        title_list = list()
        title_to_date = dict()

        page_dic = self.crawl_entire_novel_page()

        for date in page_dic.keys() :
            certain_list = self.crawl_certain_month_novel(page_dic[date], date)
            title_list.extend(certain_list)
            for title in certain_list :
                title_to_date[title] = date

        books.add_by_tl_td(title_list, title_to_date)

        return books

    def crawl_certain_period(self, start_time, end_time) :
        '''
        외부에서 호출하여 일정 기간 동안의 라노베를 크롤하는 함수
        :param start_time: 시작하는 년-월
        :param end_time: 끝나는 년-월
        :return: 책 제목이 들은 list
        '''
        books = []
        page_dic = self.crawl_entire_novel_page()

        if start_time in page_dic.keys() and\
            end_time in page_dic.keys() :


            if start_time == end_time :
                books.extend(self.crawl_certain_month_novel(page_dic[start_time], start_time))
            else:
                start_year = int(start_time.split('년')[0])
                start_month = int(start_time.split()[1].split('월')[0])

                end_year = int(end_time.split('년')[0])
                end_month = int(end_time.split()[1].split('월')[0])
                if (start_year == end_year and start_month <= end_month) or\
                    start_year < end_year :
                    for date in page_dic.keys() :
                        cur_year = int(date.split('년')[0])
                        cur_month = int(date.split()[1].split('월')[0])

                        if (cur_year > start_year and cur_year < end_year) or\
                            (cur_year == start_year and cur_year == end_year and
                            cur_month >= start_month and cur_month <= end_month) or\
                            (cur_year == start_year and cur_month >= start_month) or\
                            (cur_year == end_year and cur_month <= end_month) :
                            books.extend(self.crawl_certain_month_novel(page_dic[date], date))

        print(books)
        return books

    def crawl_selected_month(self, ym_list, page_dic = None) :
        if page_dic is None :
            page_dic = self.crawl_entire_novel_page()
        books = []

        for ym in ym_list :
            if ym in page_dic.keys() :
                books.append((ym, self.crawl_certain_month_novel(page_dic[ym], ym)))
            else :
                print("{} no such year-month".format(ym))

        return books