# search module
from datetime import datetime

import requests
import os
import json
from core.application_constants import URL, EARTH_ORBITAL_PERIOD, EARTH_ROTATION_PERIOD, DEFAULT_FILENAME, data_dir

from core.cache import PersistentCache


class SwapiDAO:

    def __init__(self, filename=''):
        self.url = URL
        self.world_url = ''
        self.suffix = ''
        self.fetch_char_query = ''
        self.search_params = ''
        if filename:
            self.filename = filename
        else:
            self.filename = DEFAULT_FILENAME
        self.data_directory = data_dir
        self.cache_obj = PersistentCache(self.filename)

    def search_char(self, search_character_query, world_flag, silent=False):
        """
        Search the character and the world info based on the search query
        The search is handled by swapi automatically.
        search_char returns print params if silent else it prints the results of the query.
        search_char uses the fetch_char and fetch_char_with_world functions
        IMPORTANT fetch_char_with_world  must always be called after fetch char in order to create
        an entry in the cache with the search_query!
        """
        char_returned_data, cache_flag = self.fetch_char(search_character_query)
        character_data = char_returned_data["character_info"]
        if character_data:
            properties = character_data
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
                planet_properties = planet_data
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
        Returns a dictionary and a flag of the form:

        returned_dict -> {"character_info": char_info_dict,
                          "world_info": world_info_dict,
                          "character_time_cached": cache_time,
                          "world_time_cached": world_cache_time}
        cache_flag -> if cached items returned :1
                      else : 0

        """
        self.fetch_char_query = search_character_query
        self.suffix = "people/"
        self.search_params = {"name": self.fetch_char_query}
        if not self.cache_obj.check_cache(self.fetch_char_query):
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
            self.cache_obj.write_char_data_to_cache(self.fetch_char_query, char_info)
            data = self.cache_obj.get_cached_data(self.fetch_char_query)
            cache_flag = 0
        else:
            data = self.cache_obj.get_cached_data(self.fetch_char_query)
            cache_flag = 1

        return data, cache_flag

    def fetch_char_with_world(self, search_character_query, world_url):
        """
        !!!!
        MUST ALWAYS RUN AFTER THE fetch_char function in order for the cache to run smoothly.
        This was done on purpose to avoid creating multiple files. It will
        serve the purpose of this assessment I think.
        !!!!
        Returns a dictionary and a flag of the form:

        returned_dict -> {"character_info": char_info_dict,
                          "world_info": world_info_dict,
                          "character_time_cached": cache_time,
                          "world_time_cached": world_cache_time}
        cache_flag -> if cached items returned :1
                      else : 0

        """
        self.fetch_char_query = search_character_query
        self.world_url = world_url

        if not self.cache_obj.check_cache(self.fetch_char_query, world_flag=True):
            # no check on request seemed a bit overkill but it will fail with bad url
            world_response = requests.get(self.world_url)
            if world_response.ok:
                world_info = json.loads(world_response.text)["result"][
                    "properties"]  # get the properties dictionary
            else:
                print("Bad Response: ", world_response)
                world_info = {"Bad Response": "Bad response"}
            self.cache_obj.write_world_data_to_cache(self.fetch_char_query, world_info)
            data = self.cache_obj.get_cached_data(self.fetch_char_query)  # get to avoid double writes maybe singleton would be useful here
            cache_flag = 0
        else:
            data = self.cache_obj.get_cached_data(self.fetch_char_query)
            cache_flag = 1

        return data, cache_flag

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
