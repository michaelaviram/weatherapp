
import pytest
import requests
import app

def test_reachability():
    website = requests.get("http://127.0.0.1:5000")

    assert website.status_code == 200
