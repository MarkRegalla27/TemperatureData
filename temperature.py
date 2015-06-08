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
'''
cities = pd.DataFrame(cities.items(), columns=['city', 'coordinates'])
cities.sort(columns=['city'], ascending=True, inplace=True)
cities.reset_index(inplace=True)
cities.drop('index', axis=1, inplace=True)
print cities['city'][1]
'''

base_url = 'https://api.forecast.io/forecast/ed5384712a6c42598d505ff33c0bd2aa/'
start_date = datetime.datetime.now() - datetime.timedelta(days=30)
#start_date = datetime.datetime.now()
#start_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%dT%H:%M:%S%z')
#start_date = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=30), '%Y-%m-%dT12:00:00')
#end_date = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%dT12:00:00')
end_date = datetime.datetime.now()
readable_date = start_date
query_date = end_date - datetime.timedelta(days=30)  #the current value being processed
#query_date = datetime.datetime.strftime(end_date - datetime.timedelta(days=30), '%Y-%m-%dT12:00:00') #the current value being processed
print 'Start Date' + str(start_date)
print 'End Date' + str(end_date)
#print cities

con = lite.connect('weather.db')
cur = con.cursor()

#Drop city_max_temp table if it exists already
with con:
    cur.execute('DROP TABLE city_max_temp')

#make a table of city, date, max temp
with con:
    #cur.execute('CREATE TABLE city_max_temp (city TEXT PRIMARY KEY, todays_date TEXT, max_temp TEXT)')
	cur.execute('CREATE TABLE city_max_temp (day_of_reading INT, Atlanta REAL, Austin REAL, Boston REAL, Chicago REAL, Cleveland REAL)')
'''
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO city_max_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)
        print query_date
'''
#sql = "INSERT INTO city_max_temp (city, todays_date, max_temp) VALUES (?,?,?)"
#data_list[]

i = 0
#with con:
#for row in cities.iterrows():
for k,v in cities.iteritems():
	print k

	query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
	print query_date
	
	while query_date < end_date:
		#url = base_url + row[1]['coordinates'] + ',' + start_date	#row is a 2-dimensional variable, containing city and coordinates for each row
		#r = requests.get(url)
		#r = requests.get(base_url + row[1]['coordinates'] + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
		r = requests.get(base_url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
		#print r.status_code		#prints url status.  If 400, then invalid request was made and will not fetch the data
		print query_date
		#Code below labeled "Label 1" inserts here
		
		with con:
			#cur.execute('UPDATE city_max_temp SET ' + i + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
			cur.execute("INSERT INTO city_max_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
			cur.execute('UPDATE city_max_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
		
		#increment query_date to the next day for next operation of loop, BUT IT WON'T
        query_date = query_date + datetime.timedelta(days=1) #increment query_date to the next day
        #print query_date
	#i += 1
	#print i
	#if i == 30:
	#	break



con.close()




# cd /users/markregalla/projects/temperaturefiles

#Label 1
#print r.url
#max_temp = r.json()['daily']['data'][0]['temperatureMax']
#print max_temp
#cur.execute(sql,(cities['city'][i],readable_date, max_temp))

