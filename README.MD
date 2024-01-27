# LED Matrix
Uses [Hzeller's rpi-rgb-led-matrix Github project](https://github.com/hzeller/rpi-rgb-led-matrix) 

A Python project for the Rasbperry Pi 3B+ Requiring:
- adafruit-hat-pwm
- RGB LED Matrix Panel – 64x64
- temper v3 USB thermometer


## What it displays
- Shows time, date and temperature by default.
- Can show a configurable pomodoro timer from the localhosted website.
- Show todays weather in the UK
    (using a free metoffice/datapoint api key)
    - Create a file under src/RPI-Led-Matrix-Python/env with the variables:
        - METOFFICE_KEY={api_key}
        - SITE_ID={siteID}
            - find your nearest site id, replacing with your api key 
            - http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=api_key

### In progress

