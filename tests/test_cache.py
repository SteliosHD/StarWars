import sys
import os
# a little trick to ensure that it can be run from anywhere not best practice indeed
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from core.application_constants import data_dir
import unittest
from tests.cache_constants import *
from tests.mock_cache import Mock


class TestCache(unittest.TestCase):
    """
    Very sloppy tests for cache.
    test_cache.json must not exist before running the test.
    """

    def setUp(self):
        self.mock_no_world = Mock()

    def test_cache_decorator(self):

        ##########################################################

        # check character info mock fetch
        char_response_1, flag_1 = self.mock_no_world.mock_fetch_char(search_query_1)
        char_response_2, flag_2 = self.mock_no_world.mock_fetch_char(search_query_2)
        char_response_3, flag_3 = self.mock_no_world.mock_fetch_char(search_query_3)
        char_response_4, flag_4 = self.mock_no_world.mock_fetch_char(search_query_1)

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
        self.assertFalse(flag_1)
        self.assertFalse(flag_2)
        self.assertFalse(flag_3)
        self.assertTrue(flag_4)

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


if __name__ == "__main__":
    # if test_cache data file exists before running the test delete the datafile
    data_file = data_dir + "test_cache.json"
    try:
        os.remove(data_file)
        print("removed cache")
    except FileNotFoundError:
        print("This galaxy was clean from the start stormtrooper!")
    unittest.main()
