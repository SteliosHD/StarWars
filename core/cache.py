import os
import json
from datetime import datetime
from core.application_constants import DEFAULT_FILENAME, data_dir


class PersistentCache:

    def __init__(self, filename=''):
        if filename:
            self.filename = filename
        else:
            self.filename = DEFAULT_FILENAME
        self.data_directory = data_dir

    def check_cache(self, search_query, world_flag=False):
        """
        Check if the info we want is in the cache and return True or False
        """
        cache, full_path = self._check_get_cache_file()
        # what type of info to check
        if world_flag:
            try:
                if cache[search_query]["world_info"]:
                    return True
                else:
                    return False
            except KeyError:
                print("The item you want was never in the galaxy to begin with!")
        else:
            if search_query in cache:
                return True
            else:
                return False

    def write_char_data_to_cache(self, search_query, char_info):
        """
        Write character data to cache
        """
        try:
            cache, full_path = self._check_get_cache_file()
            cache_time = 'cached: ' + str(datetime.now())
            cache[search_query] = {"character_info": char_info,
                                   "world_info": {},
                                   "character_time_cached": cache_time,
                                   "world_time_cached": {}}
            file_cache = open(full_path, 'w')
            # write file immediately
            json.dump(cache, file_cache)
            file_cache.flush()
            os.fsync(file_cache.fileno())
            file_cache.close()
            return 1
        except Exception as e:
            print(e)
            return 0

    def write_world_data_to_cache(self, search_query, world_info):
        """
        Write world data to cache
        """
        try:
            cache, full_path = self._check_get_cache_file()
            cache_time = 'cached: ' + str(datetime.now())
            cache[search_query].update({"world_info": world_info,
                                        "world_time_cached": cache_time})
            file_cache = open(full_path, 'w')
            # write file immediately
            json.dump(cache, file_cache)
            file_cache.flush()
            os.fsync(file_cache.fileno())
            file_cache.close()
            return 1
        except Exception as e:
            print(e)
            return 0

    def get_cached_data(self, search_query):
        """
        Get data from the cache
        """
        cache, full_path = self._check_get_cache_file()
        try:
            data = cache[search_query]
            return data
        except KeyError:
            print("The item is not in this galaxy My Lord!")
            return {}

    def delete_cache(self):
        """
        Static Method
        Clear cache by deleting the query_data.json file
        """
        try:
            os.remove(self.data_directory + self.filename)
            print("removed cache")
            return True
        except FileNotFoundError:
            print("This galaxy was clean from the start stormtrooper!")
            return False

    def get_history(self, silent=False):
        """
        Return the history of searches
        If silent it will print else it will return the print parameters in the form of a string
        if we want to process the data just change the append method.
        """
        full_path = self.data_directory + self.filename
        history = {}
        print_params = []
        try:
            cache_file = open(full_path, 'r')
            cache = json.load(cache_file)
            cache_file.close()
            for index, key in enumerate(cache.keys()):
                history.update({"search" + str(index): {"search": key,
                                                        "result": [cache[key]["character_info"],
                                                                   cache[key]["world_info"]],
                                                        "search_time": [cache[key]["character_time_cached"],
                                                                        cache[key]["world_time_cached"]]
                                                        }})
            for key in history.keys():
                val = history[key]
                search = val['search']
                result = val['result']
                search_time = val["search_time"]
                print_params.append(
                    'Search: {}\nResults: {}\nSearch Times: {}\n'.format(search, str(result), str(search_time)))
            if silent:
                return print_params
            else:
                print(print_params[0])

        except (IOError, ValueError):
            print_params = "No stars in this galaxy. Somebody has messed with the cache files"
            if silent:
                return print_params
            else:
                print(print_params)

    def _check_get_cache_file(self):
        """
        Helper method to read the cache
        It's loaded many times
        Probably could be improved if it's store inside the class somewhere
        """
        full_path = self.data_directory + self.filename

        try:
            cache_file = open(full_path, 'r')
            cache = json.load(cache_file)
            cache_file.close()
        except (IOError, ValueError):
            cache = {}

        return cache, full_path
