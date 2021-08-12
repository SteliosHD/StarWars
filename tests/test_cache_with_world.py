import unittest
from tests.cache_constants import *
from tests.mock_cache import Mock


class TestCacheWorld(unittest.TestCase):
    """
    Very sloppy tests for cache.
    """

    def setUp(self):
        self.mock_with_world = Mock()

    def test_cache_decorator_world(self):
        # check world info mock fetch
        world_response_1, world_flag_1 = self.mock_with_world.mock_fetch_char_with_world(search_query_1, character_name_1)
        world_response_2, world_flag_2 = self.mock_with_world.mock_fetch_char_with_world(search_query_2, character_name_2)
        world_response_3, world_flag_3 = self.mock_with_world.mock_fetch_char_with_world(search_query_3, {})
        world_response_4, world_flag_4 = self.mock_with_world.mock_fetch_char_with_world(search_query_1, character_name_1)

        world_cache_1 = world_response_1["world_time_cached"]
        world_cache_2 = world_response_2["world_time_cached"]
        world_cache_3 = world_response_3["world_time_cached"]
        world_cache_4 = world_response_4["world_time_cached"]

        self.assertEqual(world_response_1["world_info"], yodas_planet)
        self.assertEqual(world_response_2["world_info"], tatooine)
        self.assertEqual(world_response_3["world_info"], {})
        self.assertEqual(world_response_4["world_info"], yodas_planet)

        # test if cache flags are returned correctly
        self.assertFalse(world_flag_1)
        self.assertFalse(world_flag_2)
        self.assertFalse(world_flag_3)
        self.assertTrue(world_flag_4)

        # test if character info are still ok
        self.assertEqual(world_response_1["character_info"], yoda)
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
    unittest.main()
