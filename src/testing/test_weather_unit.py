# Reviewed by Bronia

import os
import pytest
import json
from weather import DailyWeatherForecast
from weather import Parser
from weather import API
from weather import WeatherForecast



@pytest.fixture
def api():
    setup = API()
    return setup

def test_get_geocoding(api):
    user_input = "Jerusalem"
    api.get_geocoding(user_input)
    assert os.path.exists("./Jerusalem.json") == True
    os.remove("Jerusalem.json")

def test_get_forcast(api):
    latitude = 31.768
    longitude = 35.213
    api.get_forcast(latitude, longitude)
    assert os.path.exists("./forcast_data.json") == True
    os.remove("forcast_data.json")
    
    with pytest.raises(TypeError) as exinfo:
        api.get_forcast("hi", 5)
    assert str(exinfo.value) == "Coordinates must be of type float."
    assert os.path.exists("./forcast_data.json") == False



"""
To test the Parser class used a pre-generated
json file for 'Haifa', with all data required.
"""

@pytest.fixture
def parser():
    setup = Parser()
    return setup

def test_get_location(parser): 
    with open("test_location.json", "r") as f:
        file = json.load(f) 
        assert parser.get_location(file) == "Haifa"
        assert type(parser.get_location(file)) == str

    with pytest.raises(TypeError) as exinfo:
        parser.get_location(5)
    assert str(exinfo.value) == "Location must be type dict to parse."

def test_get_country(parser):
    with open("test_location.json", "r") as f:
        file = json.load(f)
        assert parser.get_country(file) == "Israel"
        assert type(parser.get_country(file)) == str

    with pytest.raises(TypeError) as exinfo:
        parser.get_country(5)
    assert str(exinfo.value) == "Country should be dict type to parse."

def test_get_latitude(parser):
    with open("test_location.json", "r") as f:
        file = json.load(f)
        assert parser.get_latitude(file) == 32.81841
        assert type(parser.get_latitude(file)) == float

    with pytest.raises(TypeError) as exinfo:
        parser.get_latitude("test")
    assert str(exinfo.value) == "Latitude must be dict type to parse."

def test_get_longitude(parser):
    with open("test_location.json", "r") as f:
        file = json.load(f)
        assert parser.get_longitude(file) == 34.9885
        assert type(parser.get_longitude(file)) == float

    with pytest.raises(TypeError) as exinfo:
        parser.get_longitude("test")
    assert str(exinfo.value) == "Longitude must be of type dict to parse."

def test_get_date(parser):
    with open("test_forcast.json", "r") as f:
        file = json.load(f)
        assert parser.get_date(file, 0) == "17/01/2025"
        assert type(parser.get_date(file, 0)) == str

    with pytest.raises(TypeError) as exinfo:
        parser.get_date("test", "test")
    assert str(exinfo.value) == "Date must be of type dict and index must be of \
            type int."

def test_get_day_temp(parser):
    with open("test_forcast.json", "r") as f:
        file = json.load(f)
        assert parser.get_day_temp(file, 0) == 18.2
        assert type(parser.get_day_temp(file, 0)) == float

    with pytest.raises(TypeError) as exinfo:
        parser.get_day_temp("test", "test")
    assert str(exinfo.value) == "Day_temp must be of type dict and index must be \
            of type int."

def test_get_night_temp(parser):
    with open("test_forcast.json", "r") as f:
        file = json.load(f)
        assert parser.get_night_temp(file, 0) == 14.0
        assert type(parser.get_night_temp(file, 0)) == float

    with pytest.raises(TypeError) as exinfo:
        parser.get_night_temp("test", "test")
    assert str(exinfo.value) == "Night_temp must be of type dict and index must be of type int."

def test_get_humidity(parser):
    with open("test_forcast.json", "r") as f:
        file = json.load(f)
        assert parser.get_humidity(file, 0) ==  79
        assert type(parser.get_humidity(file, 0)) == int

    with pytest.raises(TypeError) as exinfo:
        parser.get_humidity("test", "test")
    assert str(exinfo.value) == "Humidity must be of type dict and index must be of type int."


@pytest.fixture
def data():
    setup = WeatherForecast()
    return setup

def test_set_days(data):
    number_of_days = 7
    assert len(data.days) == 0
    with open("test_forcast.json", "r") as f:
        file = json.load(f)
        data.set_days(file, number_of_days)
    assert len(data.days) == number_of_days
    assert data.days[0].date == "17/01/2025" 
    assert data.days[6].date == "23/01/2025"
    assert data.days[0].day_temp == 18.2
    assert data.days[6].day_temp == 17.6
    assert data.days[0].night_temp == 14.0 
    assert data.days[6].night_temp == 10.5
    assert data.days[0].humidity == 79
    assert data.days[6].humidity == 77
    for i in range(number_of_days):
            assert data.days[i].date is not None
            assert data.days[i].day_temp is not None
            assert data.days[i].night_temp is not None
            assert data.days[i].humidity is not None

    with pytest.raises(TypeError) as exinfo:
        data.set_days("test", "test")
    assert str(exinfo.value) == "Days should be of type dict and number_of_days of type int."

        
    
    


        

