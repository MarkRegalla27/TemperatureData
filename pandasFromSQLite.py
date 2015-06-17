import pandas as pd
import sqlite3 as lite
import datetime

import pandas.io.sql as psql

con = lite.connect('/Users/damian/Downloads/weather.db')

sql = 'SELECT * FROM city_max_temp'

dfTemps = psql.read_sql(sql, con)

print dfTemps

print 'Austin Temperature Range is ' + str(dfTemps['Austin'].max() - dfTemps['Austin'].min())
print 'Austin Average Temperature is ' + str(dfTemps['Austin'].mean())
print 'Austin Temperature variance is ' + str(dfTemps['Austin'].var())

dfCityTemps = pd.read_csv('/Users/damian/Downloads/cityTemp.csv')

print dfCityTemps

cities_list = dfCityTemps['City'].unique()

print cities_list

tempString = '{0} Temperature Range is: {1}'
for city in cities_list:
    tempRange = str(dfCityTemps.ix[dfCityTemps['City'] == city, 'Temp'].max() -
                    dfCityTemps.ix[dfCityTemps['City'] == city, 'Temp'].min())

    print tempString.format(city, tempRange)
