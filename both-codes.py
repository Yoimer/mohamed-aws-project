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

    # saves sensor data in list adding a new line for each value
    list_to_file = []
    temp = "PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage) + "\r\n"
    list_to_file.append(temp)
    temp = "Shunt Voltage: {:9.6f} V".format(shunt_voltage) + "\r\n"
    list_to_file.append(temp)
    temp = "Load Voltage:  {:6.3f} V".format(bus_voltage) + "\r\n"
    list_to_file.append(temp)
    temp = "Current:       {:9.6f} A".format(current / 1000) + "\r\n"
    list_to_file.append(temp)
    xyz = ("%f %f %f"%accelerometer.acceleration).split()
    temp = 'Coordinate X: {} Coordinate Y: {} Coordinate Z: {}'.format(xyz[0], xyz[1], xyz[2]) + "\r\n"
    list_to_file.append(temp)

    print("Saving data in file")
    time.sleep(2)

    # file that saves all sensor values
    f = open("sensors.txt", "a+")
    for i in range(0, len(list_to_file)):
        print(list_to_file[i])
        f.write(list_to_file[i])
    f.close()

    time.sleep(2)