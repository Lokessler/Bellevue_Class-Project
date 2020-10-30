#!/usr/bin/python3

'''
Program:        Python Weather Forecast Search
Version:        6.0
Author:         Logan Kessler
Date:           10-13-2020
Description:    Connects to openweathermap.org to gather forecast information.
                User can search for weather forecast by ZIP code or city name.
'''
import json                     # for JSON file I/O
import time                     # for printing at a certain interval
import requests                 # install via "pip3 install requests"
from forecast import *


def pp_str(string, max_string_len):
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
                 Stores successful request into a 'Forecast' Object.
                 Prints 'Forecast' Object's forecast data in 'pretty print'.
    """
    api_key = '95048d3dbeb334942022d6b1faf18c90'
    url = "https://api.openweathermap.org/data/2.5/forecast"

    # change payload and "search prompt" based on users chosen method of searching
    if option is 1:
        search = zip_search()
        payload = {'zip': search, 'units': 'imperial', 'appid': api_key}
    elif option is 2:
        search = city_search()
        payload = {'id': search, 'units': 'imperial', 'appid': api_key}

    # try/catch block for 'Requests' module
    try:
        res = requests.get(url, params=payload, timeout=6.0)
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

    fcast = Forecast()                      # create 'Forecast' Object
    fcast.parse_forecast_json(res.json())   # parse JSON, store in 'Forecast' Object
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
                print(pp_str(str0, 31))
            else:
                str0 = "| %d. %s, %s" %(i, city['name'], city['country'])
                print(pp_str(str0, 31))
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
