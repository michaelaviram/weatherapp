# Reviewed by Bronia
from datetime import datetime
from json import load
from os import remove
import weather

def main(user_input: str) -> weather.WeatherForecast:
    """
    This function recives a name of a city or country
    and returns an object with data about that location's
    weather forcast for the next week.

    The first step is converting the location into geographic
    coordinations. The second is extracting the data.

    The program saves the data on temp files, which it then
    deteles on succesful execution.
    """
    if type(user_input) != str:
        print(f"{user_input} must be a string")
        raise TypeError("Location must be a string.")
        
    parser = weather.Parser()
    weather_forecast = weather.WeatherForecast()
    api = weather.API()
    current_time = datetime.now()

    api.get_geocoding(user_input)
    with open(f"{user_input}.json", "r") as f:
        file = load(f)
        weather_forecast.location = parser.get_location(file)
        weather_forecast.country = parser.get_country(file)
        api.latitude = parser.get_latitude(file)
        api.longitude = parser.get_longitude(file)
    remove(f"{user_input}.json")
        
    api.get_forcast(user_input, api.latitude, api.longitude)
    with open(f'./history/{user_input}-{current_time.strftime("%d-%m-%Y")}.json', "r") as f:
        number_of_days = 7
        file = load(f)
        weather_forecast.set_days(file, number_of_days)
    
    return weather_forecast







if __name__ == "__main__":
    
    user_input = input("Please enter test:")
    main(user_input)

    


