import sys
import os
root_dir = os.getcwd()
sys.path.append(root_dir)

'''
This module contains constants that should be globally available to all classes
'''

data_dir = os.path.join(root_dir, "data/")
URL = "https://www.swapi.tech/api/"
EARTH_ORBITAL_PERIOD= 365
EARTH_ROTATION_PERIOD= 24
DEFAULT_FILENAME = 'query_data.json'
