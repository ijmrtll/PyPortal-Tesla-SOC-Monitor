import sys
import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
from adafruit_pyportal import PyPortal
from tesla_stats import Model3

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]

sys.path.append(cwd)

#graphics for tesla stats
import tesla_gfx 

# change to True to get debug prints
DEBUG = False

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# create pyportal object w no data source (we'll feed it text later)
pyportal = PyPortal(url = None,
                    json_path = [],
                    status_neopixel = board.NEOPIXEL,
                    default_bg = None,
                   )

pyportal.set_backlight(1.0)
gfx = tesla_gfx.Tesla_gfx(pyportal.splash, debug=DEBUG)

# display while user waits
gfx.append_background()
gfx.display_loading()


#Create a wifi object to get the data outside pyportal
if DEBUG:
    print("Creating wifi object...")
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(pyportal._esp, secrets, pyportal.neopix)


# Uncomment the  two lines below to get the access tocken. 
# Add the email and password for the tesla account.
# Use a terminal window to get the access_token.
# Update the key in the secrets.py file and then find the car id.
# To do: Parse the token.
#
#r = wifi.post("https://owner-api.teslamotors.com/oauth/token?grant_type=password&client_id=" + secrets['TESLA_CLIENT_ID'] + "&client_secret=" + secrets['TESLA_CLIENT_SECRET'] + "&email=email@email.com&password=PASSWORD")
#res = r.json(); r.close(); print(res)

# With the access_token updtaed, uncomment the following lines to search for the vehicle ID.
# Use a terminal window
# Update the id in the secrets.py
#
#r = wifi.get("https://owner-api.teslamotors.com/api/1/vehicles/", headers={"Authorization": "Bearer " + secrets['access_token']})
#res = r.json(); r.close(); print(res)


# Create car object
if DEBUG:
    print("Creating car object...")
    
# Change this name for the name of your car. You will need to update the code.
babyShark = Model3(secrets, wifi, debug=DEBUG)

# This is the refesh rate for the time and it is set to 60 min.
refresh_localtime_rate = 60 
localtime_refresh = None

# This is the refresh rate for the SOC and is set to 20 min.
refresh_SOC_rate = 20
SOC_refresh = None

was_touched = False
if DEBUG:
    print("Creating loop...")
while True:

    # only query the online time once per hour (and on first run)
    if (not localtime_refresh) or (time.monotonic() - localtime_refresh) > refresh_localtime_rate*60:
        try:
            #getting time from the internet
            pyportal.get_local_time()
            localtime_refresh = time.monotonic()
        except RuntimeError as e:
            #an error ocurred
            continue

    if pyportal.touchscreen.touch_point:
        pyportal.set_backlight(0.5)
        was_touched = True

    # only query the SOC every refresh_SOC_rate seconds (and on first run) or when pressing the touchscreen
    if (not SOC_refresh) or was_touched or (time.monotonic() - SOC_refresh) > refresh_SOC_rate*60:
        if babyShark.getSOC() == "OK":
            gfx.clear_text()
            if babyShark.getChargingStatus() == "OK":
                gfx.display_bat(babyShark.SOC, babyShark.charging_status)
            else:
                gfx.display_bat(babyShark.SOC, "UNK")
        else:
            gfx.clear_text()
            gfx.display_bat("NA", "NA")
        time.sleep(5)
        was_touched = False
        SOC_refresh = time.monotonic()

    gfx.update_time()
    if gfx.time_hour >= 6 and gfx.time_hour < 22 :
        refresh_SOC_rate = 10
        pyportal.set_backlight(0.5)
    else:
        refresh_SOC_rate = 60
        pyportal.set_backlight(0.0)