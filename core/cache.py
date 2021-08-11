# cache module
import json
from datetime import datetime
from core.application_constants import data_dir


def persistant_cache(file_name):
    """
    Add persistant cache functionality.
    All data is stored in the data/ folder
    Inputs: file name e.g. 'test.json' (excepts json files)
    """
    full_path = data_dir / file_name

    def decorator(caller_function):

        try:
            cache = json.load(open(full_path, 'r'))
        except (IOError, ValueError):
            cache = {}

        def cache_function(*args):
            cache_flag = 0
            character_query = args[0]
            if len(args) == 2:
                world_query = args[1]
            else:
                world_query = []
            cache_time = 'cached: ' + str(datetime.now())

            # check if character_query is in cache and update character info and character cache time or return cached
            # caller function must return character info as the first element
            if character_query not in cache:
                cache[character_query] = {"character_info": caller_function(character_query)[0],
                                          "world_info": {},
                                          "character_time_cached": cache_time,
                                          "world_time_cached": {}}
                json.dump(cache, open(full_path, 'w'))
            else:
                cache_flag = 1
            # if world_query was given check if it is in character_query_dict and update world info and world cache time
            # caller function must return world info as the second element
            if world_query:
                if not cache[character_query]["world_info"]:
                    cache[character_query].update({"world_info": caller_function(character_query, world_query)[1],
                                                   "world_time_cached": cache_time})
                    json.dump(cache, open(full_path, 'w'))

            return cache[character_query], cache_flag

        return cache_function

    return decorator
