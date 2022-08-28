from flask import Flask, request
import sys

sys.path.append("..") 
import services.dynamodb_handler as dynamodb


app = Flask(__name__)

@app.route('/')
def root_route():
    return dynamodb.CreateATableMovie()

#  Add a movie entry
#  Route: http://localhost:5000/movie
#  Method : POST
@app.route('/movie', methods=['POST'])
def addAMovie():

    data = request.get_json()
    # id, title, director = 1001, 'Angels and Demons', 'Dan Brown'

    response = dynamodb.addItemToMovie(data['id'], data['title'], data['director'])    
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    }

#  Read a movie entry
#  Route: http://localhost:5000/movie/<id>
#  Method : GET
@app.route('/movie/<int:id>', methods=['GET'])
def getMovie(id):
    response = dynamodb.GetItemFromMovie(id)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        
        if ('Item' in response):
            return { 'Item': response['Item'] }

        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }


#  Delete a movie entry
#  Route: http://localhost:5000/movie/<id>
#  Method : DELETE
@app.route('/movie/<int:id>', methods=['DELETE'])
def DeleteAMovie(id):

    response = dynamodb.DeleteAnItemFromMovie(id)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Deleted successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    } 


#  Update a movie entry
#  Route: http://localhost:5000/movie/<id>
#  Method : PUT
@app.route('/movie/<int:id>', methods=['PUT'])
def UpdateAMovie(id):

    data = request.get_json()

    # data = {
    #     'title': 'Angels And Demons',
    #     'director': 'Daniel Brown'
    # }

    response = dynamodb.UpdateItemInMovie(id, data)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }   

#  Rate a movie
#  Route: http://localhost:5000/like/movie/<id>
#  Method : POST
@app.route('/rate/movie/<int:id>', methods=['POST'])
def RateMovie(id):

    response = dynamodb.RateAMovie(id)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'      : 'Rated the movie successfully',
            'Ratings'    : response['Attributes']['rating'],
            'response' : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)