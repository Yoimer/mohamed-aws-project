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

# list where fan states will be saved
save_fan_state = []
# first index equal minus 1
save_fan_state.append(-1)

# creates specific header depending on the variable
headers_list = []
headers_list.append("Load-Voltage(V)")                                                              # 0
headers_list.append("Current(A)")                                                                   # 1
headers_list.append("Power(W)")                                                                     # 2
headers_list.append("Coordinate-X")                                                                 # 3
headers_list.append("Coordinate-Y")                                                                 # 4
headers_list.append("Coordinate-Z")                                                                 # 5

# paths specific depending on the variable
path_list = []
path_list.append("/home/pi/CSVServer/csv/load_voltage.csv")                                         # 0
path_list.append("/home/pi/CSVServer/csv/current.csv")                                              # 1
path_list.append("/home/pi/CSVServer/csv/power.csv")                                                # 2
path_list.append("/home/pi/CSVServer/csv/coordinate_x.csv")                                         # 3
path_list.append("/home/pi/CSVServer/csv/coordinate_y.csv")                                         # 4
path_list.append("/home/pi/CSVServer/csv/coordinate_z.csv")                                         # 5


def create_and_save_csv(date_and_time, measured_variable, header_in_csv, path_for_csv):

    print("on create_and_save_csv")

    # saves sensor data in list
    list_to_file = []

    list_to_file.append(str(date_and_time) + ",")
    list_to_file.append(measured_variable)
    headers = "Date," + header_in_csv + "\r\n"

    # checks if file already exists
    if(os.path.isfile(path_for_csv)):
        print("File exists")
        # adds only new values to file
        f = open(path_for_csv, "a+")
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()
    else:
        print("File does not exist")
        # creates file including headers
        f = open(path_for_csv, "a+")
        f.write(headers)
        for i in range(0, len(list_to_file)):
            print(list_to_file[i])
            f.write(list_to_file[i])
        f.close()
        list_to_file.clear()

# measure and display loop
while True:

    current = ina219.current  # current in mA

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage

    print("Load Voltage:  {:6.3f} V".format(12.0))
    print("Current:       {:9.6f} A".format(current / 1000))
    print("Power:          {:6.3f} W".format(current / 1000 * 12))
    xyz = ("%f %f %f"%accelerometer.acceleration).split()
    print('Coordinate X: {} Coordinate Y: {} Coordinate Z: {}'.format(xyz[0], xyz[1], xyz[2]))
    print("")

    # saves actual values in a list
    variable_list = []
    # voltage
    variable_list.append("{:6.3f}".format(12.0) + "\r\n")   # 0
    # current
    variable_list.append("{:9.6f}".format(current / 1000) + "\r\n") # 1
    # power
    variable_list.append("{:6.3f}".format((current / 1000) * 12) + "\r\n")  # 2
    # coordinates
    xyz = ("%f %f %f"%accelerometer.acceleration).split()
    # coordinate x
    variable_list.append((xyz[0]) + "\r\n") # 3
    # coordinate y
    variable_list.append((xyz[1]) + "\r\n") # 4
    # coordinate z
    variable_list.append((xyz[2]) + "\r\n") # 5

    if(float(current >= 0.1)):

        # saves state to one
        save_fan_state[0] = 1

        print("Fan is ON, saving csv files")
        for i in range(0, len(variable_list)):
            create_and_save_csv(datetime.datetime.utcnow(), variable_list[i], headers_list[i], path_list[i])
    else:
        print("Fan is turned off. As long as it turns on, system will created csv files")
        # if previous state was one, reset to initial value and sends data for 10 seconds
        if(save_fan_state[0] == 1):
            save_fan_state[0] = -1
            j = 10
            while(j > 0):
                print("Creating csv files for {} seconds!".format(j))
                for i in range(0, len(variable_list)):
                    create_and_save_csv(datetime.datetime.utcnow(), variable_list[i], headers_list[i], path_list[i])
                time.sleep(1)
                j = j - 1

    time.sleep(2)