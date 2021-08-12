import sys
import os

# a little trick to ensure that it can be run from anywhere not best practice indeed
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from core.application_constants import data_dir
import unittest
from core.search import *
from tests.search_constants import *
from time import sleep


class TestSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # if test_cache data file exists before running the test delete the datafile
        data_file = data_dir + "test_search.json"
        try:
            os.remove(data_file)
            print("removed cache")
        except FileNotFoundError:
            print("This galaxy was clean from the start stormtrooper!")

    @classmethod
    def tearDownClass(cls):
        # if test_cache data file exists before running the test delete the datafile
        data_file = data_dir + "test_search.json"
        try:
            os.remove(data_file)
            print("removed cache")
        except FileNotFoundError:
            print("This galaxy was clean from the start stormtrooper!")

    def setUp(self):
        self.search_obj_no_flag_query_exists = Search()
        self.search_obj_yes_flag_query_exists = Search()
        self.search_obj_query_no_flag_not_exists = Search()
        self.search_obj_query_yes_flag_not_exists = Search()

    def test_search_char(self):
        pass

    def test_fetch_char(self):
        return_params_1, cache_flag_1 = self.search_obj_no_flag_query_exists.fetch_char(search_query_1)
        sleep(2)  # try not to overload the server
        return_params_2, cache_flag_2 = self.search_obj_no_flag_query_exists.fetch_char(search_query_2)
        sleep(2)  # try not to overload the server
        return_params_3, cache_flag_3 = self.search_obj_no_flag_query_exists.fetch_char(search_query_3)

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
        pass

    def test_delete_cache(self):
        self.assertFalse(self.search_obj_no_flag_query_exists.delete_cache())

    def test_print_results(self):
        return_params_1 = self.search_obj_no_flag_query_exists.print_results(print_name,
                                                                             print_height,
                                                                             print_mass,
                                                                             print_birth,
                                                                             silent=True
                                                                             )

        return_params_2 = self.search_obj_yes_flag_query_exists.print_results(print_name,
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
        return_params_3 = self.search_obj_no_flag_query_exists.print_results(print_name,
                                                                             print_height,
                                                                             print_mass,
                                                                             print_birth,
                                                                             silent=False
                                                                             )
        return_params_4 = self.search_obj_yes_flag_query_exists.print_results(print_name,
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
