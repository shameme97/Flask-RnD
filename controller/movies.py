from fileinput import filename
import random, string
from re import template
from flask import Flask, request, render_template, redirect, send_file, url_for
from flask_redis import FlaskRedis
import sys

sys.path.append("..") 
import services.dynamodb_handler as dynamodb
import services.redis_handler as redis
import services.s3_handler as s3


app = Flask(__name__, template_folder='../templates')
redis_client = redis.FlaskRedis(app)
UPLOAD_FOLDER = "uploads"



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
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    response = dynamodb.addItemToMovie(id, data['title'], data['director'], data['rating'])    
    
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

# S3
@app.route("/storage")
def storage():
    contents = s3.list_files(s3.BUCKET)
    print(contents)
    return render_template('storage.html', contents=contents)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        s3.upload_file(f"{f.filename}", s3.BUCKET)
        return redirect("/storage")


@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = s3.download_file(filename, s3.BUCKET)

        return send_file(output, as_attachment=True)



#  REDIS
@app.route('/redis/add')
def add():
    key = 'item1'
    value = 'value1'
    return redis_client.__setitem__(key, value)

@app.route('/redis/<string:key>')
def get(key):
    return redis_client.__getitem__(key)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)