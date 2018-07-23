from external_tools import namu_wiki_crawler as nmcw
from external_tools import NaverBookSearcher as nase

class external_tools_instantiater :
    __instance = None

    def __init__(self) :
        self.nase_instance = nase.NaverBookSearcher()
        self.nmcw_instance = nmcw.NamuNovelCrawler()

    @classmethod
    def get_instance(cls) :
        if cls.__instance == None :
            cls.__instance = external_tools_instantiater()

        return cls.__instance

    @classmethod
    def get_searcher_naver_instance(cls) :
        return cls.__instance.nase_instance

    @classmethod
    def get_crawler_namu_instance(cls) :
        return cls.__instance.nmcw_instance