# Weather forcast

## Overview

This simpple application recives a location from the user and returns forecast for the next week.

It is meant to run inside a kubernetes cluster, alongside a MySQL db to which it writes data.

## Installation

### venv 
 
```bash
pip install -r requirements.txt
```

### docker

```bash
docker build .
```

## Testing

for static analysis on a module:
```bash
pylint <moduble_name.py>
```

to test both unit and integration:
```bash
pytest
```

to test only unit:
```bash
pytest test_weather_unit.py

```

to test only integration:
```bash
pytest test_weather_integration.py
```

## Execution

### venv

```bash
python3 app.py
```
the click on the below link:
http://127.0.0.1:8989

### docker 
```bash
docker run -p 8989:8989 -d <image_name>
```
the click on the below link:
http://127.0.0.1:8989


