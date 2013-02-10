import os

ECHO_NEST_API_KEY = ''

# where to store analysis files
ANALYSES_DIR = 'analyses'

if not os.path.exists(ANALYSES_DIR):
    os.makedirs(ANALYSES_DIR)

# where to store the dataset produced by the analysis files
DATASET_FILE = 'dataset.csv'

# maps song id to analysis file
REGISTRY = 'registry.json'

# genres to ignore
IGNORE_GENRES = set([])

# print debug messages
DEBUG = True
