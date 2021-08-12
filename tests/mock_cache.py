from core.cache import persistant_cache
from tests.cache_constants import *


class Mock:

    def __init__(self):
        pass

    @persistant_cache("test_cache.json")
    def mock_fetch_char_with_world(self, search_query, character_name):
        """ for simplicity used character name in real fetch in will the url"""
        if search_query == search_query_1 and character_name == character_name_1:
            return yodas_planet
        elif search_query == search_query_2 and character_name == character_name_2:
            return tatooine
        else:
            return {}

    @persistant_cache("test_cache.json")
    def mock_fetch_char(self, search_query):
        if search_query == search_query_1:
            return yoda
        elif search_query == search_query_2:
            return luke_skywalker
        elif search_query == search_query_3:
            return {}