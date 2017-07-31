#!/usr/bin/env python3


from darksky import forecast
import influxdb
import re


config = {
    'KEY': 'XXXXXXXXXXXXXXXXXXX',
    'debug': True,
    'longitude': '-77.2520101',
    'latitude':   '39.1048032',
    'units': 'auto',
    'influxdb_host': 'localhost',
    'influxdb_database': 'weather_db',
    'influxdb_username': 'darksky',
    'influxdb_password': 'influx_darksky',
}

def get_key(filename): 
    file = open(filename, 'r')
    return file.read().rstrip()

if __name__ == '__main__':

    config['KEY'] = get_key('key.txt')
    print(config['KEY'])
    with forecast(config['KEY'], config['latitude'], config['longitude']) as weather:
        print(weather.daily.summary, end='\n---\n')


