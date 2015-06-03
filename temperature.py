import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from scipy import stats
import numpy as np
import statsmodels.api as sm
import math
import requests
from pandas.io.json import json_normalize
import sqlite3 as lite
import time  # a package with datetime objects
from dateutil.parser import parse  # a package for parsing a string into a Python datetime object
import collections
import datetime
#import odict #imports ordered dictionary library

cities = { "Atlanta": '33.762909, -84.422675',
            "Austin": '30.303936, -97.754355',
            "Boston": '42.331960, -71.020173',
            "Chicago": '41.837551, -87.681844',
            "Cleveland": '41.478462, -81.679435'
        }
#cities = OrderedDict(sorted(cities.items(), key=lambda t: t[0]))

print cities
'''
cities = pd.DataFrame(cities.items())
print cities

#print cities.iloc[0,0]

start_date = datetime.datetime.now() - datetime.timedelta(days=30)

#for i in cities
	#r[i] = requests.get('https://api.forecast.io/forecast/ed5384712a6c42598d505ff33c0bd2aa/') #not done yet
'''