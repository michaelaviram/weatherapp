# Reviewed by Bronia
from datetime import datetime
from os import path 
from requests import get
from json import dump

class API:
    """
    This class handles open_meteo API requests.
    it recives json data and saves it on a temp file
    for future parsing.
    """

    def __init__(self):
        self.latitude = None
        self.longitude = None
    
    def get_geocoding(self, user_input: str) -> None:  
        if type(user_input) != str:
            print(f"{user_input} must be a string.")
            raise TypeError("Location must be string.")

        if path.exists(f"./{user_input}.json") == True:
            return

        url = f"https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": user_input
        }
        http_response = get(url, params=params)
        json_convert = http_response.json()
        with open(f"{user_input}.json", "w") as file:
            dump(json_convert, file)

        if path.exists(f"./{user_input}.json") == False:
            print("Unable to create Location file.")
            raise FileNotFoundError("Unable to create Location file.")

    def get_forcast(self, user_input: str, latitude: float, longitude: float) -> None:
        if type(latitude) != float and type(longitude) != float:
            print("Coordinates not of type float.")
            raise TypeError("Coordinates must be of type float.")

        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "relative_humidity_2m",
            "daily": "temperature_2m_max,temperature_2m_min"
        }
        http_response = get(url, params=params)
        json_convert = http_response.json()
        current_time = datetime.now()
        with open(f'./history/{user_input}-{current_time.strftime("%d-%m-%Y")}.json', "w") as file:
            dump(json_convert, file)

        if path.exists(f'./history/{user_input}-{current_time.strftime("%d-%m-%Y")}.json') == False:
            print("Unable to create Forcast Data file")
            raise FileNotFoundError("Unable to create Forcast file.")


class Parser:
    """
    Parses an open json file
    recived from open-meteo API.
    """

    def get_location(self, json: dict) -> str:
        if type(json) != dict:
            print("Location must be of type dict to parse.")
            raise TypeError("Location must be type dict to parse.")
    
        return json["results"][0]["name"]

    def get_country(self, json: dict) -> str:
        if type(json) != dict:
            print("Country must be of type dict to parse.")
            raise TypeError("Country should be dict type to parse.")
        return json["results"][0]["country"]

    def get_latitude(self, json: dict) -> str:
        if type(json) != dict:
            print("Latitude must be of type dict to parse.")
            raise TypeError("Latitude must be dict type to parse.")
        return json["results"][0]["latitude"]

    def get_longitude(self, json: dict) -> str:
        if type(json) != dict:
            print("Longitude must be of type dict to parse.")
            raise TypeError("Longitude must be of type dict to parse.")
        return json["results"][0]["longitude"]

    """
    The below four methods indicate which day to parse.
    """
    
    def format_date(self, date: str) -> str:
        if type(date) != str:
            print("Date must be of type str.")
            raise TypeError("Date must be of type str.")
        
        year, month, day = date.split('-')
        formatted_date = f'{day}/{month}/{year}'
        return formatted_date  

    
    def get_date(self, json: dict, index: int) -> str:
        if type(json) != dict and type(index) != int:
            print("Date must be of type dict and index must be of type int")
            raise TypeError("Date must be of type dict and index must be of \
            type int.")

        date = json["daily"]["time"][index]
        return self.format_date(date)
 
    def get_day_temp(self, json: dict, index: int) -> str:
        if type(json) != dict and type(index) != int:
            print("Day_temp must be of type dict and index must be of type int.")
            raise TypeError("Day_temp must be of type dict and index must be \
            of type int.")

        return json["daily"]["temperature_2m_max"][index]

    def get_night_temp(self, json: dict, index: int) -> str:
        if type(json) != dict and type(index) != int:
            print("Night_temp must be of type dict and index must be of type \
            int.")
            raise TypeError("Night_temp must be of type dict and index must be of type int.")
        return json["daily"]["temperature_2m_min"][index]

    def get_humidity(self, json: dict, index: int) -> str:
        if type(json) != dict and type(index) != int:
            print("Humidity must be of type dict and index must be of type \
            int.")
            raise TypeError("Humidity must be of type dict and index must be of type int.")
        humidity_average = 0
        hours_in_day = 24
        counter = 0 if index == 0 else index * hours_in_day
        for j in range(counter, (hours_in_day + counter)):
            humidity_average += json["hourly"]["relative_humidity_2m"][j]
        humidity_average //= hours_in_day
        return humidity_average
 
class DailyWeatherForecast:
    def __init__(self):
        self.date = None
        self.day_temp = None
        self.night_temp = None
        self.humidity = None
       
class WeatherForecast:
    """
    This class holds data of a week's weather forcast
    for a chosen location. It uses class 'Day' to hold
    the forcast data for each day in the week.
    """

    def __init__(self):
        self.location = None
        self.country = None
        self.days = []

    def set_days(self, json: dict, number_of_days: int) -> None:
        if type(json) != dict and type(number_of_days) != int:
            print("Days should be of type dict and number_of_days of type int.")
            raise TypeError("Days should be of type dict and number_of_days of type int.")

        parser = Parser()
        for i in range(number_of_days):
            new_day = DailyWeatherForecast()
            
            new_day.date = parser.get_date(json, i)
            if new_day.date == None:
                print(f"Unable to assign date to day {i}.")
                raise AttributeError(f"Unable to assign date to day {i}.")  
            
            new_day.day_temp = parser.get_day_temp(json, i)
            if new_day.day_temp == None:
                print(f"Unable to assign day_temp to day {i}.")
                raise AttributeError(f"Unable to assign day_temp to day {i}.")  

            new_day.night_temp = parser.get_night_temp(json, i)
            if new_day.night_temp == None:
                print(f"Unable to assign night_temp to day {i}.")
                raise AttributeError(f"Unable to assign night_temp to day {i}.")  

            new_day.humidity = parser.get_humidity(json, i)
            if new_day.humidity == None:
                print(f"Unable to assign humidity to day {i}.")
                raise AttributeError(f"Unable to assign humidity to day {i}.")  

            self.days.append(new_day)       

