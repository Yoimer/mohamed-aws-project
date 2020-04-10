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
import time

# aws and dynamo libraries
import boto3

# json library
import json

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

    # dynamodb settings
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    tableName = "sensors"
    dynamodb_client = boto3.client('dynamodb')
    existing_tables = dynamodb_client.list_tables()['TableNames']

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
    time.sleep(1)
    print("")

    current = float("{:9.6f}".format(current / 1000))

    # if current >= 0.1 starts sending data
    if(current >= 0.1):
         # if tableName does not exist already, just create it
        if tableName not in existing_tables:
            print("Creating table, {} please wait...".format(tableName))
            table = dynamodb.create_table(
                TableName=tableName,
                KeySchema=[
                    {
                        'AttributeName': 'time',
                        'KeyType': 'HASH'  #Partition key
                    },
                    {
                        'AttributeName': 'load-voltage',
                        'KeyType': 'RANGE'  #Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'time',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'load-voltage',
                        'AttributeType': 'S'
                    },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            print("Table status:", table.table_status)
            print("Table {} created successfully".format(tableName))
            time.sleep(1)
            print("Putting items on {} table, please wait...".format(tableName))
            time.sleep(5)
            table = dynamodb.Table(tableName)
            # datetime object containing current date and time
            now = datetime.now()
            response = table.put_item(
                Item={
                    'time': str(now.strftime("%H:%M:%S")),  # hour/minute/second
                    'current': "{:9.6f}".format(current / 1000),
                    'load-voltage': "{:6.3f}".format(12.0),
                    'power': "{:6.3f}".format((current / 1000) * 12),
                    "coordinate-x": xyz[0],
                    "coordinate-y": xyz[1],
                    "coordinate-z": xyz[2],
                    "date": str(now.strftime("%d/%m/%Y")) # day/month/year
                }
            )
            print("PutItem succeeded:")
            print(json.dumps(response, indent=4))
        # add new values to the table
        else:
            print("Table {} already exists".format(tableName))
            print("Putting new items on {} table, please wait...".format(tableName))
            time.sleep(1)
            table = dynamodb.Table(tableName)
            # datetime object containing current date and time
            now = datetime.now()
            response = table.put_item(
                Item={
                    'time': str(now.strftime("%H:%M:%S")),  # hour/minute/second
                    'current': "{:9.6f}".format(current / 1000),
                    'load-voltage': "{:6.3f}".format(12.0),
                    'power': "{:6.3f}".format((current / 1000) * 12),
                    "coordinate-x": xyz[0],
                    "coordinate-y": xyz[1],
                    "coordinate-z": xyz[2],
                    "date": str(now.strftime("%d/%m/%Y")) # day/month/year
                }
            )
            print("PutItem succeeded:")
            print(json.dumps(response, indent=4))       # sends data
    else:
        print("Fan is turned off. As long as it turns on, data will be sent to AWS Dynamo db")

    time.sleep(3)