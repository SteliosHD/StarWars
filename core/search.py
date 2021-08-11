# search module
import requests
import os
import json
from core.application_constants import URL, EARTH_ORBITAL_PERIOD, EARTH_ROTATION_PERIOD
from core.cache import persistant_cache


class Search:

    def __init__(self):
        self.url = URL

    def search_char(self, search_character_query):
        import pdb; pdb.set_trace();
        returned_data = self.fetch_char(search_character_query)
        cache_flag = returned_data[1]
        character_data = returned_data[0][0]["character_info"]
        if character_data:
            properties = character_data["result"][0]["properties"]
            char_name = properties["name"]
            char_height = properties["height"]
            char_mass = properties["mass"]
            char_birth_year = properties["birth_year"]
            # if cached print cache time
            if cache_flag:
                cache_info = returned_data[0][0]["character_time_cached"]
            else:
                cache_info = ''
            self.print_results(char_name,
                               char_height,
                               char_mass,
                               char_birth_year,
                               cache_info=cache_info)
        else:
            print("The force is not strong within you")

    def search_char_with_world(self, search_character_query, search_world_query):
        """ Seacrh character and get info about his/her homeworld"""
        returned_data = self.fetch_char_with_world(search_character_query, search_world_query)
        character_data, planet_data, cache_flag = returned_data[0][0]["character_info"],returned_data[0][0]["world_info"],  returned_data[1]
        if character_data:
            char_properties = character_data["result"][0]["properties"]  # needs [0] cause it returns a list
            char_name = char_properties["name"]
            char_height = char_properties["height"]
            char_mass = char_properties["mass"]
            char_birth_year = char_properties["birth_year"]
            if planet_data:
                planet_data = planet_data["world_info"]
                planet_properties = planet_data["result"]["properties"]  # does not need [0] cause it returns a dict
                planet_name = planet_properties["name"]
                planet_population = planet_properties["population"]
                planet_orbital_period = planet_properties["orbital_period"]
                planet_rotation_period = planet_properties["rotation_period"]
                plane_year_dur = EARTH_ORBITAL_PERIOD / planet_orbital_period
                plane_day_dur = EARTH_ROTATION_PERIOD / planet_rotation_period

                # if cached print cache time
                if cache_flag:
                    cache_info = returned_data[0][0]["character_time_cached"]
                else:
                    cache_info = ''
                self.print_results(char_name,
                                   char_height,
                                   char_mass,
                                   char_birth_year,
                                   planet_name,
                                   planet_population,
                                   plane_year_dur,
                                   plane_day_dur,
                                   cache_info=cache_info)
            else:
                print("A strong disturbance in the Force I feel. Know what happened I do not. Hmm.")
        else:
            print("The force is not strong within you")

    @persistant_cache('query_data.json')
    def fetch_char(self, *args):
        import pdb; pdb.set_trace();
        fetch_char_query = args[0]
        search_params = {"name": fetch_char_query}
        char_req = requests.get(self.url, params=search_params)
        char_data = json.loads(char_req.text)["result"]
        return char_data

    @persistant_cache('query_data.json')
    def fetch_char_with_world(self, *args):
        fetch_char_query_ww, fetch_world_query_ww = args[0], args[1]
        # search_params = {"name": fetch_char_query_ww}
        # char_req = requests.get(self.url, params=search_params)
        # char_data = json.loads(char_req.text)

        # call fetch_char to avoid unessecary requests if cashed
        char_data = self.fetch_char(fetch_char_query_ww)["character_info"]
        if char_data:
            char_data = char_data[0]  # unpack list else keep empty list
        if char_data.result:
            homeworld_url = char_data["result"][0]["properties"]["homeworld"]  # get homeworld planet url
            planet_req = requests.get(homeworld_url)
            planet_data = json.loads(planet_req.text)["result"]
        else:
            planet_data = []
        return [char_data, planet_data]

    @staticmethod
    def delete_cache():
        """
        Static Method
        Clear cache by deleting the query_data.json file
        """
        try:
            os.remove('query_data.json')
            print("removed cache")
        except FileNotFoundError:
            print("This galaxy was clean from the start stormtrooper!")
        return True

    @staticmethod
    def print_results(*args, cache_info='', include_world=False):
        """
            Print results
            Positional Arguments: char_name, char_height, char_mass, char_birth_year, planet_name, planet_poulation,
                                  planet_year_dur, planet_day_dur
        """
        char_name, char_height, char_mass, char_birth_year = args[0], args[1], args[2], args[3]
        print("Name: ",char_name)
        print("Height: ", char_height)
        print("Mass: ", char_mass)
        print("Birth Year: ", char_birth_year)
        if include_world:
            planet_name,planet_population, planet_year_dur, planet_day_dur = args[4], args[5], args[6], args[7]
            print("\n\n")
            print("Homeworld")
            print("-"*16)
            print("Name: ", planet_name)
            print("Population: ", planet_population)
            print("On {}, 1 year on earth is {:.2f} years and 1 day {:2f} days".format(planet_name,
                                                                                       planet_year_dur,
                                                                                       planet_day_dur))
        if cache_info:
            print(cache_info)








