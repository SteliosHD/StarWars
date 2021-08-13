import unittest

import sys
import os

# a little trick to ensure that it can be run from anywhere not best practice indeed
root_dir = os.path.dirname(os.getcwd())
# os.chdir(root_dir)
sys.path.append(root_dir)

from core.swapiDAO import *
from core.cache import *
from tests.test_swapiDAO_constants import *
from time import sleep

test_filename = "test_search.json"


class TestSwapiDAO(unittest.TestCase):
    """Some testing is better than no testing"""

    @classmethod
    def setUpClass(cls):
        # if test_cache data file exists before running the test delete the datafile
        data_file = data_dir + test_filename
        try:
            os.remove(data_file)
            print("removed cache")
        except FileNotFoundError:
            print("This galaxy was clean from the start stormtrooper!")

    @classmethod
    def tearDownClass(cls):
        # if test_cache data file exists before running the test delete the datafile
        data_file = data_dir + test_filename
        try:
            os.remove(data_file)
            print("removed cache")
        except FileNotFoundError:
            print("This galaxy was clean from the start stormtrooper!")

    def setUp(self):
        self.swapi_test_obj = SwapiDAO(test_filename)
        self.cache_test_obj = PersistentCache(test_filename)

    def test_search_char(self):
        # with no flag silent
        returned_params_no_flag_1 = self.swapi_test_obj.search_char(search_query_1, False, silent=True)
        sleep(2)
        returned_params_no_flag_2 = self.swapi_test_obj.search_char(search_query_2, False, silent=True)
        returned_params_no_flag_2.pop()
        sleep(2)
        returned_params_no_flag_3 = self.swapi_test_obj.search_char(search_query_3, False, silent=True)
        sleep(2)

        # with flag silent
        returned_params_with_flag_1 = self.swapi_test_obj.search_char(search_query_1, True, silent=True)
        sleep(2)
        returned_params_with_flag_2 = self.swapi_test_obj.search_char(search_query_2, True, silent=True)
        returned_params_with_flag_2.pop()
        sleep(2)
        returned_params_with_flag_3 = self.swapi_test_obj.search_char(search_query_3, True, silent=True)
        sleep(2)

        # with flag not silent
        returned_params_with_flag_loud = self.swapi_test_obj.search_char(search_query_1, True, silent=False)
        sleep(2)

        # with no flag no silent
        returned_params_no_flag_loud = self.swapi_test_obj.search_char(search_query_1, False, silent=False)
        sleep(2)

        # return one cached
        returned_params_no_flag_4 = self.swapi_test_obj.search_char(search_query_2, False, silent=True)
        cache_info_returned = returned_params_no_flag_4.pop()  # pop cache_info

        self.assertEqual(returned_params_no_flag_2, print_example_no_flag)
        self.assertEqual(returned_params_with_flag_2, print_example_with_flag)
        self.assertEqual(returned_params_no_flag_3, "The force is not strong within you")
        self.assertEqual(returned_params_with_flag_3, "The force is not strong within you")
        self.assertEqual(returned_params_no_flag_4, print_example_no_flag)
        self.assertFalse(returned_params_no_flag_loud)
        self.assertFalse(returned_params_with_flag_loud)
        self.assertTrue(cache_info_returned)
        self.assertTrue(returned_params_no_flag_1)
        self.assertTrue(returned_params_with_flag_1)

    def test_fetch_char(self):
        return_params_1, cache_flag_1 = self.swapi_test_obj.fetch_char(search_query_1)
        sleep(2)  # try not to overload the server
        return_params_2, cache_flag_2 = self.swapi_test_obj.fetch_char(search_query_2)
        sleep(2)  # try not to overload the server
        return_params_3, cache_flag_3 = self.swapi_test_obj.fetch_char(search_query_3)

        # delete some non constant entries
        del return_params_1["character_info"]["created"]
        del return_params_1["character_info"]["edited"]
        del return_params_2["character_info"]["created"]
        del return_params_2["character_info"]["edited"]

        self.assertEqual(return_params_1["character_info"], yoda)
        self.assertTrue(return_params_1["character_time_cached"])

        self.assertEqual(return_params_2["character_info"], luke_skywalker)
        self.assertTrue(return_params_2["character_time_cached"])

        self.assertFalse(return_params_3["character_info"])
        self.assertTrue(return_params_3["character_time_cached"])

        self.assertFalse(cache_flag_1)
        self.assertFalse(cache_flag_2)
        self.assertFalse(cache_flag_3)

    def test_fetch_char_with_world(self):
        # fetch the world data
        return_params_1, cache_flag_1 = self.swapi_test_obj.fetch_char(search_query_1)
        sleep(2)  # try not to overload the server
        return_world_params_1, world_cache_flag_1 = self.swapi_test_obj.fetch_char_with_world(search_query_1, yoda_url)
        sleep(2)  # try not to overload the server
        return_params_2, cache_flag_2 = self.swapi_test_obj.fetch_char(search_query_2)
        sleep(2)  # try not to overload the server
        return_world_params_2, world_cache_flag_2 = self.swapi_test_obj.fetch_char_with_world(search_query_2, luke_url)
        sleep(2)  # try not to overload the server

        self.assertRaises(requests.exceptions.ConnectionError, self.swapi_test_obj.fetch_char_with_world,
                          search_query_3, bad_url)

        # delete some non constant entries
        del return_params_1["character_info"]["created"]
        del return_params_1["character_info"]["edited"]
        del return_params_2["character_info"]["created"]
        del return_params_2["character_info"]["edited"]

        # delete some non constant entries
        del return_world_params_1["character_info"]["created"]
        del return_world_params_1["character_info"]["edited"]
        del return_world_params_2["character_info"]["created"]
        del return_world_params_2["character_info"]["edited"]

        del return_world_params_1["world_info"]["created"]
        del return_world_params_1["world_info"]["edited"]
        del return_world_params_2["world_info"]["created"]
        del return_world_params_2["world_info"]["edited"]

        # check if data is ok
        self.assertEqual(return_world_params_1["character_info"], yoda)
        self.assertTrue(return_world_params_1["character_time_cached"])

        self.assertEqual(return_world_params_2["character_info"], luke_skywalker)
        self.assertTrue(return_world_params_2["character_time_cached"])

        self.assertFalse(world_cache_flag_1)
        self.assertFalse(world_cache_flag_2)

        # check if world data is ok
        self.assertEqual(return_world_params_1["world_info"], yodas_planet)
        self.assertTrue(return_world_params_1["world_time_cached"])

        self.assertEqual(return_world_params_2["world_info"], tatooine)
        self.assertTrue(return_world_params_2["world_time_cached"])

        self.assertNotEqual(return_params_1["character_time_cached"], return_world_params_1["world_time_cached"])
        self.assertNotEqual(return_params_2["character_time_cached"], return_world_params_2["world_time_cached"])

    def test_delete_cache(self):
        self.assertFalse(self.cache_test_obj.delete_cache())

    def test_print_results(self):
        return_params_1 = self.swapi_test_obj.print_results(print_name,
                                                            print_height,
                                                            print_mass,
                                                            print_birth,
                                                            silent=True
                                                            )

        return_params_2 = self.swapi_test_obj.print_results(print_name,
                                                            print_height,
                                                            print_mass,
                                                            print_birth,
                                                            print_planet,
                                                            print_population,
                                                            print_year_dur,
                                                            print_day_dur,
                                                            include_world=True,
                                                            silent=True
                                                            )
        return_params_3 = self.swapi_test_obj.print_results(print_name,
                                                            print_height,
                                                            print_mass,
                                                            print_birth,
                                                            silent=False
                                                            )
        return_params_4 = self.swapi_test_obj.print_results(print_name,
                                                            print_height,
                                                            print_mass,
                                                            print_birth,
                                                            print_planet,
                                                            print_population,
                                                            print_year_dur,
                                                            print_day_dur,
                                                            include_world=True,
                                                            silent=False
                                                            )
        self.assertEqual(return_params_1, print_example_no_flag)
        self.assertEqual(return_params_2, print_example_with_flag)
        self.assertFalse(return_params_3)
        self.assertFalse(return_params_4)


if __name__ == "__main__":
    unittest.main()
