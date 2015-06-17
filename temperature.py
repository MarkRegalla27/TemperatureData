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
import pandas.io.sql as psql
#from odict import odict #imports ordered dictionary library

cities = { "Atlanta": '33.762909,-84.422675',
           "Austin": '30.303936,-97.754355',
           "Boston": '42.331960,-71.020173',
           "Chicago": '41.837551,-87.681844',
           "Cleveland": '41.478462,-81.679435'
        }


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
#print 'Start Date' + str(start_date)
#print 'End Date' + str(end_date)
#print cities

con = lite.connect('weather.db')
cur = con.cursor()
'''
#Drop city_max_temp table if it exists already
with con:
    #cur.execute('DROP TABLE city_max_temp')	#Grid table as lesson gives
    cur.execute('DROP TABLE tidy_max_temp')	#Tidy version of table

#make a table of city, date, max temp
with con:
    cur.execute('CREATE TABLE tidy_max_temp (city TEXT, todays_date TEXT, max_temp TEXT)')
    #cur.execute('CREATE TABLE city_max_temp (day_of_reading INT, Atlanta REAL, Austin REAL, Boston REAL, Chicago REAL, Cleveland REAL)')

#Insert timestamps into each row of matrix style database table
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO city_max_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)
        #print query_date


#sql = "INSERT INTO city_max_temp (city, todays_date, max_temp) VALUES (?,?,?)"
#data_list[]

p = 1
#with con:
#Put temperatures in matrix style database
for k,v in cities.iteritems():
	#print k
    
    query_date = end_date - datetime.timedelta(days=31) #set value each time through the loop of cities
    #print query_date
    while query_date < end_date:
        query_date += datetime.timedelta(days=1)
		#print query_date
		
        r = requests.get(base_url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
		#print r.status_code		#prints url status.  If 400, then invalid request was made and will not fetch the data
		#print query_date
		#print r.url
		#max_temp = r.json()['daily']['data'][0]['temperatureMax']
		#print max_temp
		#cur.execute(sql,(cities['city'][i],readable_date, max_temp))
		

            #cur.execute('UPDATE city_max_temp SET ' + i + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
            #cur.execute("INSERT INTO city_max_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        with con:
            cur.execute('UPDATE city_max_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
            if p == 1:
                print 'UPDATE city_max_temp SET ' + str(k) + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + str(query_date.strftime('%s'))
                p = 2		  
        #increment query_date to the next day for next operation of loop, BUT IT WON'T right here
        #query_date = query_date + datetime.timedelta(days=1)




#put temperatures in tidy database
#nested loop needed

cities = pd.DataFrame(cities.items(), columns=['city', 'coordinates'])
cities.sort(columns=['city'], ascending=True, inplace=True)
cities.reset_index(inplace=True)
cities.drop('index', axis=1, inplace=True)
print cities['city']
#for row in cities.iterrows():
#    print row[1]['city']

#Insert timestamps and cities into rows of tidy database
query_date = end_date - datetime.timedelta(days=31)
with con:
    while query_date < end_date:
        query_date += datetime.timedelta(days=1)
        for row in cities.iterrows():
            cur.execute("INSERT INTO tidy_max_temp(city, todays_date) VALUES (?,?)", (str(row[1]['city']), int(query_date.strftime('%s')),))
        

query_date = end_date - datetime.timedelta(days=31) #set value each time through the loop of temperature collections
while query_date < end_date:
    query_date += datetime.timedelta(days=1)
    i = 0
    for row in cities.iterrows():
        url = base_url + row[1]['coordinates'] + ',' + query_date.strftime('%Y-%m-%dT12:00:00')	#row is a 2-dimensional variable, containing city and coordinates for each row
        r = requests.get(url)
        print r.status_code
        #print r.json()
        #print r.url
        with con:
            #if p == 2:
                #print 'UPDATE tidy_max_temp SET ' + str(row[1]['city']) + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE city = ' + str(query_date.strftime('%s'))
                #p = 3
            
            update_sql = """UPDATE tidy_max_temp SET max_temp = """ + str(r.json()['daily']['data'][0]['temperatureMax']) + """ WHERE city = '""" + str(row[1]['city']) + """' AND todays_date = """ + str(query_date.strftime('%s'))
            print update_sql
            cur.execute(update_sql)
            
            i += 1

	#print i
	#if i == 30:
	#	break
'''

#Select and print range of temperatures for each city
Tempdf = pd.read_sql_query("SELECT * from tidy_max_temp", con)
print Tempdf

cities_list = Tempdf['city'].unique()
print cities_list

tempString = '{0} Temperature Range is: {1}'
for city in cities_list:
    tempRange = str(Tempdf.ix[Tempdf['city'] == city, 'max_temp'].max() - Tempdf.ix[Tempdf['city'] == city, 'max_temp'].min())
    #check data types in line above
    print tempString.format(city, tempRange)
'''
for i in Tempdf.iterrows():
	print 'Austin Temperature Range is ' + str(max(Tempdf['Austin']) - min(Tempdf['Austin']))
	print 'Austin Average Temperature is ' + str(Tempdf['Austin'].mean())
	print 'Austin Temperature variance is ' + str(Tempdf['Austin'].var())

#scatter_matrix(Tempdf, alpha=0.05, figsize=(6,6))
#plt.show()


with con:
	cur.execute("SELECT * from city_max_temp")
	Tempdf = cur.fetchall()
	Tempdf = pd.DataFrame(Tempdf)
	scatter_matrix(Tempdf, alpha=0.05, figsize=(6,6))
	plt.show()

	#print 'Austin Temperature Range is ' + str(max(Tempdf['Austin']) - min(Tempdf['Austin']))
	#print 'Austin Average Temperature is ' + str(Tempdf['Austin'].mean())
	#print 'Austin Temperature variance is ' + str(Tempdf['Austin'].var())

	
	cur.execute("SELECT max(Austin) FROM city_max_temp")
	theMax = cur.fetchall()
	print type(theMax)
	theMax = map(lambda theMax: float(theMax))
	print type(theMax)

	cur.execute("SELECT min(Austin) FROM city_max_temp")
	theMin = cur.fetchall()
	print type(theMin)
	theMin = map(float, theMin)
	print type(theMin)
	#theRange = float(theMax) - float(theMin)
	#print 'Austin temperature range = ' + theRange

	cur.execute("SELECT avg(Austin) from city_max_temp")
	theAvg = cur.fetchall()
	theAvg = pd.DataFrame(theAvg)
	print 'Average temperature in Austin is ' + str(theAvg.mean())

	cur.execute("SELECT var(Austin) from city_max_temp")
	theVar = cur.fetchall()
	print 'Temperature variance in Austin is ' + str(theVar)

con.close()
'''


# cd /users/markregalla/projects/temperaturefiles



