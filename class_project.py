#!/usr/bin/python3

'''
Program:        Python Weather Forecast Search
Version:        3.0
Author:         Logan Kessler
Date:           08-30-2020
Description:    I'll add later...
'''
import json         # for JSON file I/O
import time         # for printing at a certain interval
import requests     # install via "pip3 install requests"

def pp_spaces(string, max_string_len):
    while len(string) < max_string_len:
        string += ' '
    return string

def pp_init_dialog():
    str1 = '+-----------------------------+\n'
    str2 = '| Search for Weather Forecast |\n'
    str3 = '+-----------------------------+\n'
    str4 = '| 1. Search using ZIP code    |\n'
    str5 = '| 2. Search using city name   |\n'
    str6 = '| 3. Exit program             |\n'
    str7 = '+-----------------------------+'
    print(str1 + str2 + str3 + str4 + str5 + str6 + str7)

def pp_city_chooser(city_list):
    lock = True
    while lock:
        print('+-----------------------------+')
        print('|         Choose City         |')
        print('+-----------------------------+')
        i = 0
        for city in city_list:
            i += 1
            if city['state'] is not "":
                str0 = "| %d. %s, %s, %s" %(i, city['name'], city['state'], city['country'])
                print(pp_spaces(str0, 30) + '|')
            else:
                str0 = "| %d. %s, %s" %(i, city['name'], city['country'])
                print(pp_spaces(str0, 30) + '|')
        print('+-----------------------------+')
        try:
            choice = int(input('-->>> '))
            if choice > 0 and choice <= len(city_list):
                lock = False
                # returning 'city id' to query API
                return city_list[choice - 1]['id']
            else:
                print("%s%d%s" %('\nPlease choose a valid number [1 - ', len(city_list), ']'))
        except ValueError:
            print("%s%d%s" %('\nPlease choose a valid number [1 - ', len(city_list), ']'))

def pp_full_forecast(forecast):
    deg = ' degrees'    # word 'degrees' with single-space at element 0.
    print('\n5 Day Forecast for: ' + forecast[0] + '\n')
    # start loop at element 2 in List Object
    for fdata in forecast[2:]:
        # get 'wind_direction()' function
        print("%s%s" %('Time: ', fdata['time']))
        print("%s%.2f%s" %('Temperature: ', fdata['temp'], deg))
        print("%s%.2f%s" %('Max Temperature: ', fdata['temp_max'], deg))
        print("%s%.2f%s" %('Minimum Temperature: ', fdata['temp_min'], deg))
        print("%s%.2f%s" %('Feels Like: ', fdata['feels_like'], deg))
        print("%s%d%s" %('Humidity: ', fdata['humidity'], '%'))
        print("%s%.2f%s" %('Wind Speed: ', fdata['wind_speed'], ' mph'))
        print("%s%s" %('Wind Direction: ', wind_direction(fdata['wind_dir'])))
        print("%s%s%s" %('Sky: ', fdata['sky'].title(), '\n'))

def zip_search():
    lock = True
    while lock:
        try:
            i_o = int(input('Please enter ZIP code\n-->>> '))
            # based on file 'zip-codes.txt' in repo
            if i_o > 10000 and i_o < 99951:
                lock = False
                return i_o # mesh 'zip-code.txt' and 'city.list.json' file for 'id'?
            else:
                print('\nPlease input number between [10001 - 99950]')
        except ValueError:
            print('\nPlease input number between [10001 - 99950]')

def city_search():
    lock = True
    valid_cities = []
    while lock:
        i_o = str(input('Please enter name of city\n-->>> '))
        # read JSON file of all OpenWeatherMap.org cities available
        # file URL: http://bulk.openweathermap.org/sample/city.list.json.gz
        with open('city.list.json', 'r') as file_handle:
            city_data = file_handle.read()

        for city in json.loads(city_data):
            if i_o.title() == str(city['name']):
                valid_cities.append(city)   # append any valid 'city names' to List
                lock = False                # end loop
        # when a input 'city name' doesn't exist, prompt user they need to try again
        if lock:
            print("%s%s%s" %('\n', i_o.title(), ' is not a valid city name!'))

    # both to get 'city id' and check if only one 'city' has user input name
    num_cities = len(valid_cities)
    if num_cities == 1:
        # returning 'city id' to query API
        return valid_cities[num_cities - 1]['id']
    elif len(valid_cities) > 1:
        # allow user to choose city with 'pretty print' interface
        return pp_city_chooser(valid_cities)

