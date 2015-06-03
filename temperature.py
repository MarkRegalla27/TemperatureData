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
#from odict import odict #imports ordered dictionary library

cities = { "Atlanta": '33.762909,-84.422675',
           "Austin": '30.303936,-97.754355',
           "Boston": '42.331960,-71.020173',
           "Chicago": '41.837551,-87.681844',
           "Cleveland": '41.478462,-81.679435'
        }

print cities

cities = pd.DataFrame(cities.items(), columns=['city', 'coordinates'])
cities.sort(columns=['city'], ascending=True, inplace=True)
cities.reset_index(inplace=True)
cities.drop('index', axis=1, inplace=True)
print cities

base_url = 'https://api.forecast.io/forecast/ed5384712a6c42598d505ff33c0bd2aa/'
#start_date = datetime.datetime.now() - datetime.timedelta(days=30)
start_date = datetime.datetime.now()
start_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%S%z')
#print start_date

#data_list[]
for row in cities.iterrows():
	url = base_url + row[1]['coordinates'] + ',' + start_date	#row is a 2-dimensional variable, containing city and coordinates for each row
	r = requests.get(url)
	print r.status_code		#prints url status.  If 400, then invalid request was made and will not fetch the data
	print r.url
	max_temp = r.json()['daily']['data'][0]['temperatureMax']
	print max_temp

	#make a table of city, date, max temp
