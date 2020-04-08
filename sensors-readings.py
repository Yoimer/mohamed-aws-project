"""Sample code and test for adafruit_in219 and SW-420 accelerometer sensors"""

# adafruit_in219 libraries
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
import datetime
import time

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

    # date,temperature
    # 2019-11-14 00:00:00.000,51.5
    # 2019-11-14 01:00:00.000,56.2
    # 2019-11-14 02:00:00.000,58.3
    # 2019-11-14 03:00:00.000,62.4
    # 2019-11-14 04:00:00.000,66.5
    # 2019-11-14 05:00:00.000,70.6
    # 2019-11-14 06:00:00.000,65.7
    # 2019-11-14 07:00:00.000,45.8

    # datetime.datetime.utcnow()
    # 2020-04-07 23:39:51.679200

    # datetime object containing current date and time
    # now = datetime.now()

    # saves sensor data in list
    list_to_file = []

    # creates specific header depending on the variable
    headers_list = []
    headers_list.append("Load-Voltage(V)")                 # 0
    headers_list.append("Current(A)")                      # 1
    headers_list.append("Power(W)")                        # 2
    headers_list.append("Coordinate-X")                    # 3
    headers_list.append("Coordinate-Y")                    # 4
    headers_list.append("Coordinate-Z")                    # 5

    # date and time of reading

    # date space and time utc format
    # 2020-04-07 23:39:51.679200
    temp = str(datetime.datetime.utcnow()) + ","
    list_to_file.append(temp)

    ######################################## load voltage
    # load voltage
    temp = "{:6.3f}".format(12.0) + "\r\n"
    list_to_file.append(temp)

    headers = "Date," + headers_list[0] + "\r\n"
    # checks if file already exists
    if(os.path.isfile('/home/pi/project/load_voltage.csv')):
        # adds only new values to file
        f = open("load_voltage.csv", "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()
    else:
        # creates file including headers
        f = open("load_voltage.csv", "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()

    ######################################## current
    # date space and time utc format
    # 2020-04-07 23:39:51.679200
    temp = str(datetime.datetime.utcnow()) + ","
    list_to_file.append(temp)

    # current
    temp = "{:9.6f}".format(current / 1000) + "\r\n"
    list_to_file.append(temp)

    headers = "Date," + headers_list[1] + "\r\n"
    # checks if file already exists
    if(os.path.isfile('/home/pi/project/current.csv')):
        # adds only new values to file
        f = open("current.csv", "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()
    else:
        # creates file including headers
        f = open("current.csv", "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()

    ######################################## power
    # date space and time utc format
    # 2020-04-07 23:39:51.679200
    temp = str(datetime.datetime.utcnow()) + ","
    list_to_file.append(temp)

    # # power
    temp = "{:6.3f}".format((current / 1000) * 12) + "\r\n"
    list_to_file.append(temp)

    headers = "Date," + headers_list[2] + "\r\n"
    # checks if file already exists
    if(os.path.isfile('/home/pi/project/power.csv')):
        # adds only new values to file
        f = open("power.csv", "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()
    else:
        # creates file including headers
        f = open("power.csv", "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()

    ######################################## coordinates xyz
    # date space and time utc format
    # 2020-04-07 23:39:51.679200
    temp = str(datetime.datetime.utcnow()) + ","
    list_to_file.append(temp)

    # coordinates
    xyz = ("%f %f %f"%accelerometer.acceleration).split()

    ######################################### coordinates x
    temp = (xyz[0]) + "\r\n"
    list_to_file.append(temp)

    headers = "Date," + headers_list[3] + "\r\n"
    # checks if file already exists
    if(os.path.isfile('/home/pi/project/coordinate_x.csv')):
        # adds only new values to file
        f = open("coordinate_x.csv", "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()
    else:
        # creates file including headers
        f = open("coordinate_x.csv", "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()

    # date space and time utc format
    # 2020-04-07 23:39:51.679200
    temp = str(datetime.datetime.utcnow()) + ","
    list_to_file.append(temp)

    ######################################### coordinates y
    temp = (xyz[1]) + "\r\n"
    list_to_file.append(temp)

    headers = "Date," + headers_list[4] + "\r\n"
    # checks if file already exists
    if(os.path.isfile('/home/pi/project/coordinate_y.csv')):
        # adds only new values to file
        f = open("coordinate_y.csv", "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()
    else:
        # creates file including headers
        f = open("coordinate_y.csv", "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()

    # date space and time utc format
    # 2020-04-07 23:39:51.679200
    temp = str(datetime.datetime.utcnow()) + ","
    list_to_file.append(temp)

    ######################################### coordinates z
    temp = (xyz[2]) + "\r\n"
    list_to_file.append(temp)

    headers = "Date," + headers_list[5] + "\r\n"
    # checks if file already exists
    if(os.path.isfile('/home/pi/project/coordinate_z.csv')):
        # adds only new values to file
        f = open("coordinate_z.csv", "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()
    else:
        # creates file including headers
        f = open("coordinate_z.csv", "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()


    # # day/month/year
    # temp = now.strftime("%d/%m/%Y") + ","
    # list_to_file.append(temp)

    # # hour/minute/second
    # temp = now.strftime("%H:%M:%S") + ","
    # list_to_file.append(temp)

    # # load voltage
    # temp = "{:6.3f}".format(12.0) + ","
    # list_to_file.append(temp)

    # # current
    # temp = "{:9.6f}".format(current / 1000) + ","
    # list_to_file.append(temp)

    # # power
    # temp = "{:6.3f}".format((current / 1000) * 12) + ","
    # list_to_file.append(temp)

    # # coordinates
    # xyz = ("%f %f %f"%accelerometer.acceleration).split()

    # # coordinate x
    # temp = (xyz[0]) + ","
    # list_to_file.append(temp)

    # # coordinate y
    # temp = (xyz[1]) + ","
    # list_to_file.append(temp)

    # # coordinate z
    # temp = (xyz[2]) + "\r\n"
    # list_to_file.append(temp)

    # creates sensor.csv including all the values
    # headers = "Date,Time,Load-Voltage(V),Current(A),Power(W),Coordinate-X,Coordinate-Y,Coordinate-Z" + "\r\n"

    # # checks if file already exists
    # if(os.path.isfile('/home/pi/sensors.csv')):
    #     # adds only new values to file
    #     # print("file exists already")
    #     f = open("sensors.csv", "a+")
    #     for i in range(0, len(list_to_file)):
    #         print(list_to_file[i])
    #         f.write(list_to_file[i])
    #     f.close()
    # else:
    #     # creates file including headers
    #     # print("file does not exist")
    #     f = open("sensors.csv", "a+")
    #     f.write(headers)
    #     for i in range(0, len(list_to_file)):
    #         print(list_to_file[i])
    #         f.write(list_to_file[i])
    #     f.close()

    time.sleep(2)