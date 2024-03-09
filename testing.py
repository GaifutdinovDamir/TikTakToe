import numpy as np
import json
import os.path

parentpath = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(parentpath, 'graph.json')

file = open(path, 'r')
graph = json.load(file)


