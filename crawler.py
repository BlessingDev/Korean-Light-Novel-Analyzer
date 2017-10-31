import requests
from bs4 import BeautifulSoup

import book_data

def get_html(url) :
    html = ""
    resp = ""
    try:
        resp = requests.get(url)
    except:
        print("URL {}에 접속 불가".format(url))
        return None

    if resp.status_code == 200 :
        html = resp.text

    return html


def crawl_whole_korean_novel() :
    pages = []
    books = book_data.book_storer()

    c = get_html('https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%ED%8A%B8%20%EB%85%B8%EB%B2%A8/%EC%8B%A0%EA%B0%84%20%EB%AA%A9%EB%A1%9D')


    soup = BeautifulSoup(c)

    for td in soup('td') :
        for a in td('a') :
            print(a.get_text())

            if ('class' in a.attrs
                and 'wiki-link-internal' in a['class']
                and a.get_text()[-1] == '월') :
                print("page added")
                pages.append('https://namu.wiki' + a['href'])

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

    for page in pages :
        c = get_html(page)

        soup = BeautifulSoup(c)

        date = ""

        need_japan_check = False
        for h2 in soup.find_all("h2"):
            if h2.get_text() == "1. 대한민국[편집]":
                need_japan_check = True
                break

        for td in soup('td') :
            for st in td('strong') :
                date = st.get_text().strip()

                if not (date in ignore_word):
                    date = date.split('/')[1]

                    #print(date)
                    #print()

        for div in soup('div') :

            if ('class' in div.attrs and
                'wiki-inner-content' in div['class']) :

                for li in div('li') :

                    if need_japan_check :
                        japan_check = False

                        for parent in li.parents:
                            if parent.name == "ul":
                                for sibling in parent.previous_siblings:
                                    if sibling.name == 'h2':
                                        if sibling.get_text() != '1. 대한민국[편집]':
                                            #print('일본 체크 {0}'.format(sibling.get_text()))
                                            japan_check = True
                                            break

                        if japan_check:
                            break

                    book_title = li.get_text().strip()

                    if book_title != "" and (not (book_title in ignore_word)) :
                        if '[' in book_title :
                            list_a = book_title.split('[')

                            book_title = list_a[0]

                        if '(' in book_title :
                            list_a = book_title.split('(')

                            book_title = list_a[0]

                        if book_title[-1] == '권' :
                            book_title = book_title.split('권')[0]

                        books.add_by_date_title(date, book_title)


        print("{0} 크롤링 종료".format(date))



        print()

    return books