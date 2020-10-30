from datetime import datetime   # convert date and time String

class Forecast(object):
    """
    One Class to rule them all!
    """
    def __init__(self):
        """
        Set: self's variables to empty 'ForecastCity', 'ForecastTemperature',
             and 'ForecastConditions' Objects.
        """
        self.fdata = ()
    def convert_forecast_datetime(self, forecast_time):
        """
        Set: JSON derived time String to easier to read time String
        """
        # source: https://docs.python.org/3.5/library/datetime.html
        f_dt = datetime.strptime(forecast_time, "%Y-%m-%d %H:%M:%S")
        return str(f_dt.strftime("%B %d, %Y at %I:%M %p"))
    def convert_wind_direction(self, wind_dir):
        """
        Set: self's wind direction to passed 'wind_dir' variable.
        Convert: float value of wind heading to N-E-S-W direction of String type.
        """
        # sourced data from: www.windfinder.com/wind/windspeed.htm
        w_dir = ''
        if wind_dir > 0 and wind_dir < 22.5:
            w_dir = 'North'
        elif wind_dir >= 22.5 and wind_dir < 45:
            w_dir = 'North-Northeast'
        elif wind_dir >= 45 and wind_dir < 67.5:
            w_dir = 'Northeast'
        elif wind_dir >= 67.5 and wind_dir < 90:
            w_dir = 'East-Northeast'
        elif wind_dir >= 90 and wind_dir < 112.5:
            w_dir = 'East'
        elif wind_dir >= 112.5 and wind_dir < 135:
            w_dir = 'East-Southeast'
        elif wind_dir >= 135 and wind_dir < 157.5:
            w_dir = 'Southeast'
        elif wind_dir >= 157.5 and wind_dir < 180:
            w_dir = 'South-Southeast'
        elif wind_dir >= 180 and wind_dir < 202.5:
            w_dir = 'South'
        elif wind_dir >= 202.5 and wind_dir < 225:
            w_dir = 'South-Southwest'
        elif wind_dir >= 225 and wind_dir < 247.5:
            w_dir = 'Southwest'
        elif wind_dir >= 247.5 and wind_dir < 270:
            w_dir = 'West-Southwest'
        elif wind_dir >= 270 and wind_dir < 292.5:
            w_dir = 'West'
        elif wind_dir >= 292.5 and wind_dir < 315:
            w_dir = 'West-Northwest'
        elif wind_dir >= 315 and wind_dir < 337.5:
            w_dir = 'Northwest'
        elif wind_dir >= 337.5:
            w_dir = 'North-Northwest'
        return w_dir
    def parse_forecast_json(self, jdict):
        """
        parse openweathermap.org "5 day / 3 Hour" forecast JSON.
        """
        city = jdict['city']['name']    # fdata[0]
        cnt = jdict['cnt']              # fdata[1]
        i = 0
        while i < cnt:
            # convert JSON date and time to a more human-readable version
            ftime = jdict['list'][i]['dt_txt']              # fdata[2]
            ftime = self.convert_forecast_datetime(ftime)   # convert time String

            # temperature data
            temp = jdict['list'][i]['main']['temp']         # fdata[3]
            tmax = jdict['list'][i]['main']['temp_max']     # fdata[4]
            tmin = jdict['list'][i]['main']['temp_min']     # fdata[5]
            tfl = jdict['list'][i]['main']['feels_like']    # fdata[6]
            # weather condition data
            hum = jdict['list'][i]['main']['humidity']              # fdata[7]
            sky = jdict['list'][i]['weather'][0]['description']     # fdata[8]
            sky = sky.title()
            wspeed = jdict['list'][i]['wind']['speed']      # fdata[9]
            wdir = jdict['list'][i]['wind']['deg']          # fdata[10]
            wdir = self.convert_wind_direction(wdir)
            # set 'fdata' tuple attributes to Dictionary/JSON values
            self.fdata = (city, cnt, ftime, temp, tmax, tmin, tfl, hum, sky, wspeed,wdir)
            i += 1
            self.pp_forecast_full()
    def set_pp_string(self, string, max_string_len):
        """
        Parameters: String Object and max length the String will be padded to.
        Return: String Object padded with Spaces and a Pipe at the end.
        """
        while len(string) < max_string_len - 1:
            string += ' '
        string += '|'
        return string
    def pp_tail(self, string):
        """
        Takes a String and the minimum number of characters.
        """
        fout = self.set_pp_string(string, 37)
        return fout
    def pp_forecast_full(self):
        """
        Execute: 'pretty print' of all forecast data
        """
        deg = ' degrees'
        print('+-----------------------------------+')
        print(self.pp_tail("%s%s" %('| Weather in ', self.fdata[0])))
        print(self.pp_tail("%s%s" %('| On ', self.fdata[2])))
        print('+-----------------------------------+')
        print('|            Temperature            |')
        print('+-----------------------------------+')
        print(self.pp_tail("%s%.2f%s" %('|      Projected: ', self.fdata[3], deg)))
        print(self.pp_tail("%s%.2f%s" %('|            Max: ', self.fdata[4], deg)))
        print(self.pp_tail("%s%.2f%s" %('|        Minimum: ', self.fdata[5], deg)))
        print(self.pp_tail("%s%.2f%s" %('|     Feels Like: ', self.fdata[6], deg)))
        print('+-----------------------------------+')
        print('|            Conditions             |')
        print('+-----------------------------------+')
        print(self.pp_tail("%s%d%s" %('|       Humidity: ', self.fdata[7], '%')))
        print(self.pp_tail("%s%.2f%s" %('|     Wind Speed: ', self.fdata[9], ' mph')))
        print(self.pp_tail("%s%s" %('| Wind Direction: ', self.fdata[10])))
        print(self.pp_tail("%s%s" %('|  Sky Condition: ', self.fdata[8])))
        print('+-----------------------------------+\n')
