# Reviewed by Bronia

import os
import sys
import pytest
import json
import weather

@pytest.fixture
def api():
    setup = weather.API()
    return setup


@pytest.fixture
def parser():
    setup = weather.Parser()
    return setup

@pytest.fixture
def data():
    setup = weather.WeatherForecast()
    return setup

def test_integration(api, parser, data):
    user_input = "Haifa" 

    api.get_geocoding(user_input)
    assert os.path.exists("./Haifa.json") == True

    with open("Haifa.json", "r") as f:
        file = json.load(f)
        data.location = parser.get_location(file)
        assert data.location is not None

        data.country = parser.get_country(file)
        assert data.country is not None

        api.latitude = parser.get_latitude(file)
        assert api.latitude is not None

        api.longitude = parser.get_longitude(file)
        assert api.longitude is not None
    
    os.remove("Haifa.json")

    api.get_forcast(api.latitude, api.longitude)
    assert os.path.exists("./forcast_data.json") == True
    
    with open("forcast_data.json", "r") as f:
        number_of_days = 7
        file = json.load(f)
        data.set_days(file, number_of_days)

    os.remove("forcast_data.json")

    assert data.location == "Haifa"
    assert data.country == "Israel"
    assert len(data.days) == number_of_days
    for i in range(number_of_days):
        assert data.days[i].date is not None
        assert data.days[i].day_temp is not None
        assert data.days[i].night_temp is not None
        assert data.days[i].humidity is not None

    

