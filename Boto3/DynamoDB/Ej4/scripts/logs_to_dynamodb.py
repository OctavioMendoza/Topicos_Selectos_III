import boto3
import json
from decimal import Decimal

def list_tables():
    db = boto3.client('dynamodb')
    response = db.list_tables()

    print(response['TableNames'])

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

def load_json(json_data, table_name):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table_name)

    for item in json_data:
        print(f"Adding item: {item}")
        table.put_item(Item=item)

if __name__ == "__main__":
    
    table_name = 'Orders'
    key_schema=[
            {
                'AttributeName':'CustomerID',
                'KeyType':'HASH'
            },

            {
                'AttributeName': 'OrderID',
                'KeyType': 'RANGE'
            }
        ]
    attribute_definitions=[
            {
                'AttributeName': 'CustomerID',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'OrderID',
                'AttributeType': 'S'
            }
        ]
    provisioned_throughput = {
            'ReadCapacityUnits':1,
            'WriteCapacityUnits':1
        }
    list_table = list_tables()

    if table_name not in list_table:
        create_table(table_name=table_name,
                     key_schema=key_schema,
                     attribute_definitions=attribute_definitions,
                     provisioned_throughput=provisioned_throughput)
        
    # Load Json
    json_file_path = '../logs/2025-02-26_20-39-26.log'
    with open(json_file_path) as json_file:
        orders_data = json.load(json_file, parse_float=Decimal)

    load_json(json_data=orders_data, table_name=table_name)



    #movie_table = create_table(table_name=table_name,
    #                           key_schema=key_schema,
    #                           attribute_definitions=attribute_definitions,
    #                           provisioned_throughput=provisioned_throughput)
    #print("Table status : ", movie_table.table_status)