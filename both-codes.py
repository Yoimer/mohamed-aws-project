"""Sample code and test for adafruit_in219 and SW-420 accelerometer sensors"""

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


# path libraries
import os.path

# time libraries
from datetime import datetime


# display some of the advanced field (just to test)
print("Config register:")
print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
print("  gain:                 0x%1X" % ina219.gain)
print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
print("  mode:                 0x%1X" % ina219.mode)
print("")

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V


# get accelerometer data
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# measure and display loop
while True:
    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = ina219.current  # current in mA

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage

    # print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
    # print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
    # print("Load Voltage:  {:6.3f} V".format(bus_voltage))
    print("Load Voltage:  {:6.3f} V".format(12.0))
    print("Current:       {:9.6f} A".format(current / 1000))
    print("Power:          {:6.3f} W".format(current / 1000 * 12))
    xyz = ("%f %f %f"%accelerometer.acceleration).split()
    print('Coordinate X: {} Coordinate Y: {} Coordinate Z: {}'.format(xyz[0], xyz[1], xyz[2]))
    print("")
    print("Saving data in file, please wait...")
    time.sleep(2)
    print("")

    
    # datetime object containing current date and time
    now = datetime.now()

    # saves sensor data in list
    list_to_file = []

    # date and time of reading

    # day/month/year
    temp = now.strftime("%d/%m/%Y") + ","
    list_to_file.append(temp)

    # hour/minute/second
    temp = now.strftime("%H:%M:%S") + ","
    list_to_file.append(temp)

    # bus_voltage + shunt_voltage
    # temp = "{:6.3f}".format(bus_voltage + shunt_voltage) + ","
    # list_to_file.append(temp)

    # shunt_voltage
    # temp = "{:9.6f}".format(shunt_voltage) + ","
    # list_to_file.append(temp)

    # bus_voltage
    # temp = "{:6.3f}".format(bus_voltage) + ","
    # list_to_file.append(temp)

    # load voltage
    temp = "{:6.3f}".format(12.0) + ","
    list_to_file.append(temp)

    # current
    temp = "{:9.6f}".format(current / 1000) + ","
    list_to_file.append(temp)

    # power
    temp = "{:6.3f}".format((current / 1000) * 12) + ","
    list_to_file.append(temp)

    # coordinates
    xyz = ("%f %f %f"%accelerometer.acceleration).split()

    # coordinate x
    temp = (xyz[0]) + ","
    list_to_file.append(temp)

    # coordinate y
    temp = (xyz[1]) + ","
    list_to_file.append(temp)

    # coordinate z
    temp = (xyz[2]) + "\r\n"
    list_to_file.append(temp)

    # headers = "Date,Time,PSU-Voltage(V),Shunt-Voltage(V),Bus-Voltage(V),Current(A),Power(W),Coordinate-X,Coordinate-Y,Coordinate-Z" + "\r\n"
    headers = "Date,Time,Load-Voltage(V),Current(A),Power(W),Coordinate-X,Coordinate-Y,Coordinate-Z" + "\r\n"

    # checks if file already exists
    if(os.path.isfile('/home/pi/sensors.csv')):
        # adds only new values to file
        # print("file exists already")
        f = open("sensors.csv", "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
    else:
        # creates file including headers
        # print("file does not exist")
        f = open("sensors.csv", "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()

    time.sleep(2)