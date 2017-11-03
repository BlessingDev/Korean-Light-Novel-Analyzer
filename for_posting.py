import requests
from bs4 import BeautifulSoup
from urllib import parse, request

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

    for td in soup('td') : # td 안의
        for a in td('a') : # a 태그 중에서
            if ('class' in a.attrs # a가 class 속성을 가지고 있고
                and 'wiki-link-internal' in a['class'] # class가 'wiki-link-internal'이다
                and a.get_text()[-1] == '월') : # 그리고 안에 들어있는 내용이 '월'로 끝날 때

                print("page {0} added".format(a['href']))
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

        need_japan_check = False
        for h2 in soup.find_all("h2"):
            if h2.get_text() == "1. 대한민국[편집]" :
                need_japan_check = True
                break

        for div in soup('div') : # 페이지에 있는 div 태그 중에서

            if ('class' in div.attrs and
                'wiki-inner-content' in div['class']) : # class가 'wiki-inner-content'인 아이(본문)

                for td in soup('td'):
                    for st in td('strong'):
                        date = st.get_text().strip()

                        if not (date in ignore_word):
                            date = date.split('/')[1]

                            print(date)
                            print()

                for li in div('li') :

                    if need_japan_check :
                        japan_check = False

                        for parent in li.parents:
                            if parent.name == "ul":
                                for sibling in parent.previous_siblings:
                                    if sibling.name == 'h2':
                                        if sibling.get_text() != '1. 대한민국[편집]':
                                            print('일본 체크 {0}'.format(sibling.get_text()))
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

                        print(book_title) # 여기에 수행할 동작 넣기


def search_book_by_title(title) :
    client_id = "EiPxhHox870abSfDvZBR"
    client_pw = "RqJncUd4p1"

    enc_text = parse.quote(title) # 변수 title을 인코딩

    url = "https://openapi.naver.com/v1/search/book.json?query=" + enc_text + "&display=10&start=1"
        # API URL에 query와 패러미터를 추가한 url
    req = request.Request(url) # urllib.request.Request로 http 요청 객체 생성
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_pw) # header로 id와 secret 추가

    try:
        response = request.urlopen(req) # 객체를 매개변수로 request.urlopen을 호출해 Web 서버에 요청
    except:
        print("책 제목 {} 검색 불가".format(title))
        return None

    res_code = response.getcode() # response의 코드

    if (res_code == 200): # 200 OK 이면
        response_body = response.read()

        print("body " + response_body.decode('utf-8')) # 내용을 출력



if __name__ == "__main__" :
    search_book_by_title("기생여친 사나 1") # 책 제목을 전달