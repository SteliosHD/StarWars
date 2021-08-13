# search module
from datetime import datetime

import requests
import os
import json
from core.application_constants import URL, EARTH_ORBITAL_PERIOD, EARTH_ROTATION_PERIOD, DEFAULT_FILENAME, data_dir


class SwapiDAO:

    def __init__(self, filename=''):
        self.url = URL
        self.world_url = ''
        self.suffix = ''
        self.fetch_char_query = ''
        self.search_params = ''
        self.type_search = ''  # types : 'simple' or 'complex'
        if filename:
            self.filename = filename
        else:
            self.filename = DEFAULT_FILENAME
        self.data_directory = data_dir

    def search_char(self, search_character_query, world_flag, silent=False):
        char_returned_data, cache_flag = self.fetch_char(search_character_query)
        character_data = char_returned_data["character_info"]
        if character_data:
            properties = character_data  # ["result"][0]["properties"]
            char_name = properties["name"]
            char_height = properties["height"]
            char_mass = properties["mass"]
            char_birth_year = properties["birth_year"]
            self.world_url = properties["homeworld"]  # get homeworld planet url
            if cache_flag:
                cache_info = char_returned_data["character_time_cached"]
            else:
                cache_info = ''
            if world_flag:
                world_returned_data, cache_flag = self.fetch_char_with_world(self.fetch_char_query, self.world_url)
                planet_data = world_returned_data["world_info"]
                planet_properties = planet_data  # ["result"]["properties"]  # does not need [0] cause it returns a dict
                planet_name = planet_properties["name"]
                planet_population = planet_properties["population"]
                planet_orbital_period = int(planet_properties["orbital_period"])
                planet_rotation_period = int(planet_properties["rotation_period"])

                # based on the example "On Tatooine, 1 year on earth is 0.83 years and 1 day 0.96 days"
                # it should have been reversed cause 1 year on earth is 365 rotations and on Tatooine is
                # 304 so 1 year on earth is 365/304 ~ 1.2 years on Tatooine and similar for the day.
                plane_year_dur = planet_orbital_period / EARTH_ORBITAL_PERIOD
                plane_day_dur = planet_rotation_period / EARTH_ROTATION_PERIOD
                if cache_flag:
                    cache_info = world_returned_data["character_time_cached"]
                else:
                    cache_info = ''

                print_params = self.print_results(char_name,
                                                  char_height,
                                                  char_mass,
                                                  char_birth_year,
                                                  planet_name,
                                                  planet_population,
                                                  plane_year_dur,
                                                  plane_day_dur,
                                                  cache_info=cache_info,
                                                  include_world=True,
                                                  silent=silent)
            else:
                print_params = self.print_results(char_name,
                                                  char_height,
                                                  char_mass,
                                                  char_birth_year,
                                                  cache_info=cache_info,
                                                  silent=silent)
        else:
            # if silent dont print and return params else return 0
            if silent:
                print_params = "The force is not strong within you"
            else:
                print("The force is not strong within you")
                print_params = 0
        return print_params

    def fetch_char(self, search_character_query):
        """
        Returns a dictionary (cause of the decorator) of the form:

        returned_dict -> {"character_info": char_info_dict,
                          "world_info": world_info_dict,
                          "character_time_cached": cache_time,
                          "world_time_cached": world_cache_time}

        """
        self.fetch_char_query = search_character_query
        self.suffix = "people/"
        self.search_params = {"name": self.fetch_char_query}
        self.type_search = 'simple'

        data, flag = self.get_data_from_cache_or_fetch()
        return data, flag

    def fetch_char_with_world(self, search_character_query, world_url):
        """
        !!!!
        MUST ALWAYS RUN AFTER THE fetch_char function in order for the cache to run smoothly.
        This was done on purpose to avoid creating multiple files or multiple cache methods. It will
        serve the purpose of this assessment I think.
        !!!!

        Inputs are used for the cache and to avoid the creation multiple types of cache
        Not the cleanest work but it will do.
        ( this is a static method masked as not one) didn't want to test if it breaks the decorator
        Returns a dictionary (cause of the decorator) of the form:

        returned_dict -> {"character_info": char_info_dict,
                          "world_info": world_info_dict,
                          "character_time_cached": cache_time,
                          "world_time_cached": world_cache_time}

        """
        self.fetch_char_query = search_character_query
        self.world_url = world_url
        self.type_search = 'complex'
        data, flag = self.get_data_from_cache_or_fetch()
        return data, flag

    def get_data_from_cache_or_fetch(self):
        """
        Initially was a decorator but didn't behave so well so I modified it in order to meet the deadline
        not the most elegant approach but it works.

        """
        full_path = self.data_directory + self.filename

        try:
            cache_file = open(full_path, 'r')
            cache = json.load(cache_file)
            cache_file.close()
        except (IOError, ValueError):
            cache = {}

        # use the flag to identify if cached was used
        cache_flag = 0

        # should have been more deeper in the function but we don't care so much about accuracy
        cache_time = 'cached: ' + str(datetime.now())

        if self.type_search == 'simple':
            # check if fetch_char_query is in cache and update character info and character cache time or return cached
            # caller function must return character info as the first element
            if self.fetch_char_query not in cache:
                # no check on request seemed a bit overkill
                char_response = requests.get(self.url + self.suffix, params=self.search_params)
                if char_response.ok:
                    char_data = json.loads(char_response.text)["result"]
                    # if search query found a character get the properties or else return empty dict
                    if char_data:
                        char_info = char_data[0]["properties"]  # get the properties dictionary
                    else:
                        char_info = {}
                else:
                    print("Bad response: ", char_response)
                    char_info = {"Bad Response": "Bad response"}

                cache[self.fetch_char_query] = {"character_info": char_info,
                                                "world_info": {},
                                                "character_time_cached": cache_time,
                                                "world_time_cached": {}}
                file_cache = open(full_path, 'w')

                # write file immediately
                json.dump(cache, file_cache)
                file_cache.flush()
                os.fsync(file_cache.fileno())
                file_cache.close()

            else:
                cache_flag = 1
        elif self.type_search == 'complex':
            # if world_query search was given check if it is in world_info_dict and update
            # assuming that fetch_char function has already run and fetch_char_query is in the cache when
            # fetch_char_with_world is run.
            if not cache[self.fetch_char_query]["world_info"]:
                # no check on request seemed a bit overkill but it will fail with bad url
                world_response = requests.get(self.world_url)
                if world_response.ok:
                    world_info = json.loads(world_response.text)["result"][
                        "properties"]  # get the properties dictionary
                else:
                    print("Bad Response: ", world_response)
                    world_info = {"Bad Response": "Bad response"}
                cache[self.fetch_char_query].update({"world_info": world_info,
                                                     "world_time_cached": cache_time})
                file_cache = open(full_path, 'w')
                json.dump(cache, file_cache)

                # write file immediately
                file_cache.flush()
                os.fsync(file_cache.fileno())
                file_cache.close()
            else:
                cache_flag = 1
        else:
            cache[self.fetch_char_query] = {"character_info": {},
                                            "world_info": {},
                                            "character_time_cached": {},
                                            "world_time_cached": {}}

        return cache[self.fetch_char_query], cache_flag

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
                print_params.append('Search: {}\nResults: {}\nSearch Times: {}\n'.format(search, str(result), str(search_time)))
            if silent:
                return print_params
            else:
                print(print_params)

        except (IOError, ValueError):
            print_params = "No stars in this galaxy. Somebody has messed with the cache files"
            if silent:
                return print_params
            else:
                print(print_params)

    ####################################################################################################################
    #                                           Static Methods                                                         #
    ####################################################################################################################

    @staticmethod
    def print_results(*argv, cache_info='', include_world=False, silent=False):
        """
            Print results
            Positional Arguments: char_name, char_height, char_mass, char_birth_year, planet_name, planet_poulation,
                                  planet_year_dur (int/float), planet_day_dur (int/float)
        """
        char_name, char_height, char_mass, char_birth_year = argv[0], argv[1], argv[2], argv[3]
        print_params = ["Name: " + char_name,
                        "Height: " + char_height,
                        "Mass: " + char_mass,
                        "Birth Year: " + char_birth_year]
        if include_world:
            planet_name, planet_population, planet_year_dur, planet_day_dur = argv[4], argv[5], argv[6], argv[7]
            print_params.append("\n\n")
            print_params.append("Homeworld")
            print_params.append("-" * 16)
            print_params.append("Name: " + planet_name)
            print_params.append("Population: " + planet_population)
            print_params.append("On {}, 1 year on earth is {:.2f} years and 1 day {:.2f} days".format(planet_name,
                                                                                                      planet_year_dur,
                                                                                                      planet_day_dur))
        if cache_info:
            print_params.append(cache_info)

        if silent:
            return print_params
        else:
            for param in print_params:
                print(param)
            return 0
