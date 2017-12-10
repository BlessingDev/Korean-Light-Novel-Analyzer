import random, math, pathlib, json

import visualization, json_file

def distance_book(book1, book2) :
    '''
    거리를 0~1 사이의 실수로 돌려주는 함수

    :param book1:
    :param book2:
    :return:
    '''
    genre_distance = 0  # 장르 거리
    genre_weight = 2    # 장르 가중치
    for genre in book1.genre :
        if genre not in book2.genre :
            genre_distance += 1.0
    for genre in book2.genre :
        if genre not in book1.genre :
            genre_distance += 1.0

    genre_distance += abs(len(book1.genre) - len(book2.genre))

    author_distance = 0 # 작가 거리
    author_weight = 5   # 작가 가중치

    if book1.author != book2.author :
        author_distance += 1

    maxdis = (len(book1.genre) + len(book2.genre)
              + abs(len(book1.genre) - len(book2.genre))) * genre_weight + author_weight

    dis = genre_distance * genre_weight + author_distance * author_weight
    if dis == 0 and book1 is not book2:
        print("dis is 0")
        print(book1.title)
        print(book1.genre)
        print(book2.title)
        print(book2.genre)
        dis = 0.1

    return dis / maxdis

class BookCluster :
    '''
    책 사이의 거리에 관련된 데이터를 관리하는 클래스
    '''
    def __init__(self):
        self.data_size = 0
        self.coords = None
        self.real_dist = None

    def set_real_dist(self, book_set) :
        self.data_size = len(book_set)

        self.real_dist = [[distance_book(book_set[i], book_set[j]) for j in range(self.data_size)]
                         for i in range(0, self.data_size)]

    def get_close_books(self, book_idx, n = 10):
        '''
        거리가 가까운 책들을 n개 찾는 함수
        :param book_idx: 찾을 책의 인덱스
        :param n: 찾을 책의 개수 <기본 10>
        :return:
        if 거리 계산됨 [(book index, distance)] 배열
        else None
        '''
        if self.real_dist is not None :
            dist_list = self.real_dist[book_idx]
            dist_list_idx = [(i, dist) for i, dist in enumerate(dist_list)]

            return sorted(dist_list_idx, key = lambda x : x[1])[1:n + 1]
        else :
            print("거리가 계산되지 않음")
            return None

    def scaledown(self, trainn = 1000, rate=0.01):
        n = self.data_size
        realdist = self.real_dist

        outersum = 0.0

        # 2D 내에서 무작위로 선정된 위치에 시작점을 초기화
        loc = [[random.random(), random.random()] for _ in range(n)]
        fakedist = [[0.0 for j in range(n)] for i in range(n)]

        lasterror = None
        for m in range(0, trainn):
            # 투영된 거리를 구함
            for i in range(n):
                for j in range(n):
                    fakedist[i][j] = math.sqrt(sum([pow(loc[i][x] - loc[j][x], 2)
                                                    for x in range(len(loc[i]))]))

            # 점을 이동시킴
            grad = [[0.0, 0.0] for i in range(n)]

            totalerror = 0
            for k in range(n):
                for j in range(n):
                    if j == k: continue
                    # 오류는 거리 간의 차이 비율
                    errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]

                    # 각 점을 오류 정도에 비례해서 다른 점 근처나 멀리 이동시킴
                    grad[k][0] += ((loc[k][0] - loc[j][0]) / fakedist[j][k]) * errorterm
                    grad[k][1] += ((loc[k][1] - loc[j][1]) / fakedist[j][k]) * errorterm

                    totalerror += abs(errorterm)
            print("totalerror = " + totalerror.__str__())

            if lasterror and lasterror < totalerror: break
            lasterror = totalerror

            for k in range(n):
                loc[k][0] -= rate * grad[k][0]
                loc[k][1] -= rate * grad[k][1]

        self.coords = loc
        return loc

    def export_data(self) :
        coordpath = pathlib.Path('coordinates.json')
        coordpath.write_text(json_file.list_to_json(self.coords, json_file.data_to_json), encoding='utf-8')
        distpath = pathlib.Path('dist.json')
        distpath.write_text(json_file.list_to_json(self.real_dist, json_file.data_to_json), encoding='utf-8')

    def import_data(self) :
        coordpath = pathlib.Path('coordinates.json')
        if coordpath.exists() :
            self.coords = json.loads(coordpath.read_text('utf-8'), encoding='utf-8', strict=False)
        distpath = pathlib.Path('dist.json')
        if distpath.exists() :
            self.real_dist = json.loads(distpath.read_text('utf-8'), encoding='utf=8', strict=False)


    def visualize(self, storer) :
        title_list = [book.title for book in storer.get_ordinary_book()]

        visualization.draw2d(self.coords, title_list, imagerate=10000, jpeg = 'book_relavant.jpg')