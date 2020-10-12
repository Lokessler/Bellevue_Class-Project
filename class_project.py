#!/usr/bin/python3

'''
Program:        Python Weather Forecast Search
Version:        4.0
Author:         Logan Kessler
Date:           08-30-2020
Description:    I'll add later...
'''
import json                     # for JSON file I/O
import time                     # for printing at a certain interval
from datetime import datetime   # convert date and time String
import requests                 # install via "pip3 install requests"

class ForecastCity():
    """
    Parent Class for: 'ForecastTemperature', 'ForecastConditions',
                      'ForecastFull', and ForecastList
    Base Class with city name, number of weather sets, and forecast time attributes
    """
    def __init__(self):
        """
        initialize attributes to be empty
        """
        self.city_name = ''
        self.count = 0
        self.f_time = ''

    # forecast "setter" methods
    def set_forecast_city(self, city):
        """
        Set: self's city name to passed 'city' variable.
        """
        self.city_name = str(city)
    def set_forecast_count(self, count):
        """
        Set: self's count to passed 'count' variable.
        """
        self.count = int(count)
    def set_forecast_datetime(self, forecast_time):
        """
        Set: JSON derived time String to easier to read time String
        """
        # source: https://docs.python.org/3.5/library/datetime.html
        f_dt = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S")
        self.f_time = str(f_dt.strftime("%B %d, %Y at %I:%M %p"))
    def pp_forecast_city_time(self):
        """
        Execute: 'pretty print' of ALL 'ForecastCity' Object's attributes
        """
        print('+-----------------------------------+')
        print(pp_tail("%s%s" %('| Weather in ', self.city_name), 37))
        print(pp_tail("%s%s" %('| On ', self.f_time), 37))

class ForecastTemperature(ForecastCity):
    """
    Parent Class: ForecastCity
    Inherits forecast attributes from 'ForecastCity' Class.
    Set: current temp, max temp, minimum temp, and "feels like" temp attributes
    """
    def __init__(self):
        """
        initialize attributes to be empty
        """
        super().__init__()
        self.temp = 0.0
        self.t_max = 0.0
        self.t_min = 0.0
        self.t_fl = 0.0

    def set_temp(self, temperature):
        """
        Set: self's temp to passed 'temperature' variable.
        """
        self.temp = float(temperature)
    def set_max_temp(self, max_temperature):
        """
        Set: self's max temp to passed 'max_temperature' variable.
        """
        self.t_max = float(max_temperature)
    def set_min_temp(self, min_temperature):
        """
        Set: self's minimum temp to passed 'min_temperature' variable.
        """
        self.t_min = float(min_temperature)
    def set_feels_like_temp(self, fl_temperature):
        """
        Set: self's feels like temp to passed 'fl_temperature' variable.
        """
        self.t_fl = float(fl_temperature)
    def pp_forecast_temperature(self):
        """
        Execute: 'pretty print' of ALL 'ForecastTemperature' Object's attributes
        """
        deg = ' degrees'
        print('+-----------------------------------+')
        print('|            Temperature            |')
        print('+-----------------------------------+')
        print(pp_tail("%s%.2f%s" %('|      Projected: ', self.temp, deg), 37))
        print(pp_tail("%s%.2f%s" %('|            Max: ', self.t_max, deg), 37))
        print(pp_tail("%s%.2f%s" %('|        Minimum: ', self.t_min, deg), 37))
        print(pp_tail("%s%.2f%s" %('|     Feels Like: ', self.t_fl, deg), 37))