def get_full_forecast(option):
    api_key = '95048d3dbeb334942022d6b1faf18c90'
    url = "https://api.openweathermap.org/data/2.5/forecast"
    weather_list = []
    jdict = {}

    if option is 1:
        search = zip_search()
        payload = {'zip': search, 'units': 'imperial', 'appid': api_key}
    elif option is 2:
        search = city_search()
        payload = {'id': search, 'units': 'imperial', 'appid': api_key}

    try:
        res = requests.get(url, params=payload, timeout=16.0)
        res.raise_for_status()
    # one exception to validate no connection to https://openweathermap.org
    except (requests.HTTPError, requests.ConnectionError, requests.Timeout, requests.RequestException):
        print('\nFailed to connect to OpenWeatherMap.org!\n')
        return 'ERROR'  # return 'ERROR' to start program from initial dialog prompt

    # HTTP status code is a '200'
    if res.ok:
        print('\nSuccessfully connected to OpenWeatherMap.org!\n')
        time.sleep(3)   # sleep to make it appear like works still being done
        owm_json = res.json()

    # append city name and number of forecasts requested to List
    weather_list.append(str(owm_json['city']['name']))    # city name
    weather_list.append(int(owm_json['cnt']))             # 40 'forecast' List items

    i = 0
    # parse JSON request to Dictionary of 40 'forecast' items
    while i < weather_list[1]:
        jdict['time'] = str(owm_json['list'][i]['dt_txt'])
        jdict['temp'] = float(owm_json['list'][i]['main']['temp'])
        jdict['temp_max'] = float(owm_json['list'][i]['main']['temp_max'])
        jdict['temp_min'] = float(owm_json['list'][i]['main']['temp_min'])
        jdict['feels_like'] = float(owm_json['list'][i]['main']['feels_like'])
        jdict['humidity'] = int(owm_json['list'][i]['main']['humidity'])
        jdict['sky'] = str(owm_json['list'][i]['weather'][0]['description'])
        jdict['wind_speed'] = float(owm_json['list'][i]['wind']['speed'])
        jdict['wind_dir'] = int(owm_json['list'][i]['wind']['deg'])

        # append Dictionary to a List of Dictionary 'forecasts'
        # copy() documentation: https://docs.python.org/3/library/copy.html
        weather_list.append(jdict.copy())   # copy() for new compound Object
        i += 1

    return weather_list

def wind_direction(wind):
    # sourced data from: www.windfinder.com/wind/windspeed.htm
    wdir = ''
    if wind > 0 and wind < 22.5:
        wdir = 'North'
    elif wind >= 22.5 and wind < 45:
        wdir = 'North-Northeast'
    elif wind >= 45 and wind < 67.5:
        wdir = 'Northeast'
    elif wind >= 67.5 and wind < 90:
        wdir = 'East-Northeast'
    elif wind >= 90 and wind < 112.5:
        wdir = 'East'
    elif wind >= 112.5 and wind < 135:
        wdir = 'East-Southeast'
    elif wind >= 135 and wind < 157.5:
        wdir = 'Southeast'
    elif wind >= 157.5 and wind < 180:
        wdir = 'South-Southeast'
    elif wind >= 180 and wind < 202.5:
        wdir = 'South'
    elif wind >= 202.5 and wind < 225:
        wdir = 'South-Southwest'
    elif wind >= 225 and wind < 247.5:
        wdir = 'Southwest'
    elif wind >= 247.5 and wind < 270:
        wdir = 'West-Southwest'
    elif wind >= 270 and wind < 292.5:
        wdir = 'West'
    elif wind >= 292.5 and wind < 315:
        wdir = 'West-Northwest'
    elif wind >= 315 and wind < 337.5:
        wdir = 'Northwest'
    elif wind >= 337.5:
        wdir = 'North-Northwest'
    return wdir

def run():
    lock = True
    while lock:
        try:
            pp_init_dialog()
            i_o = int(input('-->>> '))
            if i_o == 1:
                status = get_full_forecast(1)
                if status != 'ERROR':
                    pp_full_forecast(status)
            elif i_o == 2:
                status = get_full_forecast(2)
                if status != 'ERROR':
                    pp_full_forecast(status)
            elif i_o == 3:
                lock = False
                return 1
            else:
                print('Input number 1, 2, or 3!')
        except ValueError:
            print('Input number 1, 2, or 3!')
        lock = True

def main():
    # It's a habit now to have a welcome message.
    print("\nWelcome to LK's Weather Forecast Report!\n")
    # One function to 'run' them all!
    run()
    # My way of saying thank you to the user.
    print("\nThank you for using LK's Weather Forecast Report!\n")

###############
# Run Program #
###############
main()
