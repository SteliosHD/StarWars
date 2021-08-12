import sys
import os
# a little trick to ensure that it can be run from anywhere not best practice indeed
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from core.application_constants import data_dir
import unittest
from core.cache import persistant_cache
from tests.cache_constants import *


class TestCache(unittest.TestCase):
    """
    Very sloppy tests for cache.
    file test_cache.json must not exist before running test it is handled if module called directly.
    """

    def test_cache_decorator(self):

        @persistant_cache("test_cache.json")
        def mock_fetch_char(search_query):
            if search_query == search_query_1:
                return yoda
            elif search_query == search_query_2:
                return luke_skywalker
            elif search_query == search_query_3:
                return {}

        ##########################################################

        # check character info mock fetch
        char_response_1, flag_1 = mock_fetch_char(search_query_1)
        char_response_2, flag_2 = mock_fetch_char(search_query_2)
        char_response_3, flag_3 = mock_fetch_char(search_query_3)
        char_response_4, flag_4 = mock_fetch_char(search_query_1)

        char_cache_1 = char_response_1["character_time_cached"]
        char_cache_2 = char_response_2["character_time_cached"]
        char_cache_3 = char_response_3["character_time_cached"]
        char_cache_4 = char_response_4["character_time_cached"]

        # test if character info returned correctly
        self.assertEqual(char_response_1["character_info"],yoda)
        self.assertEqual(char_response_2["character_info"], luke_skywalker)
        self.assertEqual(char_response_3["character_info"], {})
        self.assertEqual(char_response_4["character_info"], yoda)

        # test if cache flags are returned correctly
        self.assertEqual(flag_1, 0)
        self.assertEqual(flag_2, 0)
        self.assertEqual(flag_3, 0)
        self.assertEqual(flag_4, 1)

        # test if world info returned correctly
        self.assertEqual(char_response_1["world_info"], {})
        self.assertEqual(char_response_2["world_info"], {})
        self.assertEqual(char_response_3["world_info"], {})
        self.assertEqual(char_response_4["world_info"], {})

        # test if cached times are recorded correctly
        self.assertTrue(char_cache_1)
        self.assertTrue(char_cache_3)
        self.assertTrue(char_cache_2)
        self.assertTrue(char_cache_4)
        self.assertEqual(char_cache_1, char_cache_4)

    def test_cache_decorator_world(self):

        @persistant_cache("test_cache.json")
        def mock_fetch_char_with_world(search_query, character_name):
            """ for simplicity used character name in real fetch in will the url"""
            if search_query == search_query_1 and character_name == character_name_1:
                return yodas_planet
            elif search_query == search_query_2 and character_name == character_name_2:
                return tatooine
            else:
                return {}
        #################################################################

        # check world info mock fetch
        world_response_1,world_flag_1  = mock_fetch_char_with_world(search_query_1, character_name_1)
        world_response_2,world_flag_2  = mock_fetch_char_with_world(search_query_2, character_name_2)
        world_response_3,world_flag_3  = mock_fetch_char_with_world(search_query_3, {})
        world_response_4,world_flag_4  = mock_fetch_char_with_world(search_query_1, character_name_1)

        world_cache_1 = world_response_1["world_time_cached"]
        world_cache_2 = world_response_2["world_time_cached"]
        world_cache_3 = world_response_3["world_time_cached"]
        world_cache_4 = world_response_4["world_time_cached"]

        self.assertEqual(world_response_1["world_info"], yodas_planet)
        self.assertEqual(world_response_2["world_info"], tatooine)
        self.assertEqual(world_response_3["world_info"], {})
        self.assertEqual(world_response_4["world_info"], yodas_planet)

        # test if cache flags are returned correctly
        self.assertEqual(world_flag_1, 0)
        self.assertEqual(world_flag_2, 0)
        self.assertEqual(world_flag_3, 0)
        self.assertEqual(world_flag_4, 1)

        # test if character info are still ok
        self.assertEqual(world_response_1["character_info"],yoda)
        self.assertEqual(world_response_2["character_info"], luke_skywalker)
        self.assertEqual(world_response_3["character_info"], {})
        self.assertEqual(world_response_4["character_info"], yoda)

        # test if cached times are recorded correctly
        self.assertTrue(world_cache_1)
        self.assertTrue(world_cache_3)
        self.assertTrue(world_cache_2)
        self.assertTrue(world_cache_4)
        self.assertEqual(world_cache_1, world_cache_4)


if __name__ == "__main__":
    # if test_cache data file exists before running the test delete the datafile
    data_file = data_dir + "test_cache.json"
    try:
        os.remove(data_file)
        print("removed cache")
    except FileNotFoundError:
        print("This galaxy was clean from the start stormtrooper!")
    unittest.main()
