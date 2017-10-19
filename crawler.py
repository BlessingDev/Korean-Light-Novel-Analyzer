import requests
from bs4 import BeautifulSoup

def get_html(url) :
    html = ""
    resp = requests.get(url)

    if resp.status_code == 200 :
        html = resp.text

    return html


def crawl_korean_novel_page() :
    pages = []

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

    print(pages)

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

        for td in soup('td') :
            for st in td('strong') :
                date = st.get_text().strip()

                if not (date in ignore_word):
                    date = date.split('/')[1]

                    print(date)
                    print()

        for div in soup('div') :

            if ('class' in div.attrs and
                'wiki-inner-content' in div['class']) :

                for li in div('li') :
                    book_title = li.get_text().strip()

                    if not (book_title in ignore_word) :
                        if '[' in book_title :
                            list_a = book_title.split('[')

                            book_title = list_a[0]

                        print(book_title)


        print()