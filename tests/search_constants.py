# constants for test_search
search_query_1 = "yoda"
search_query_2 = "luke"
search_query_3 = "whatever"

print_name = "Luke Skywalker"
print_height = "172"
print_mass = "77"
print_birth = "19BBY"
print_planet = "Tatooine"
print_population = "200000"
print_year_dur = 304/365
print_day_dur = 23/24
cache_info = "cached: 2021-08-10 12:55:06.059097"

print_example_no_flag = ["Name: " + print_name,
                         "Height: " + print_height,
                         "Mass: " + print_mass,
                         "Birth Year: " + print_birth
                         ]
print_example_with_flag = ["Name: " + print_name,
                           "Height: " + print_height,
                           "Mass: " + print_mass,
                           "Birth Year: " + print_birth,
                           "\n\n",
                           "Homeworld",
                           "-" * 16,
                           "Name: " + print_planet,
                           "Population: " + print_population,
                           "On {}, 1 year on earth is {:.2f} years and 1 day {:.2f} days".format(print_planet,
                                                                                                print_year_dur,
                                                                                                print_day_dur)
                           ]

luke_skywalker = {'height': '172',
                  'mass': '77',
                  'hair_color': 'blond',
                  'skin_color': 'fair',
                  'eye_color': 'blue',
                  'birth_year': '19BBY',
                  'gender': 'male',
                  'created': '2021-08-11T11:10:19.975Z',
                  'edited': '2021-08-11T11:10:19.975Z',
                  'name': 'Luke Skywalker',
                  'homeworld': 'https://www.swapi.tech/api/planets/1',
                  'url': 'https://www.swapi.tech/api/people/1'
                  }
tatooine = {'diameter': '10465',
            'rotation_period': '23',
            'orbital_period': '304',
            'gravity': '1 standard',
            'population': '200000',
            'climate': 'arid',
            'terrain': 'desert',
            'surface_water': '1',
            'created': '2021-08-11T11:10:19.977Z',
            'edited': '2021-08-11T11:10:19.977Z',
            'name': 'Tatooine',
            'url': 'https://www.swapi.tech/api/planets/1'
            }

yoda = {"height": "66",
        "mass": "17",
        "hair_color": "white",
        "skin_color": "green",
        "eye_color": "brown",
        "birth_year": "896BBY",
        "gender": "male",
        "created": "2021-08-11T11:10:19.975Z",
        "edited": "2021-08-11T11:10:19.975Z",
        "name": "Yoda",
        "homeworld": "https://www.swapi.tech/api/planets/28",
        "url": "https://www.swapi.tech/api/people/20"}

yodas_planet = {'diameter': '0',
                'rotation_period': '0',
                'orbital_period': '0',
                'gravity': 'unknown',
                'population': 'unknown',
                'climate': 'unknown',
                'terrain': 'unknown',
                'surface_water': 'unknown',
                'created': '2021-08-11T11:10:19.977Z',
                'edited': '2021-08-11T11:10:19.977Z',
                'name': 'unknown',
                'url': 'https://www.swapi.tech/api/planets/28'}