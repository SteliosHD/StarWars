from pathlib import Path
# from sys import platform

'''
This module contains constants that should be globally available to all classes
'''

data_dir = Path("data")
URL = "https://www.swapi.tech/"
EARTH_ORBITAL_PERIOD= 365
EARTH_ROTATION_PERIOD= 24


# if platform == "linux" or platform == "linux2":
#     dataset = Path("data")
#     TRUST_FILE_PATH = dataset/"trust.txt"
#     RATINGS_FILE_PATH = dataset/"rating_with_timestamp.txt"
# else:
#     dataset = Path("dataset")
#     TRUST_FILE_PATH = dataset/"trust.txt"
#     RATINGS_FILE_PATH = dataset/"rating_with_timestamp.txt"