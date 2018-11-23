from external_tools import namu_wiki_crawler as nmcw
from external_tools import naver_book_searcher as nase


class external_tools_instantiater :
    __instance = None

    def __init__(self) :
        self.nase_instance = nase.NaverBookSearcher()
        self.nmcw_instance = nmcw.NamuNovelCrawler()
        self.gc_instances = {}

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

    @classmethod
    def get_genre_classifier_instance(cls, key) :
        if (key in cls.__instance.gc_instances.keys()) :
            return cls.__instance.gc_instances
        else :
            return None

    @classmethod
    def set_genre_classifier_instance(cls, key, g) :
        cls.__instance.gc_instances[key] = g