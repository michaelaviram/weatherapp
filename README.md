# Weather forcast

### This application recives a location from the user and returns for cast for the next week.
Each days contain the following data:
- Date    
- Day Temperature    
- Night Temperature    
- Average humidity    

## Installation
 
```bash
pip install -r requirements.txt
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

## Exection

To run the app:
```bash
python3 app.py
```
the click on the below link:
http://127.0.0.1:5000
