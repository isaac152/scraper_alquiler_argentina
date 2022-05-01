#Python imports
import json
from glob import glob
from typing import List

#Local imports
from models.apartament import Apartament

#Constants
JSON_PATH = './data/*.json'
GRAPH_PATH = './graphs'

def get_data()->List[Apartament]:
    """Extract the data from folder with the json files"""
    data= []
    for filename in glob(JSON_PATH):
        with open(filename) as p:
            data_j = json.load(p)
        data.extend(data_j)
    return [Apartament(d) for d in data]    