#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from darksky import forecast
from influxdb import InfluxDBClient

import re
import sys


config = {
    'KEY': 'XXXXXXXXXXXXXXXXXXX',
    'debug': True,
    'longitude': '-77.2520101',
    'latitude':   '39.1048032',
    'location': 'Gaithersburg',
    'units': 'auto',
    'influxdb_host': 'localhost',
    'influxdb_port': '8086',
    'influxdb_database': 'weather_db',
    'influxdb_username': 'darksky',
    'influxdb_password': 'influx_darksky',
}


def get_key(filename): 
    file = open(filename, 'r')
    return file.read().rstrip()

def is_number(x):
    try:
        return 0 == x*0
    except:
        return False


def make_point(time, measurement, tags, fields):
    point={}
    point['time']=time
    point['measurement']=measurement
    point['tags']={}
    point['fields']={}
    for key, value in tags.items():
        point['tags'][key]=value

    for key, value in fields.items():
        if is_number(value):
            point['fields'][key]=value
        else:
            point['fields'][key]='"'+str(value)+ '"'

    return point


def point2line(point):

    tags   = ','.join( [ "{}={}".format(k,v)  for k,v in sorted(point['tags'  ].items()) ])
    fields = ','.join( [ "{}={}".format(k,v)  for k,v in sorted(point['fields'].items()) ])
    line = ' '.join([point['measurement']+','+tags, fields, str(point['time'])])

    return line
    
def darksky2dict(darksky,datatype):

    data = {}
    keys = [
        'time'                ,  # time of data measured (current), or when in the future the forecast is good for (i.e. off in the future)

        'temperature'         ,
        'pressure'            ,
        'dewPoint'            ,
        'humidity'            ,
        'apparentTemperature' ,

        'precipIntensity'     ,
        'precipProbability'   ,
        'precipType'          ,

        'cloudCover'          ,
        'ozone'               ,
        'uvIndex'             , 
        'visibility'          ,

        'windBearing'         ,
        'windSpeed'           ,
        'windGust'            ,

        'nearestStormBearking',
        'nearestStormDistance',
    ]
 
    #print(darksky._data)

    for k in keys:
        if k in darksky._data:
            data[k]=darksky._data[k]
        #else:
        #    print("{}: Missing {}".format(datatype,k))

    return data


if __name__ == '__main__':

    config['KEY'] = get_key('key.txt')
    print(config['KEY'])

    try:
        influxdb = InfluxDBClient(host=config['influxdb_host'],
                              port=config['influxdb_port'],
                              username=config['influxdb_username'],
                              password=config['influxdb_password'],
                              database=config['influxdb_database'])
    except Exception as err:
        print("Exception (failed to connect to influxdb): ", sys.exc_info()[0])
        sys.exit(1)
        

    points = []

    influx_tags={ 'lat' : config['latitude'],
                  'long': config['longitude'],
                  'loc' : config['location'], }

    with forecast(config['KEY'], config['latitude'], config['longitude']) as weather:
        print(weather.daily.summary, end='\n---\n')
        #rint((weather.currently._data.keys), end='\n---\n')
        #print((weather.hourly.__dict__), end='\n---\n')

        print(' '.join(map(str,[hour.temperature for hour in weather.hourly])))
        print(' '.join(map(str,[hour.windGust for hour in weather.hourly])))

        # This is the current, actual reported data; it is not a forecast.
        current_data = make_point(
                weather.currently.time, 
                'weather', 
                influx_tags,
                darksky2dict(weather.currently, 'current')
        )

        points.append(point2line(current_data))

        # this is forecast data, and not "real"
        # it is a list of datapoints, forecast at a given time, for a different 
        # time in the future.  For now, we just use the hourly data, which extends
        # ~48 hours in the future
        FT=weather.currently.time, 
        forecast_data = [ point2line(make_point(
                            hourly_data.time, 
                            'forecast',
                            influx_tags,
                            darksky2dict(hourly_data, 'hourly', forecast_time=FT)))
                          for hourly_data in weather.hourly ]

    #point = make_point(1234,'foo', {'alpha':'A', 'name':'bob'}, {'age':123, 'weight':1234})
    #print(point2line(point))

    influxdb_parameters = {
        'db': 'weather_db', 
        'precision':'s'
    }
    #print('\n'.join(points))
    #print(forecast_data)
    #print('\n'.join(forecast_data))
    influxdb.write(points, params=influxdb_parameters, protocol='line')
    influxdb.write(forecast_data, params=influxdb_parameters, protocol='line')


