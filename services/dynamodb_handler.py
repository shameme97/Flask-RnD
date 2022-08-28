import re
import boto3
import os
from decouple import config

AWS_ACCESS_KEY_ID     = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = os.environ.get("REGION_NAME")

client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
    endpoint_url="http://dynamodb.host:4566",
)
resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
    endpoint_url="http://dynamodb.host:4566",
)

def CreateATableMovie():
    # return 
    try:
        client.create_table(
            AttributeDefinitions = [ # Name and type of the attributes
                {
                    'AttributeName': 'id', # Name of the attribute
                    'AttributeType': 'N'   # N -> Number (S -> String, B-> Binary)
                }
            ],
            TableName = 'Movie', # Name of the table
            KeySchema = [       # Partition key/sort key attribute
                {
                    'AttributeName': 'id',
                    'KeyType'      : 'HASH'
                    # 'HASH' -> partition key, 'RANGE' -> sort key
                }
            ],
            BillingMode = 'PAY_PER_REQUEST',
            Tags = [ # OPTIONAL
                {
                    'Key' : 'test-resource',
                    'Value': 'dynamodb-test'
                }
            ]
        )
        return "Table created"
    except:
        return "Table is ready"


MovieTable = resource.Table('Movie')

def addItemToMovie(id, title, author):
    response = MovieTable.put_item(
        Item = {
            'id'     : id,
            'title'  : title,
            'director' : author,
            'rating'  : 0
        }
    )
    return response

def GetItemFromMovie(id):
    response = MovieTable.get_item(
        Key = {
            'id'     : id
        },
        AttributesToGet=[
            'title', 'director'
        ]
    )
    return response

def UpdateItemInMovie(id, data:dict):
    response = MovieTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates={
            'title': {
                'Value'  : data['title'],
                'Action' : 'PUT' # available options -> DELETE(delete), PUT(set), ADD(increment)
            },
            'director': {
                'Value'  : data['director'],
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW" # returns the new updated values
    )
    return response

def RateAMovie(id):
    response = MovieTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates = {
            'rating': {
                'Value'  : 1,   # Add '1' to the existing value
                'Action' : 'ADD'
            }
        },
        ReturnValues = "UPDATED_NEW"
    )
    # The 'rating' value will be of type Decimal, which should be  converted to python int type, to pass the response in json format.
    response['Attributes']['rating'] = int(response['Attributes']['rating'])
    return response

def DeleteAnItemFromMovie(id):
    response = MovieTable.delete_item(
        Key = {
            'id': id
        }
    )
    return response