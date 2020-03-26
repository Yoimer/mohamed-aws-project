
#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function # Python 2/3 compatibility
import boto3
from datetime import datetime
import json
import time


# dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

tableName = "sensors"
dynamodb_client = boto3.client('dynamodb')
existing_tables = dynamodb_client.list_tables()['TableNames']

# if tableName does not exist already, just create it
if tableName not in existing_tables:
    print("Creating table, {} please wait...".format(tableName))
    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': 'current',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'load-voltage',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'current',
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
            'current': "0.1762",
            'load-voltage': "12",
            'power': "2.114",
            "coordinate-x": "0.078453",
            "coordinate-y": "-0.509946",
            "coordinate-z": "10.002783",
            "date": str(now.strftime("%d/%m/%Y")),
            'time': str(now.strftime("%H:%M:%S"))
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
            'current': "0.1587",
            'load-voltage': "12",
            'power': "2.114",
            "coordinate-x": "0.078453",
            "coordinate-y": "-0.509946",
            "coordinate-z": "10.002783",
            "date": str(now.strftime("%d/%m/%Y")),
            'time': str(now.strftime("%H:%M:%S"))
        }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4))