class ForecastConditions(ForecastTemperature):
    """
    Parent Class: ForecastTemperature
    Inherits forecast attributes from 'ForecastTemperature' Class.
    Set: humidity, sky conditions, wind speed, and wind direction attributes
    """
    def __init__(self):
        """
        initialize attributes to be empty
        """
        super().__init__()
        self.humidity = 0
        self.sky = ''
        self.w_speed = 0.0
        self.w_dir = ''
    def set_humidity(self, humidity):
        """
        Set: self's humidity to passed 'humidity' variable.
        """
        self.humidity = int(humidity)
    def set_sky(self, sky_conditions):
        """
        Set: self's sky conditions to passed 'sky_conditions' variable.
        """
        self.sky = str(sky_conditions).title()
    def set_wind_speed(self, wind_speed):
        """
        Set: self's wind speed to passed 'wind_speed' variable.
        """
        self.w_speed = float(wind_speed)
    def set_wind_direction(self, wind_dir):
        """
        Set: self's wind direction to passed 'wind_dir' variable.
        Convert: float value of wind heading to N-E-S-W direction of String type.
        """
        # sourced data from: www.windfinder.com/wind/windspeed.htm
        if wind_dir > 0 and wind_dir < 22.5:
            self.w_dir = 'North'
        elif wind_dir >= 22.5 and wind_dir < 45:
            self.w_dir = 'North-Northeast'
        elif wind_dir >= 45 and wind_dir < 67.5:
            self.w_dir = 'Northeast'
        elif wind_dir >= 67.5 and wind_dir < 90:
            self.w_dir = 'East-Northeast'
        elif wind_dir >= 90 and wind_dir < 112.5:
            self.w_dir = 'East'
        elif wind_dir >= 112.5 and wind_dir < 135:
            self.w_dir = 'East-Southeast'
        elif wind_dir >= 135 and wind_dir < 157.5:
            self.w_dir = 'Southeast'
        elif wind_dir >= 157.5 and wind_dir < 180:
            self.w_dir = 'South-Southeast'
        elif wind_dir >= 180 and wind_dir < 202.5:
            self.w_dir = 'South'
        elif wind_dir >= 202.5 and wind_dir < 225:
            self.w_dir = 'South-Southwest'
        elif wind_dir >= 225 and wind_dir < 247.5:
            self.w_dir = 'Southwest'
        elif wind_dir >= 247.5 and wind_dir < 270:
            self.w_dir = 'West-Southwest'
        elif wind_dir >= 270 and wind_dir < 292.5:
            self.w_dir = 'West'
        elif wind_dir >= 292.5 and wind_dir < 315:
            self.w_dir = 'West-Northwest'
        elif wind_dir >= 315 and wind_dir < 337.5:
            self.w_dir = 'Northwest'
        elif wind_dir >= 337.5:
            self.w_dir = 'North-Northwest'

    def pp_forecast_conditions(self):
        """
        Execute: 'pretty print' of ALL 'ForecastConditions' Object's attributes
        """
        print('+-----------------------------------+')
        print('|            Conditions             |')
        print('+-----------------------------------+')
        print(pp_tail("%s%d%s" %('|       Humidity: ', self.humidity, '%'), 37))
        print(pp_tail("%s%.2f%s" %('|     Wind Speed: ', self.w_speed, ' mph'), 37))
        print(pp_tail("%s%s" %('| Wind Direction: ', self.w_dir), 37))
        print(pp_tail("%s%s" %('|  Sky Condition: ', self.sky), 37))

class ForecastList():
    """
    Parent Class: ForecastCity
    Set: append 'ForecastCity' or it's child Classes to List
    """
    def __init__(self):
        """
        initialize attribute to be empty
        """
        self.fcast_list = []

    def append_forecast(self, forecast):
        """
        Set: appends passed 'forecast' variable to self's forecast List Object.
        """
        self.fcast_list.append(forecast)

    def pp_forecast_list(self):
        """
        Execute: 'pretty print' of every List Object's 'ForecastCity' attributes.
        """
        for fcast in self.fcast_list:
            fcast.pp_forecast_city_time()
            fcast.pp_forecast_temperature()
            fcast.pp_forecast_conditions()
            print('+-----------------------------------+\n')

def pp_tail(string, max_string_len):
    """
    Parameters: String Object and max length the String will be padded to.
    Return: String Object padded with Spaces and a Pipe at the end.
    """
    while len(string) < max_string_len - 1:
        string += ' '
    string += '|'
    return string

def init_dialog():
    """
    Initial loop function to prompt user for input and choose way to search or exit.
    """
    lock = True
    while lock:
        try:
            str1 = '+-----------------------------+\n'
            str2 = '| Search for Weather Forecast |\n'
            str3 = '+-----------------------------+\n'
            str4 = '| 1. Search using ZIP code    |\n'
            str5 = '| 2. Search using city name   |\n'
            str6 = '| 3. Exit program             |\n'
            str7 = '+-----------------------------+'
            print("%s%s%s%s%s%s%s" %(str1, str2, str3, str4, str5, str6, str7))
            i_o = int(input('-->>> '))
            # when user chooses '3' exit loop and program
            if i_o == 3:
                lock = False
                return lock
            # let user search by ZIP with '1' or by city with '2'
            elif i_o == 1 or i_o == 2:
                if get_full_forecast(i_o):
                    return True
                else:
                    lock = True
            else:
                print('\nInput number 1, 2, or 3!')
        except ValueError:
            print('\nInput number 1, 2, or 3!')

