import boto3
import json
import os
from decimal import Decimal
import uuid
from datetime import datetime

def list_tables():
    db = boto3.client('dynamodb')
    response = db.list_tables()
    return response['TableNames']

def create_table(table_name, key_schema, attribute_definitions, provisioned_throughput):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )
    return table

def put_bash(table_name, items):
    db = boto3.resource('dynamodb')
    table = db.Table(table_name)
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

def is_file_in_date_range(filename, start_date, end_date):
    try:
        date_str = filename.split('.')[0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
        return start_date <= date_obj <= end_date
    except:
        return False

if __name__ == "__main__":
    table_name = 'Orders'
    key_schema=[
        {'AttributeName':'CustomerID','KeyType':'HASH'},
        {'AttributeName':'OrderID','KeyType':'RANGE'}
    ]
    attribute_definitions=[
        {'AttributeName': 'CustomerID','AttributeType': 'N'},
        {'AttributeName': 'OrderID','AttributeType': 'S'}
    ]
    provisioned_throughput = {'ReadCapacityUnits':1,'WriteCapacityUnits':1}

    if table_name not in list_tables():
        create_table(table_name, key_schema, attribute_definitions, provisioned_throughput)

    logs_dir = '../logs'
    start_date = datetime(2025, 3, 1)
    end_date = datetime(2025, 3, 10)

    for filename in os.listdir(logs_dir):
        if filename.endswith('.log') and is_file_in_date_range(filename, start_date, end_date):
            with open(os.path.join(logs_dir, filename)) as json_file:
                orders_data = json.load(json_file, parse_float=Decimal)

            item_list = []
            for item in orders_data:
                if not item.get('CustomerID'):
                    continue
                orderID = item['InvoiceNo'] + "-" + item['StockCode'] + "-" + uuid.uuid4().hex
                json_data = {
                    'CustomerID': Decimal(int(item['CustomerID'])),
                    'OrderID': orderID,
                    'Invoice': item['InvoiceNo'],
                    'OrderDate': item['InvoiceDate'],
                    'Quantity': Decimal(item['Quantity']),
                    'UnitPrice': Decimal(item['UnitPrice']),
                    'Description': item['Description'],
                    'Country': item['Country'].rstrip(),
                    'StockCode': item['StockCode']
                }
                item_list.append(json_data)

            put_bash(table_name, item_list)
