# cache module
import json
from datetime import datetime
from core.application_constants import data_dir
import os

def persistant_cache(file_name):
    """
    Add persistant cache functionality.
    All data is stored in the data/ folder
    Inputs: file name e.g. 'test.json' (excepts json files)
    """
    full_path = data_dir + file_name

    def decorator(caller_function):

        try:
            cache_file = open(full_path, 'r')
            cache = json.load(cache_file)
            cache_file.close()
        except (IOError, ValueError):
            cache = {}

        def wrapper_function(*argv):
            """
            Query parameters: search_query and character_name (in case of world)
            Function code -> 1 for search query without world
                             2 for search query with world

            """

            # use the flag to identify if cached was used
            cache_flag = 0
            caller_obj = argv[0]
            search_query = argv[1]

            # should have been more deeper in the function but we don't care so much about accuracy
            cache_time = 'cached: ' + str(datetime.now())

            if len(argv) == 2:
                # check if search_query is in cache and update character info and character cache time or return cached
                # caller function must return character info as the first element
                if search_query not in cache:
                    char_info = caller_function(caller_obj, search_query)  # caller function is fetch_character always
                    cache[search_query] = {"character_info": char_info,
                                           "world_info": {},
                                           "character_time_cached": cache_time,
                                           "world_time_cached": {}}
                    file_cache = open(full_path, 'w')
                    json.dump(cache, file_cache)
                    file_cache.flush()
                    os.fsync(file_cache.fileno())
                    file_cache.close()

                else:
                    cache_flag = 1
            elif len(argv) == 3:
                world_url = argv[2]
                world_info= caller_function(caller_obj, search_query, world_url)  # caller function is fetch_character always
                # if world_query was given check if it is in world_url_dict and update
                # world info and world cache time caller function must return world info
                # as the second element

                # assuming that fetch_char function has already run and search_query is in the cache when
                # fetch_char_with_world is run.
                if not cache[search_query]["world_info"]:
                    cache[search_query].update({"world_info": world_info,   "world_time_cached": cache_time})
                    file_cache = open(full_path, 'w')
                    json.dump(cache, file_cache)
                    file_cache.flush()
                    os.fsync(file_cache.fileno())
                    file_cache.close()
                else:
                    cache_flag = 1

            return cache[search_query], cache_flag

        return wrapper_function

    return decorator
