# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it
# which would be not great. So, instead, keep it all in this one file and
# keep it a secret.

secrets = {
    'ssid' : 'ssidName',             # Keep the two '' quotes around the name
    'password' : 'PASSWORD',         # Keep the two '' quotes around password
    'timezone' : "America/Los_Angeles",  # http://worldtimeapi.org/timezones
    
    # to get the time from the internet I'm using the adafruit aio service
    'aio_username' : 'AdafruitAIOUSER',
    'aio_key' : 'AIOKEY',
    
    # Get the following two keys using the TESLA API, you can use the code.py for this
    'access_token' : "YourToken",
    'id_s' : "YourCarID",
    
    # To get the token, this comes from the un-official API https://www.teslaapi.io
    # Check to see if it has changed
    
    'TESLA_CLIENT_ID' : "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384",
    'TESLA_CLIENT_SECRET' : "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"
    }