def get_full_forecast(option):
    """
    Parameter: user chosen 'option' of '1' or '2' used to create proper API request.
    Return: True or False based on failed or successful request to API.
    Description: Creates API query based on ZIP code or a cities ID.
                 Stores successful request into a 'ForecastList' Object.
                 Prints 'ForecastList' Objects forecast data in 'pretty print'.
    """
    api_key = '95048d3dbeb334942022d6b1faf18c90'
    url = "https://api.openweathermap.org/data/2.5/forecast"
    # create empty user-defined 'Forecast_List' Object
    forecast_list = ForecastList()

    # change payload and "search prompt" based on users chosen method of searching
    if option is 1:
        search = zip_search()
        payload = {'zip': search, 'units': 'imperial', 'appid': api_key}
    elif option is 2:
        search = city_search()
        payload = {'id': search, 'units': 'imperial', 'appid': api_key}

    # try/catch block for 'Requests' module
    try:
        res = requests.get(url, params=payload, timeout=8.0)
        res.raise_for_status()
    # HTTP Error exception for any invalid 'HTTP codes'
    except requests.HTTPError:
        print('\nFailed to connect to OpenWeatherMap.org!\n')
        # return 'False' to start program from initial dialog prompt
        return False
    # one exception to validate no connection to https://openweathermap.org
    except (requests.ConnectionError, requests.Timeout, requests.RequestException):
        print('\nFailed to connect to OpenWeatherMap.org!\n')
        # return 'False' to start program from initial dialog prompt
        return False

    # HTTP status code is a '200' verification
    if res.ok:
        print('\nSuccessfully connected to OpenWeatherMap.org!\n')
        time.sleep(2)   # sleep to make it appear like works still being done
        owm_json = res.json()

    city = owm_json['city']['name'] # city name
    count = owm_json['cnt']         # number of forecast weather sets

    i = 0
    # parse JSON request to 'Forecast' Object and append to 'ForecastList' Object
    while i < count:
        # create user-defined 'ForecastFull' Object
        fcast = ForecastConditions()

        # set user-defined 'ForecastCity' Object inherited attributes
        fcast.set_forecast_city(city)
        fcast.set_forecast_count(count)
        # set and convert forcast's time String to a 'pretty print' version
        fcast.set_forecast_datetime(owm_json['list'][i]['dt_txt'])

        # set user-defined 'ForecastTemperature' Object inherited attributes
        fcast.set_temp(owm_json['list'][i]['main']['temp'])
        fcast.set_max_temp(owm_json['list'][i]['main']['temp_max'])
        fcast.set_min_temp(owm_json['list'][i]['main']['temp_min'])
        fcast.set_feels_like_temp(owm_json['list'][i]['main']['feels_like'])

        # set user-defined 'ForecastConditions' Object inherited attributes
        fcast.set_humidity(owm_json['list'][i]['main']['humidity'])
        fcast.set_sky(owm_json['list'][i]['weather'][0]['description'])
        fcast.set_wind_speed(owm_json['list'][i]['wind']['speed'])
        # set and convert forecast's wind direction integer to String to N-S-E-W
        fcast.set_wind_direction(owm_json['list'][i]['wind']['deg'])

        # append 'ForcastFull' Object to 'ForecastList' Object
        forecast_list.append_forecast(fcast)
        i += 1

    # call method to 'pretty print' ALL 'ForecastList' Object's data
    forecast_list.pp_forecast_list()
    return True

def zip_search():
    """
    Return: valid USA ZIP code used as 'payload' variable.
    Description: Loop until user input is a valid ZIP code, then return.
    """
    lock = True
    while lock:
        try:
            i_o = int(input('Please enter ZIP code\n-->>> '))
            # based on file 'zip-codes.txt' in repo
            if i_o > 10000 and i_o < 99951:
                lock = False
                return i_o
            else:
                print('\nPlease input number between [10001 - 99950]')
        except ValueError:
            print('\nPlease input number between [10001 - 99950]')

def city_search():
    """
    Return: valid city 'id' used as 'payload' variable from 'city.list.json' file.
    Description: Loop and read 'city.list.json' file to create 'valid_list' List..
    """
    lock = True
    valid_cities = []
    while lock:
        i_o = str(input('Please enter name of city\n-->>> '))
        # read JSON file of all OpenWeatherMap.org cities available
        with open('city.list.json', 'r') as file_handle:
            city_data = file_handle.read()

        for city in json.loads(city_data):
            if i_o.title() == str(city['name']).title():
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

def pp_city_chooser(city_list):
    """
    Parameters: valid 'city_list' of List Objects for user to choose from.
    Return: valid city 'id' used as 'payload' variable from 'city_list' List.
    Description: Loop until city from 'city_list' List is chosen by user.
    """
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
                print(pp_tail(str0, 31))
            else:
                str0 = "| %d. %s, %s" %(i, city['name'], city['country'])
                print(pp_tail(str0, 31))
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

def main():
    """
    Description: Initialize program to loop and count each search done by user.
                 Prints custom intro and outro message.
    """
    lock = True
    searches = 0
    # It's a habit now to have a welcome message.
    print("\nWelcome to LK's Weather Forecast Report!\n")
    # loop until user exits program.
    while lock:
        lock = init_dialog()
        if lock:
            searches += 1
            lock = True
        else:
            lock = False
    # My way of saying thank you to the user.
    print("%s%d%s" %("\nThank you for using LK's Weather Forecast Report ", searches, ' times!\n'))

###############
# Run Program #
###############
main()
