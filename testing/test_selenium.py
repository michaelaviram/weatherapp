import app
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    setup = webdriver.Chrome()
    setup.get("http://127.0.0.1:5000")
    yield setup
    setup.quit()

def test_valid_location_cursor_click(driver):
    """check a valid location name via clicking submit button"""

    search_bar = driver.find_element(By.NAME, "data")
    search_bar.send_keys("Haifa")
    search_bar.submit()
    assert "Country: Israel" in driver.page_source

def test_valid_location_enter_key(driver):
    """check a valid location name via typing enter"""

    search_bar = driver.find_element(By.NAME, "data")
    search_bar.send_keys("Haifa")
    search_bar.send_keys(Keys.RETURN)
    assert "Country: Israel" in driver.page_source

def test_invalid_location(driver):
    """check an invalid location"""

    search_bar = driver.find_element(By.NAME, "data") 
    search_bar.send_keys("kzjssdgnodsjgdsf")
    search_bar.submit()
    assert "Location does not exist!" in driver.page_source

def test_valid_location_in_wrong_country(driver):
    """check a valid location in the wrong country.
        (A famous city in a different country"""

    search_bar = driver.find_element(By.NAME, "data")
    search_bar.send_keys("cairo")
    search_bar.submit()
    assert "Country: United States" not in driver.page_source

def test_submit_empty_input(driver):
    """checks an empty location"""

    search_bar = driver.find_element(By.NAME, "data")
    search_bar.clear()
    search_bar.submit()
    assert "Location does not exist!" in driver.page_source


