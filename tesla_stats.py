# Car object with the methods to parse the JSON

from adafruit_esp32spi import adafruit_esp32spi_wifimanager

class Model3:
    def __init__(self, secrets=None, WIFI=None, debug=False):
        self._id_s = secrets['id_s']
        self._access_token = secrets['access_token']
        self._wifi = WIFI
        self.SOC = 0
        self.SOC_response ={}
        self._debug = debug
        self.updated = False

    def getSOC(self):
        try:
            if self._debug:
                print("Getting SOC...")
            r = self._wifi.get(
                "https://owner-api.teslamotors.com/api/1/vehicles/" + self._id_s + "/data_request/charge_state",
                headers={"Authorization": "Bearer " + self._access_token})
            res = r.json()
            r.close()

            if self._debug:
                print(res)

            # Getting the battery level in percentage
            response = res['response']
            self.SOC_response = response
            if isinstance(response, dict):
                self.SOC = response['battery_level']
                self.updated = True
                if self._debug:
                    print("SOC: ", self.SOC, "%")
                    print("SOC OK")
                return "OK"
            else:
                if self._debug:
                    print("SOC UNKNOWN")
                self.updated = False
                return "UNK"

        except (ValueError, RuntimeError) as e:
            if self._debug:
                print("Failed to get data, retrying\n", e)
            self._wifi.reset
            return "ERR"

    def getChargingStatus(self):
        try:
            if isinstance(self.SOC_response, dict):
                self.charging_status = self.SOC_response['charging_state']
                if self._debug:
                    print("Charging Status: ", self.charging_status)
                return "OK"
            else:
                if self._debug:
                    print("Charging Status UNKNOWN")
                return "UNK"
        except (ValueError, RuntimeError) as e:
            if self._debug:
                print("Failed to get data, retrying\n", e)
            self._wifi.reset
            return "ERR"