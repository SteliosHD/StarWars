# search module
import requests
import os
import json
from core.application_constants import URL, EARTH_ORBITAL_PERIOD, EARTH_ROTATION_PERIOD, DEFAULT_FILENAME, data_dir
from core.cache import persistant_cache


class Search:

    def __init__(self):
        self.url = URL

    def search_char(self, search_character_query, world_flag, silent=False):
        char_returned_data, cache_flag = self.fetch_char(search_character_query)
        character_data = char_returned_data["character_info"]
        if character_data:
            properties = character_data["result"][0]["properties"]
            char_name = properties["name"]
            char_height = properties["height"]
            char_mass = properties["mass"]
            char_birth_year = properties["birth_year"]
            homeworld_url = properties["homeworld"]  # get homeworld planet url
            if cache_flag:
                cache_info = char_returned_data["character_time_cached"]
            else:
                cache_info = ''
            if world_flag:
                world_returned_data, cache_flag = self.fetch_char_with_world(search_character_query, homeworld_url)
                planet_data = world_returned_data["world_info"]
                planet_properties = planet_data["result"]["properties"]  # does not need [0] cause it returns a dict
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

    @persistant_cache("test_search.json")
    def fetch_char(self, search_character_query):
        """
        Returns a dictionary (cause of the decorator) of the form:

        returned_dict -> {"character_info": char_info_dict,
                          "world_info": world_info_dict,
                          "character_time_cached": cache_time,
                          "world_time_cached": world_cache_time}

        """
        fetch_char_query = search_character_query
        suffix = "people/"
        search_params = {"name": fetch_char_query}

        # no check on request seemed a bit overkill
        char_response = requests.get(self.url + suffix, params=search_params)
        if char_response.ok:
            char_data = json.loads(char_response.text)["result"]
            # if search query found a character get the properties or else return empty dict
            if char_data:
                char_data = char_data[0]["properties"]  # get the properties dictionary
            else:
                char_data = {}
        else:
            print("Bad response: ", char_response)
            char_data = {"Bad Response": "Bad response"}
        return char_data

    @persistant_cache("test_search.json")
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
        fetch_world_url = world_url

        # no check on request seemed a bit overkill
        world_response = requests.get(fetch_world_url)
        if world_response.ok:
            world_data = json.loads(world_response.text)["result"]["properties"]  # get the properties dictionary
        else:
            print("Bad Response: ", world_response)
            world_data = {"Bad Response": "Bad response"}
        return world_data

    ####################################################################################################################
    #                                           Static Methods                                                         #
    ####################################################################################################################

    @staticmethod
    def delete_cache():
        """
        Static Method
        Clear cache by deleting the query_data.json file
        """
        try:
            os.remove(data_dir + 'query_data.json')
            print("removed cache")
            return True
        except FileNotFoundError:
            print("This galaxy was clean from the start stormtrooper!")
            return False

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
