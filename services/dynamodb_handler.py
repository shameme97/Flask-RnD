from decouple import config
import sys
sys.path.append("..")
from config.dynamoDBConfig import client, resource

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