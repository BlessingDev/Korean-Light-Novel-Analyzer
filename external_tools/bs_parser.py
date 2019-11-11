from bs4 import BeautifulSoup
import urllib.parse

class BSParser :
    """
    BS를 파싱하는데 필요한 가장 기본적인 기능을 정의하는 클래스
    """
    def __init__(self, html_source) :
        self.soup = BeautifulSoup(html_source)

    def get_node(self, tag, attribute, node = None) :
        """

        :param tag: 검색할 태그(str)
        :param attribute: (속성이름, 속성 리스트)
        :param node: 검색을 시작할 노드 기본값은 전체
        :return: 찾은 노드
        """
        if node == None :
            node = self.soup

        for t in node(tag) :
            if attribute[0] in t.attrs \
                and all(a in t[attribute[0]] for a in attribute[1]) :
                # attribute 안에 있는 모든 요소가 t의 속성 중에도 있는지 확인하는
                # all 함수
                return t

        return None

    def get_nodes(self, tag, attribute, node = None) :
        """

        :param tag: 검색할 태그(str)
        :param attribute: (속성이름, 속성 리스트)
        :param node: 검색을 시작할 노드 기본값은 전체
        :return: 찾은 노드의 리스트
        """
        if node == None :
            node = self.soup

        node_list = []
        for t in node(tag) :
            if attribute[0] in t.attrs \
                and all(a in t[attribute[0]] for a in attribute[1]) :
                node_list.append(t)

        if len(node_list) == 0 :
            # get_node 함수와의 작동상 일체성을 위해서
            node_list = None

        return node_list

    def get_text(self, tag, attribute, node = None):
        """

        :param tag: 검색할 태그(str)
        :param attribute: (속성이름, 속성값)
        :param node: 검색을 시작할 노드 기본값은 전체
        :return: 찾은 노드
        """
        if node == None :
            node = self.soup

        for t in node(tag) :
            if attribute[0] in t.attrs \
                and all(a in t[attribute[0]] for a in attribute[1]) :
                return t.get_text()

        return ""