"""Sample code and test for adafruit_in219 and SW-420 accelerometer sensors"""

import time
import requests
import math
import random

# adafruit_in219 libraries
import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

# SW-420 accelerometer libraries
import busio
import adafruit_adxl34x

i2c_bus = board.I2C()
ina219 = INA219(i2c_bus)
print("ina219 test")

from datetime import datetime

# display some of the advanced field (just to test)
print("Config register:")
print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
print("  gain:                 0x%1X" % ina219.gain)
print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
print("  mode:                 0x%1X" % ina219.mode)
print("")

ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

# get accelerometer data
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

TOKEN = "BBFF-7w8odlanUiGHIGM6x2R7oziemqeRwq"  # Put your TOKEN here
DEVICE_LABEL = "machine"  # Put your device label here


VARIABLE_LABEL_1 = "Load Voltage"  # Put your first variable label here
VARIABLE_LABEL_2 = "Current"  # Put your second variable label here
VARIABLE_LABEL_3 = "Power"  # Put your third variable label here
VARIABLE_LABEL_4 = "Coordinate-X" # Put your fourth variable label here
VARIABLE_LABEL_5 = "Coordinate-Y" # Put your fifth variable label here
VARIABLE_LABEL_6 = "Coordinate-Z" # Put your sixth variable label here
VARIABLE_LABEL_7 = "Fan State" # Put your seventh variable label here

def build_payload(variable_1, variable_2, variable_3, variable_4, variable_5, variable_6, variable_7):

    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = ina219.current  # current in mA

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage

    print("Load Voltage:  {:6.3f} V".format(12.0))
    print("Current:       {:9.6f} A".format(current / 1000))
    print("Power:          {:6.3f} W".format(current / 1000 * 12))
    xyz = ("%f %f %f"%accelerometer.acceleration).split()
    print('Coordinate X: {} Coordinate Y: {} Coordinate Z: {}'.format(xyz[0], xyz[1], xyz[2]))
    print("")
    time.sleep(2)
    print("")


    # load voltage
    value_1 = "{:6.3f}".format(12.0)

    # current
    value_2 = float("{:9.6f}".format(current / 1000))

    # power
    value_3 = float("{:6.3f}".format((current / 1000) * 12))

    # coordinates
    xyz = ("%f %f %f"%accelerometer.acceleration).split()

    # coordinate x
    value_4 = (xyz[0])

    # coordinate y
    value_5 = (xyz[1])

    # coordinate z
    value_6 = (xyz[2])

    # if current >= 0.1 fan is on, else is off
    if(value_2 >= 0.1):
        value_7 = 1
    else:
        value_7 = 0


    payload = {
        variable_1: value_1,
        variable_2: value_2,
        variable_3: value_3,
        variable_4: value_4,
        variable_5: value_5,
        variable_6: value_6,
        variable_7: value_7
    }

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4, VARIABLE_LABEL_5, VARIABLE_LABEL_6, VARIABLE_LABEL_7)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)